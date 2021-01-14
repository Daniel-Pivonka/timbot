import pytest
from unittest.mock import patch
import datetime
from src import timbot


class FakeSlackClient:
    def __init__(self, fake_api_call):
        self.fake_api_call = fake_api_call

    def api_call(self, *args, **kwargs):
        return self.fake_api_call()


class TestTimbot:
    def init_vars(self, cid="test-channel", uid="@timbot",
                  uid_stripped="timbot", uae=True):
        timbot.channel_id = cid
        timbot.timbot_user_id = uid
        timbot.timbot_user_id_stripped = uid_stripped
        timbot.use_authenticated_user = uae

    patch("timbot.send_message")

    def test_openstack(self):
        timbot.sc = FakeSlackClient(
            lambda: {"messages": [{"user": "me", "text":
                     "openstack is the best"}]})
        self.init_vars()
        timbot.send_message = lambda arg: (_ for _ in ()).throw(Exception(arg))
        with pytest.raises(Exception) as e:
            timbot.run_timbot()
        assert str(e.value) in ["i hear openstack and cephadm are career killers"]

    patch("timbot.send_message")

    def test_pong(self):
        timbot.sc = FakeSlackClient(lambda: {"messages": [{"user": "me",
                                                           "text":
                                             "play some pong?"}]})
        self.init_vars()
        timbot.send_message = lambda arg: (_ for _ in ()).throw(Exception(arg))
        with pytest.raises(Exception) as e:
            timbot.run_timbot()
        assert str(e.value) in ["im in. best 2 out of 3 games to 7?"]

    patch("timbot.send_message")

    def test_where_lunch(self):
        self.init_vars()
        timbot.send_message = lambda arg: (_ for _ in ()).throw(Exception(arg))

        # guarantee not Friday
        timbot.friday_index_elem = -1

        timbot.sc = FakeSlackClient(lambda: {"messages": [{"user": "me",
                                                           "text":
                                                           "@timbot where "
                                                           "lunch no feast"
                                                           }
                                                          ]
                                             })
        with pytest.raises(Exception) as e:
            timbot.run_timbot()
        assert str(e.value) in ['pauls', 'asian plus', 'moes',
                                'the 99', 'chilis']

        timbot.sc = FakeSlackClient(lambda: {"messages": [{"user": "me",
                                                           "text":
                                             "@timbot where lunch"}]})
        with pytest.raises(Exception) as e:
            timbot.run_timbot()
        assert str(e.value) in ['epicurean feast']

        # make it Friday
        timbot.friday_index_elem = datetime.datetime.today().weekday()

        timbot.sc = FakeSlackClient(lambda: {"messages": [{"user": "me",
                                                           "text":
                                             "@timbot where lunch"}]})
        with pytest.raises(Exception) as e:
            timbot.run_timbot()
        assert str(e.value) in ['pauls', 'asian plus', 'moes',
                                'the 99', 'chilis']

    patch("timbot.send_message")

    def test_when_lunch(self):
        self.init_vars()
        timbot.send_message = lambda arg: (_ for _ in ()).throw(Exception(arg))

        timbot.sc = FakeSlackClient(lambda: {"messages": [{"user": "me",
                                                           "text":
                                             "@timbot when lunch"}]})
        with pytest.raises(Exception) as e:
            timbot.run_timbot()
        assert str(e.value) in [timbot.utc_to_est("16:30")]

        timbot.sc = FakeSlackClient(lambda: {"messages": [{"user": "me",
                                                           "text":
                                             "@timbot lunch time"}]})
        with pytest.raises(Exception) as e:
            timbot.run_timbot()
        assert str(e.value) in [timbot.utc_to_est("16:30")]

    patch("timbot.send_message")

    def test_what_lunch(self):
        self.init_vars()
        timbot.send_message = lambda arg: (_ for _ in ()).throw(Exception(arg))

        # guarantee not Friday
        timbot.friday_index_elem = -1

        timbot.sc = FakeSlackClient(lambda: {"messages": [{"user": "me",
                                                           "text":
                                             "@timbot what lunch"}]})
        with pytest.raises(Exception) as e:
            timbot.run_timbot()
        assert str(e.value) in ['may I suggest the chicken sandwich']

        timbot.sc = FakeSlackClient(lambda: {"messages": [{"user": "me",
                                                           "text":
                                             "@timbot what eat"}]})
        with pytest.raises(Exception) as e:
            timbot.run_timbot()
        assert str(e.value) in ['may I suggest the chicken sandwich']

        # make it Friday
        timbot.friday_index_elem = datetime.datetime.today().weekday()

        timbot.sc = FakeSlackClient(lambda: {"messages": [{"user": "me",
                                                           "text":
                                             "@timbot what lunch"}]})
        with pytest.raises(Exception) as e:
            timbot.run_timbot()
        assert str(e.value) in ['Its friday enjoy a meal out. '
                                'Maybe some french toast at pauls?']

        timbot.sc = FakeSlackClient(lambda: {"messages": [{"user": "me",
                                                           "text":
                                             "@timbot what eat"}]})
        with pytest.raises(Exception) as e:
            timbot.run_timbot()
        assert str(e.value) in ['Its friday enjoy a meal out. Maybe some '
                                'french toast at pauls?']

    patch("timbot.db.increment_webopoly_wins")
    patch("timbot.send_message")

    def test_increment_webopoly_wins(self):
        self.init_vars()
        timbot.conn = ""

        def iww_func(_, name):
            (_ for _ in ()).throw(Exception(name))
        timbot.db.increment_webopoly_wins = iww_func
        timbot.send_message = lambda arg: (_ for _ in ()).throw(Exception(arg))

        timbot.sc = FakeSlackClient(lambda: {"messages": [{"user": "me",
                                                           "text":
                                                           "@timbot increment"
                                                           " webopoly "
                                             "win Jeff"}]})
        with pytest.raises(Exception) as e:
            timbot.run_timbot()
        assert str(e.value) in ["Couldn't do it cause jeff"]

    patch("timbot.db.get_webopoly_standings")
    patch("timbot.send_message")

    def test_show_webopoly_standings(self):
        self.init_vars()
        timbot.conn = ""
        standings = [["Webopoly-king", 75], ["Webopoly-prince", 54],
                     ["Webopoly-knight", 37], ["Webopoly-peasant", 2]]
        timbot.db.get_webopoly_standings = lambda _: standings
        timbot.send_message = lambda arg: (_ for _ in ()).throw(Exception(arg))

        timbot.sc = FakeSlackClient(lambda: {"messages": [{"user": "me",
                                             "text": "@timbot show webopoly "
                                                           "standings"}]})
        with pytest.raises(Exception) as e:
            timbot.run_timbot()
        assert str(e.value) in ["Webopoly-king is the reigning champ with "
                                "75 wins\n"
                                "Webopoly-prince is next with 54 wins\n"
                                "Webopoly-knight is next with 37 wins\n"
                                "And in last is loser Webopoly-peasant with 2 "
                                "wins"]

    patch("timbot.send_message")

    def test_help(self):
        timbot.sc = FakeSlackClient(lambda: {"messages": [{"user": "me",
                                             "text": "@timbot help me"}]})
        self.init_vars()
        timbot.send_message = lambda arg: (_ for _ in ()).throw(Exception(arg))
        with pytest.raises(Exception) as e:
            timbot.run_timbot()
        assert str(e.value) in [timbot.help_text]

    patch("timbot.send_message")

    def test_pounding(self):
        timbot.sc = FakeSlackClient(lambda: {"messages": [{"user": "me",
                                             "text": "@timbot what now?"}]})
        self.init_vars()
        timbot.send_message = lambda arg: (_ for _ in ()).throw(Exception(arg))
        with pytest.raises(Exception) as e:
            timbot.run_timbot()
        assert str(e.value) in ["keep pounding"]

    patch("timbot.send_message")

    def test_ideal_lunch_time(self, capsys):
        timbot.sc = FakeSlackClient(lambda: {"nothing": []})
        self.init_vars()
        timbot.send_message = lambda arg: (_ for _ in ()).throw(Exception(arg))

        # guarantee not weekend
        timbot.saturday_index_elem = -1
        timbot.sunday_index_elem = -1

        # make it ideal lunch time
        timbot.ideal_lunch_time = datetime.datetime.now().strftime('%H:%M')

        # set alert to True (means ideal lunch time message hasn't been sent)
        timbot.handle_ideal_lunch_time.alert = True

        with pytest.raises(Exception) as e:
            timbot.run_timbot()
        assert str(e.value) in ["IT IS THE IDEAL LUNCH TIME GO TO LUNCH"]

        # make it not ideal lunch time
        timbot.ideal_lunch_time = "fake time"

        timbot.run_timbot()
        captured = capsys.readouterr()
        assert captured.out == "[DEBUG]: no logs in history, sleeping...\n"
