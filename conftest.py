# need to get past slackclient import in pytests by making fake
# slackclient module

import sys


class slackclient:

    class SlackClient:
        def __init__(token):
            token = token


module = type(sys)('slackclient')
module.SlackClient = slackclient.SlackClient
sys.modules['slackclient'] = module
