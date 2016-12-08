import json
import os

import muffin

from slacker import Slacker

app = muffin.Application('webhook')
slack = Slacker(os.environ['SLACK_BOT_TOKEN'])

USER_MAPPING = {
    # Github: Slack
    'aichane': 'anael',
    'wo0dyn': 'wo0dyn',
}


@app.register('/payload')
class Webhook(muffin.Handler):
    """
    Simple Webhook to catch GitHub Pull Request changes on labels.

    """

    def post(self, request):
        payload = yield from request.json()

        if 'labeled' in payload['action']:
            username = payload['sender']['login']

            action = 'added' if payload['action'] == 'labeled' else 'removed'

            template = '@{username} just {action} label “{label}” to “{pr}” <{url}>'

            message = template.format(
                username=USER_MAPPING.get(username, username),
                action=action,
                label=payload['label']['name'],
                pr=payload['pull_request']['title'],
                url=payload['pull_request']['html_url'],
            )

            slack.chat.post_message('#github-playground', message)

            return message

        return None


if __name__ == '__main__':
    app.manage()
