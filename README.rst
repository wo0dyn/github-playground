GitHub Playground
=================

Tiny bot that post messages on Slack when label are modified on a pull
request.

Install
-------

.. code:: console

    $ mkproject --python=$(which python3.4) GithubPlayground
    $ git clone git@github.com:wo0dyn/github-playground
    $ pip install -r requirements.txt
    $ ${EDITOR-vi} $VIRTUAL_ENV/bin/postactivate
    # add these vars:
    # export SLACK_BOT_TOKEN='xoxp-3xxxxxx'
    # export SLACK_CHANNEL='#github-playground'
    # Reload the env
    $ deactivate && workon GithubPlayground


Launch the server
-----------------

.. code:: console

    $ ngrok http 5000                    # To expose the local server publicly
    $ python webhook.py run              # default port: 5000


Kill the server
---------------

.. code:: console

    $ ps aux | grep webhook.py | grep -v grep | awk '{print $2}' | xargs kill -9
