import os
from slackclient import SlackClient
import random
import datetime

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

def handle_ideal_lunch_time(curr_time):
	if curr_time == ideal_lunch_time and alert:
		sc.api_call("chat.postMessage", channel=channel_name, text='IT IS THE IDEAL LUNCH TIME GO TO LUNCH', as_user=True)
		alert = False
	else:
		alert = True

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
					sc.api_call("chat.postMessage", channel=channel_name, text='i hear opensack is a career killer', as_user=True)

				# pong responce
				elif 'pong' in message:
					sc.api_call("chat.postMessage", channel=channel_name, text='im in. best 2 out of 3 games to 7?', as_user=True)

				if message.startswith(timbot_user_id):

					# message now equals what was after '@timbot'
					message = message.replace(timbot_user_id, '')

					# where to go to lunch
					if 'lunch' in message and 'where' in message:

						# if friday
						if datetime.datetime.today().weekday() == friday_index_elem:
							random.seed(datetime.datetime.now())

							# choose place to go
							places = ['pauls','moes','asian plus','99s']
							sc.api_call("chat.postMessage", channel=channel_name, text=random.choice(places), as_user=True)

						# mon-thur
						else:
							sc.api_call("chat.postMessage", channel=channel_name, text='epicurean feast', as_user=True)

					# what time is lunch
					elif 'lunch' in message and ('time' in message or 'when' in message):
						sc.api_call("chat.postMessage", channel=channel_name, text=ideal_lunch_time, as_user=True)

					# what to eat
					elif 'what' in message and 'eat' in message:
						sc.api_call("chat.postMessage", channel=channel_name, text="chicken sandwich", as_user=True)

					# base response
					else:
						sc.api_call("chat.postMessage", channel=channel_name, text="keep pounding", as_user=True)

if __name__ == '__main__':
	main()
