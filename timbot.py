import os
from slackclient import SlackClient
import random
import datetime


slack_token = os.environ['SLACK_API_TOKEN']
channel_name = os.environ['SLACK_CHANNEL_NAME']
timbot_user_id = os.environ['SLACK_TIMBOT_USER_ID']

sc = SlackClient(slack_token)

while True:
	history = sc.api_call("groups.history", channel=channel_name, count=1)

	# look for a message in the chat that starts with '@timbot .....'
	if 'messages' in history:
		for message in  history['messages']:
			if 'text' in message:
				message = message['text']
				message = message.encode('UTF8')

				if 'openstack' in message:
					sc.api_call("chat.postMessage", channel=channel_name, text='i hear opensack is a career killer', as_user=True)


				if message.startswith(timbot_user_id):

					#message now equals what was after '@timbot'
					message = message.replace(timbot_user_id, '')

					#check what the message is
					if 'lunch' in message and 'where' in message:
						#send a message as timbot
						if datetime.datetime.today().weekday() == 4:
							places = ['pauls','moes','asian plus','99s']
							sc.api_call("chat.postMessage", channel=channel_name, text=random.choice(places), as_user=True)
						else:
							sc.api_call("chat.postMessage", channel=channel_name, text='epicurean feast', as_user=True)
					elif 'lunch' in message and ('time' in message or 'when' in message):
						#send a message as timbot
						sc.api_call("chat.postMessage", channel=channel_name, text="11:30", as_user=True)
					else:
						#send a message as timbot
						sc.api_call("chat.postMessage", channel=channel_name, text="keep pounding", as_user=True)

