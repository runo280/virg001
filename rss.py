import json
import time

import feedparser
import requests

import db


def get_topics():
    with open("feeds.txt", "r") as read_file:
        data = json.load(read_file)
    return data['topics']


def is_url_ok(url):
    try:
        r = requests.head(url)
        if r.status_code == 200:
            print('Url is OK: ' + url)
            return True
        else:
            print('StatusCode is {}: {} '.format(r.status_code, url))
            return True
    except requests.ConnectionError:
        print('Failed to connect: ' + url)
        return False


def read_article_feed(topic):
    if not is_url_ok(topic['url'].replace('/topic', '/feed/topic')):
        return
    try:
        feed = feedparser.parse(topic['url'].replace('/topic', '/feed/topic'))
        print('Count is ' + str(len(feed['entries'])))
        for article in feed['entries']:
            title = article['title']
            link = article['link']

            if 'published' in article:
                date = article['published']
            else:
                date = article['updated']

            if not is_article_in_db(link):
                add_article_to_db(title, link, date, topic['fa_name'], False)
    except:
        print()


def is_article_in_db(url):
    query = {'link': url}
    if db.feeds.count_documents(query) == 0:
        return False
    else:
        return True


def add_article_to_db(title, link, date, cat, is_pub):
    article = {'title': title, 'link': link, 'date': date, 'cat': cat, 'is_pub': is_pub}
    x = db.feeds.insert_one(article)
    print(x.inserted_id)


if __name__ == '__main__':
    items = get_topics()
    print('Feeds count: ' + str(len(items)))
    index = 0
    for item in items:
        index += 1
        print('Processing feed #' + str(index))
        read_article_feed(item)
        time.sleep(15)
