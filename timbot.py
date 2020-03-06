import io
import os
import random
import datetime
from slackclient import SlackClient

slack_token = os.environ['SLACK_API_TOKEN']
channel_name = os.environ['SLACK_CHANNEL_NAME']
timbot_user_id = os.environ['SLACK_TIMBOT_USER_ID'].lower()
timbot_user_id_striped = timbot_user_id.strip('<@>')

sc = SlackClient(slack_token)

ideal_lunch_time = "16:30"
friday_index_elem = 4
saturday_index_elem = 5
sunday_index_elem = 6
help_text = '''
    You can ask me the following:
    `where lunch`: i tell you where to eat lunch
    `where lunch no feast`: i tell you where to eat lunch that isn't epicurean feast
    `when lunch/lunch time`: i tell you when to eat lunch
    `what lunch/what eat`: i tell you what to eat
    `help`: this
'''


def main():
    while True:
        run_timbot()


def utc_to_est(utc_time):
    return str((int(utc_time[:2]) - 5) % 24) + ':' + utc_time[-2:]


def send_message(text):
    sc.api_call("chat.postMessage", channel=channel_name, text=text, as_user=True)


def handle_ideal_lunch_time(curr_time):
    if curr_time == ideal_lunch_time:
        if handle_ideal_lunch_time.alert:
            send_message('IT IS THE IDEAL LUNCH TIME GO TO LUNCH')
        handle_ideal_lunch_time.alert = False
    else:
        handle_ideal_lunch_time.alert = True


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


def choose_lunchcation():
    return "the 99"


def run_timbot():
    history = sc.api_call("groups.history", channel=channel_name, count=1)

    # handle ideal lunch time if it is a weekday
    if datetime.datetime.today().weekday() not in [saturday_index_elem, sunday_index_elem]:
        handle_ideal_lunch_time(datetime.datetime.now().strftime('%H:%M'))

    # look for a message in the chat that starts with '@timbot .....'
    if 'messages' in history:
        for data in history['messages']:
            if 'text' in data and 'user' in data:

                message = data['text'].encode('UTF8').lower()
                sender = data['user'].encode('UTF8').lower()

                # check if timbot is sender
                if sender != timbot_user_id_striped:

                    # openstack meme
                    if 'openstack' in message:
                        send_message('i hear openstack is a career killer')

                    # pong responce
                    elif 'pong' in message:
                        send_message('im in. best 2 out of 3 games to 7?')

                    if message.startswith(timbot_user_id):

                        # message now equals what was after '@timbot'
                        message = message.replace(timbot_user_id, '')

                        # where to go to lunch
                        if 'lunch' in message and 'where' in message:

                            # if friday or "no feast" override included in message
                            if (datetime.datetime.today().weekday() == friday_index_elem) or ("no feast" in message):
                                random.seed(datetime.datetime.now())

                                # choose place to go
                                choice = choose_lunchcation()
                                send_message(choice)

                            # mon-thur
                            else:
                                send_message('epicurean feast')

                        # what time is lunch
                        elif ('lunch' in message) and ('time' in message or 'when' in message):
                            send_message(utc_to_est(ideal_lunch_time))
                            uploadimage('images/lunchchart.png', 'IdealLunchTimeChart', '')

                        # what to eat
                        elif ('what' in message) and ('eat' or 'lunch' in message):
                            # if friday
                            if datetime.datetime.today().weekday() == friday_index_elem:
                                send_message('Its friday enjoy a meal out. Maybe some french toast at pauls?')
                            else:
                                image_url = 'http://cafe.epicureanfeast.com/Clients/8680redhat.jpg'
                                attachments = [{"title": 'Menu', "image_url": image_url}]
                                sc.api_call("chat.postMessage", channel=channel_name, text='Heres the cafe menu', as_user=True, attachments=attachments)
                                send_message("may I suggest the chicken sandwich")

                        elif 'help' in message:
                            send_message(help_text)

                        # base response
                        else:
                            send_message('keep pounding')

                # openstack meme (temp fix)
                elif 'openstack' in message and message != 'i hear openstack is a career killer':
                    send_message('i hear openstack is a career killer')

                # pong response (temp fix)
                elif 'pong' in message:
                    send_message('im in. best 2 out of 3 games to 7?')


if __name__ == '__main__':
    main()
