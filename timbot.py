import io
import os
import sys
import yaml
import random
import datetime
import numpy as np
import database as db
import mysql.connector
from slackclient import SlackClient
from mysql.connector import errorcode

slack_token = os.environ['SLACK_API_TOKEN']
channel_name = os.environ['SLACK_CHANNEL_NAME']
timbot_user_id = os.environ['SLACK_TIMBOT_USER_ID'].lower()
timbot_user_id_striped = timbot_user_id.strip('<@>')

sc = SlackClient(slack_token)

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
    `show webopoly standings`: show who is captalist king and who is poor
    `help`: this
'''


def main():
    while True:
        run_timbot()


# TODO: Change this to handle daylight savings
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
    places = ['pauls', 'asian plus', 'moes', 'the 99', 'chilis']
    weights = [0.5, 0.3, 0.1, 0.05, 0.05]
    choice = np.random.choice(places, p=weights)
    return choice


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

                        # webopoly standings
                        elif 'show webopoly standings' in message:
                            raw_standings = db.getWebopolyStandings(conn)
                            standings = "{} is the reigning champ with {} wins".format(raw_standings[0][0], raw_standings[0][1])
                            for record in raw_standings[1:-1]:
                                standings += "\n{} is next with {} wins".format(record[0], record[1])
                            standings += "And in last is loser {} with {} wins".format(raw_standings[-1][0], raw_standings[-1][1])
                            send_message(standings)

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

    # load configuration data
    try:
        with open('config.yaml', 'r') as file:
            config = yaml.load(file)
    except Exception as e:
        print("Error loading configuration data: ", e)
        sys.exit()

    # connect to database
    try:
        conn = mysql.connector.connect(user=config['mysql']['user'],
                                       password=config['mysql']['password'],
                                       host=config['mysql']['host'],
                                       database=config['mysql']['database'])

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        sys.exit()

    else:
        main()
