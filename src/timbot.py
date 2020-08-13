import io
import os
import sys
import time
import random
import datetime
import numpy as np
import database as db
import mysql.connector
from slackclient import SlackClient


ideal_lunch_time = "15:30"
friday_index_elem = 4
saturday_index_elem = 5
sunday_index_elem = 6
help_text = '''
    You can ask me the following:
    `where lunch`: i tell you where to eat lunch
    `where lunch no feast`: i tell you where to eat lunch that isn't epicurean feast
    `when lunch/lunch time`: i tell you when to eat lunch
    `what lunch/what eat`: i tell you what to eat
    `increment weboploy win <name>`: more glory to whoever <name> is
    `show webopoly standings`: show who is captalist king and who is poor
    `help`: this
'''


# TODO: Change this to handle daylight savings
def utc_to_est(utc_time):
    return str((int(utc_time[:2]) - 5) % 24) + ':' + utc_time[-2:]


def send_message(text):
    sc.api_call("chat.postMessage", channel=channel_id, text=text, as_user=use_authenticated_user)


def handle_ideal_lunch_time(curr_time):
    if curr_time == ideal_lunch_time:
        if handle_ideal_lunch_time.alert:
            send_message('IT IS THE IDEAL LUNCH TIME GO TO LUNCH')
        handle_ideal_lunch_time.alert = False
    else:
        handle_ideal_lunch_time.alert = True


def uploadimage(path, title, text):
    with open(path, 'rb') as f:
        response = sc.api_call(
            "files.upload",
            title='sampletitle',
            file=io.BytesIO(f.read())
        )
    fileinfo = response['file']
    sc.api_call("files.sharedPublicURL", file=fileinfo['id'])
    image_url = fileinfo['permalink_public']
    attachments = [{"title": title, "image_url": image_url}]
    response = sc.api_call("chat.postMessage", channel=channel_id, text=text, as_user=use_authenticated_user, attachments=attachments)


def choose_lunchcation():
    places = ['pauls', 'asian plus', 'moes', 'the 99', 'chilis']
    weights = [0.5, 0.3, 0.1, 0.05, 0.05]
    choice = np.random.choice(places, p=weights)
    return choice


def handle_timbot_message(message):
    # where to go to lunch
    if 'lunch' in message and 'where' in message:
        # if friday or "no feast" override included in message
        if (datetime.datetime.today().weekday() == friday_index_elem) or ("no feast" in message):
            random.seed(datetime.datetime.now())
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
            sc.api_call("chat.postMessage", channel=channel_id, text='Heres the cafe menu', as_user=use_authenticated_user, attachments=attachments)
            send_message("may I suggest the chicken sandwich")

    # increment weboploy win
    elif 'increment weboploy win' in message:
        name = message.split()[-1]
        try:
            db.increment_weboploy_wins(conn, name)
        except Exception as e:
            send_message("Couldn't do it cause {}".format(e))

    # webopoly standings
    elif 'show webopoly standings' in message:
        raw_standings = db.get_webopoly_standings(conn)
        standings = "{} is the reigning champ with {} wins".format(raw_standings[0][0], raw_standings[0][1])
        for record in raw_standings[1:-1]:
            standings += "\n{} is next with {} wins".format(record[0], record[1])
        standings += "\nAnd in last is loser {} with {} wins".format(raw_standings[-1][0], raw_standings[-1][1])
        send_message(standings)

    elif 'help' in message:
        send_message(help_text)

    # base response
    else:
        send_message('keep pounding')


def run_timbot():
    history = sc.api_call("groups.history", channel=channel_id, count=1)

    # handle ideal lunch time if it is a weekday
    if datetime.datetime.today().weekday() not in [saturday_index_elem, sunday_index_elem]:
        handle_ideal_lunch_time(datetime.datetime.now().strftime('%H:%M'))

    # check if there's any messages in the channel history
    # if not, sleep for two seconds and continue polling
    if 'messages' not in history:
        print('[DEBUG]: no logs in history, sleeping...')
        time.sleep(2)
        return

    for data in history['messages']:
        if 'text' not in data or 'user' not in data:
            continue

        sender = data['user'].encode('UTF8').lower()
        if sender == timbot_user_id_striped:
            print('[DEBUG] last message was from the timbot_user_id, continuing to next loop iteration')
            continue

        message = data['text'].encode('UTF8').lower()

        # openstack meme
        if 'openstack' in message:
            send_message('i hear openstack is a career killer')

        # pong response
        if 'pong' in message:
            send_message('im in. best 2 out of 3 games to 7?')

        # look for a message in the chat that starts with '@timbot .....'
        if message.startswith(timbot_user_id):
            handle_timbot_message(message.replace(timbot_user_id, ''))


def main():
    while True:
        run_timbot()


if __name__ == '__main__':
    slack_token = os.environ['SLACK_API_TOKEN']
    channel_id = os.environ['SLACK_CHANNEL_ID']
    timbot_user_id = os.environ['SLACK_TIMBOT_USER_ID'].lower()
    timbot_user_id_striped = timbot_user_id.strip('<@>')
    sc = SlackClient(slack_token)

    use_authenticated_user = True
    dev_mode = os.environ.get('TIMBOT_USE_DEV_MODE', False)
    if dev_mode:
        use_authenticated_user = False

    # connect to database
    try:
        conn = mysql.connector.connect(user=os.environ['SQL_USER'],
                                       password=os.environ['SQL_PASSWORD'],
                                       host=os.environ['SQL_HOST'],
                                       database=os.environ['SQL_DATABASE'])
    except (KeyError, mysql.connector.Error) as e:
        print("Encountered an error: {}".format(e))
        sys.exit(1)

    main()
