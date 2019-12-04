import os
from slackclient import SlackClient


slack_token = os.environ['SLACK_API_TOKEN']
channel_name = 'GMS5DNGSK'

sc = SlackClient(slack_token)

while True:

	history = sc.api_call("groups.history", channel=channel_name, count=1)

	if 'messages' in history:
		for message in  history['messages']:
			if 'text' in message:
				message = message['text']
				message = message.encode('UTF8')
				if message.startswith('<@UR9HA8KV2>'):
					message = message.replace('<@UR9HA8KV2>', '')

					if 'lunch' in message:
						sc.api_call("chat.postMessage", channel=channel_name, text="11:30", as_user=True)
					else:
						sc.api_call("chat.postMessage", channel=channel_name, text="keep pounding", as_user=True)

