import os
from slackclient import SlackClient
import random


slack_token = os.environ['SLACK_API_TOKEN']
channel_name = 'GMS5DNGSK'

sc = SlackClient(slack_token)

while True:
	history = sc.api_call("groups.history", channel=channel_name, count=1)

	# look for a message in the chat that starts with '@timbot .....'
	if 'messages' in history:
		for message in  history['messages']:
			if 'text' in message:
				message = message['text']
				message = message.encode('UTF8')
				if message.startswith('<@UR9HA8KV2>'):

					#message now equals what was after '@timbot'
					message = message.replace('<@UR9HA8KV2>', '')

					#check what the message is
					if 'lunch' in message and 'where' in message:
						#send a message as timbot
						places = ['pauls','moes','asian plus','99s']
						sc.api_call("chat.postMessage", channel=channel_name, text=random.choice(places), as_user=True)
					elif 'lunch' in message and ('time' in message or 'when' in message):
						#send a message as timbot
						sc.api_call("chat.postMessage", channel=channel_name, text="11:30", as_user=True)
					else:
						#send a message as timbot
						sc.api_call("chat.postMessage", channel=channel_name, text="keep pounding", as_user=True)

