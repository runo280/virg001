import os

import requests

bot_token = os.environ['bot_token']
channel_id = os.environ['channel_id']


def send_article(title, link, cat, date):
    message = '{cat}\n\n<a href="{link}">{title}</a>\n\n<pre>{date}</pre>\n' \
        .format(cat=cat, title=title, link=link, date=date)
    return requests.post(
        url='https://api.telegram.org/bot{0}/{1}'.format(bot_token, 'sendMessage'),
        data={'chat_id': channel_id, 'text': message, 'parse_mode': 'HTML'}
    )
