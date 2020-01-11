import io
import os
import random
import datetime
import time
import helpers
from slackclient import SlackClient

class Timbot:

	def __init__(self):
		self.client = SlackClient(os.environ['SLACK_API_TOKEN'])
		self.channel_id = os.environ['SLACK_CHANNEL_NAME']
		self.timbot_user_id = os.environ['SLACK_TIMBOT_USER_ID'].lower()

		self.ideal_lunch_time = "16:30"
		self.images_base_dir = "images"
		self.weekday_lunch_index = 4
		self.default_lunchcation = "epicurean feast"

		self.message_handler = {
			'openstack': self.openstack_message_handler,
			'pong': self.pong_message_handler,
		}

	def openstack_message_handler(self):
		self.send_message('I hear Openstack is a career killer')

	def pong_message_handler(self):
		self.send_message('I\'m in. Best 2 games out of 3?')

	def default_message_handler(self):
		self.send_message('keep pounding')

	def chose_message_handler(self, message):
		return self.message_handler[next(key for key in self.message_handler if key in message)]

	def get_channel_history(self):
		return self.client.api_call("group.history", channel=self.channel_id, count=1)

	def send_message(self, text):
		self.client.api_call('chat.postMessage', channel=self.channel_id, text=text, as_user=False)

	def send_lunch_time_notification(self):
		self.send_message("IT IS THE IDEAL LUNCH TIME GO TO LUNCH")

	def send_chat_image(self, image_name, image_url, title, text):
		if image_name is not None:
			filepath = os.path.join(self.images_base_dir, image_name)

			try:
				with open(filepath, 'rb') as f:
					resp = self.client.api_call(
						"files.upload",
						title='sampletitle',
						file=io.BytesIO(f.read()),
				)
			except IOError:
				print("Failed to open file: the path '{}' does not exist".format(filepath))
				return

			meta = resp['file']
			self.client.api_call("files.sharedPublicURL", file=meta['id'])
			attachments = [{"title": title, "image_url": meta['permalink_public']}]
		else:
			attachments = [{"title": title, "image_url": image_url}]

		resp = self.client.api_call("chat.postMessage", channel=self.channel_id, text=text, attachments=attachments, as_user=True)

	def handle_message(self, message):
		# base case: handle unrecognized input
		if 'lunch' not in message:
			self.default_message_handler()
			return

		if 'where' in message:
			if (datetime.datetime.today().weekday() == self.weekday_lunch_index) or 'no feast' in message:
				random.seed(datetime.datetime.now())
				self.send_message(helpers.choose_lunchcation())
			else:
				self.send_message(self.default_lunchcation)
		elif 'when' in message or 'time' in message:
			self.send_chat_image("lunchchart.png", '', 'IdealLunchTimeChart', self.ideal_lunch_time)
		elif 'what' in message and 'eat' in message:
			if datetime.datetime.today().weekday() == self.weekday_lunch_index:
				self.send_message('Its friday enjoy a meal out. Maybe some french toast at pauls?')
			else:
				self.send_chat_image('', 'http://cafe.epicureanfeast.com/Clients/8680redhat.jpg', 'Menu', 'May I suggest the chicken sandwich')

	def payload_handler(self, message):
		# check if the current message was in the form of '@timbot ...'
		# current problem: message is in the form of "<@ur9ha8kv2> hey"
		# note: DM history may be handled differently than channel history
		if message.startswith(self.timbot_user_id):
			self.handle_message(message)
		elif 'openstack' in message:
			self.send_message("I hear Openstack is a career killer")
		elif 'pong' in message:
			self.send_message("I\'m in. Best 2 out of 3 games to 7?")

	def run(self):
		timbot_user_id_striped = self.timbot_user_id.strip('<@>')

		while True:
			history = self.get_channel_history()

			if datetime.datetime.now().strftime('%H:%M') == self.ideal_lunch_time:
				self.send_lunch_time_notification()

			# wait until there are messages populated in the history dictionary
			if 'messages' not in history or len(history['messages']) == 0:
				time.sleep(1.5)

			for data in history['messages']:
				# check if the last message was from a user and not a bot
				# note: timbot is registered as a user and not a slack bot
				if 'text' not in data or 'bot_id' in data:
					continue

				sender = data['user'].encode('UTF8').lower()

				# ignore parsing any messages that were sent from timbot
				if sender == timbot_user_id_striped:
					continue

				self.payload_handler(data['text'].encode('UTF8').lower())


if __name__ == '__main__':
	timbot = Timbot()
	timbot.run()
