GitHub Playground
=================

.. code:: console

    $ export SLACK_BOT_TOKEN='xoxp-3xxxxxx'
    $ ngrok http 5000  # To expose the local server publicly
    $ python webhook.py run  # default port: 5000
    # To kill the server:
    $ ps aux | grep webhook.py | grep -v grep | awk '{print $2}' | xargs kill -9
