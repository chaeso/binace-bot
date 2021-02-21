import json
import requests
from pandas.io.json import json_normalize
from slacker import Slacker

json_slack_path: str = './slack_token.json'


class SlackSender:
    slack: Slacker

    def __init__(self):
        with open(json_slack_path, 'r') as json_file:
            slack_dict = json.load(json_file)

        slack_token = slack_dict['token']

        self.slack = Slacker(slack_token)

    def send_message(self, message: str):
        self.slack.chat.post_message("#test", message)


if __name__ == '__main__':
    slackSender: SlackSender = SlackSender()
    slackSender.send_message("HELLO WORLD!")
