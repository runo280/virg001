# -*- coding: utf-8 -*-

import db
import telegram

if __name__ == '__main__':

    unpublished_query = {'is_pub': False}
    set_published_query = {'$set': {'is_pub': True}}
    for x in db.feeds.find(unpublished_query):
        title = x['title']
        link = x['link']
        date = x['date']
        cat = '#' + x['cat'].replace(' ', '_')
        send = telegram.send_article(title, link, cat, date)
        result = send.json()
        print(result)
        if result['ok'] is True:
            print('ok')
            db.feeds.update_one({'link': link}, set_published_query)
        else:
            print('failed to publish')
