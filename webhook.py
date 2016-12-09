import os

import muffin
from slacker import Slacker

app = muffin.Application('webhook')
slack = Slacker(os.environ['SLACK_BOT_TOKEN'])
channel = os.environ['SLACK_CHANNEL']

USER_MAPPING = {
    # Github: Slack
    'aichane': 'anael',
}

def get_slack_username(username):
    """
    Get user from mapping GitHut/Slack, when the GitHub username is
    different from the Slack one.

    >>> get_slack_username('aichane')
    '@anael'
    >>> get_slack_username('wo0dyn')
    '@wo0dyn'

    """
    return '@{username}'.format(username=USER_MAPPING.get(username, username))


templates = {
    '+label:"3 - Reviewing"': '<{url}|{pr} (#{number})> is now ready for _review_!{ping}',
    '-label:"3 - Reviewing"': '<{url}|{pr} (#{number})> is now ready for _merge_!{ping}',
    '+label:"4 - Testing"': '<{url}|{pr} (#{number})> is now ready for test!{ping}',
    'default': '{username} just {action} label “{label}” to <{url}|{pr} (#{number})>.',
}


@app.register('/payload')
class Webhook(muffin.Handler):
    """
    Simple Webhook to catch GitHub Pull Request changes on labels.

    """

    def post(self, request):
        payload = yield from request.json()

        if 'labeled' in payload['action']:
            params = {
                'action': 'added' if payload['action'] == 'labeled' else 'removed',
                'assignees': ' '.join(
                    get_slack_username(assignee['login'])
                    for assignee in payload['pull_request']['assignees']),
                'label': payload['label']['name'],
                'number': payload['pull_request']['number'],
                'ping': '',
                'pr': payload['pull_request']['title'],
                'url': payload['pull_request']['html_url'],
                'username': get_slack_username(payload['sender']['login']),
            }

            if params['assignees']:
                params['ping'] = ' • ping {assignees}'.format(
                    assignees=params['assignees'])

            rule = '{sign}label:"{label}"'.format(
                sign='+' if params['action'] == 'added' else '-',
                label=params['label'])

            message = templates.get(rule, templates['default']).format(**params)

            slack.chat.post_message(channel, message, username='PeopleAskBot',
                icon_emoji=':peopleask:')

            return message

        return None


if __name__ == '__main__':
    app.manage()
