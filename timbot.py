import io
import os
import random
import datetime
import numpy as np
from slackclient import SlackClient

slack_token = os.environ['SLACK_API_TOKEN']
channel_name = os.environ['SLACK_CHANNEL_NAME']
timbot_user_id = os.environ['SLACK_TIMBOT_USER_ID']

sc = SlackClient(slack_token)

alert = True
ideal_lunch_time = "11:30"
friday_index_elem = 4

def main():
	while True:
		run_timbot()

def send_message(text):
	sc.api_call("chat.postMessage", channel=channel_name, text=text, as_user=True)

def handle_ideal_lunch_time(curr_time):
	if curr_time == ideal_lunch_time and alert:
		send_message('IT IS THE IDEAL LUNCH TIME GO TO LUNCH')
		alert = False
	else:
		alert = True

def uploadimage(path, title, text):
	with open(path, 'rb') as f:
		responce = sc.api_call(
			"files.upload",
			title='sampletitle',
			file=io.BytesIO(f.read())
		)
	fileinfo = responce['file']
	sc.api_call("files.sharedPublicURL", file=fileinfo['id'])
	image_url = fileinfo['permalink_public']
	attachments = [{"title": title, "image_url": image_url}]
	responce = sc.api_call("chat.postMessage", channel=channel_name, text=text, as_user=True, attachments=attachments)

def run_timbot():
	history = sc.api_call("groups.history", channel=channel_name, count=1)

	handle_ideal_lunch_time(datetime.datetime.now().strftime('%H:%M'))

	# look for a message in the chat that starts with '@timbot .....'
	if 'messages' in history:
		for message in  history['messages']:
			if 'text' in message:
				message = message['text']
				message = message.encode('UTF8')

				# openstack meme
				if 'openstack' in message:
					send_message('i hear opensack is a career killer')

				# pong responce
				elif 'pong' in message:
					send_message('im in. best 2 out of 3 games to 7?')

				if message.startswith(timbot_user_id):

					# message now equals what was after '@timbot'
					message = message.replace(timbot_user_id, '')

					# where to go to lunch
					if 'lunch' in message and 'where' in message:

						# if friday
						if datetime.datetime.today().weekday() == friday_index_elem:
							random.seed(datetime.datetime.now())

							# choose place to go
							places = ['pauls', 'asian plus', 'moes', 'the 99', 'chilis']
							weights = [0.5, 0.3, 0.1, 0.05, 0.05]
							choice = np.random.choice(places, p=weights)

							send_message(choice)

						# mon-thur
						else:
							send_message('epicurean feast')

					# what time is lunch
					elif 'lunch' in message and ('time' in message or 'when' in message):
						send_message(ideal_lunch_time)
						uploadimage('images/lunchchart.png', 'IdealLunchTimeChart','')

					# what to eat
					elif 'what' in message and 'eat' in message:
						# if friday
						if datetime.datetime.today().weekday() == friday_index_elem:
							send_message('Its friday enjoy a meal out. Maybe some french toast at pauls?')
						else:
							image_url = 'http://cafe.epicureanfeast.com/Clients/8680redhat.jpg'
							attachments = [{"title": 'Menu', "image_url": image_url}]              
							sc.api_call("chat.postMessage", channel=channel_name, text='Heres the cafe menu', as_user=True, attachments=attachments)
							send_message("may I suggest the chicken sandwich")

					# base response
					else:
						send_message('keep pounding')

if __name__ == '__main__':
	main()
