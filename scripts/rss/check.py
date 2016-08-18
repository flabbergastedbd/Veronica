import os
import json
import time

import feedparser
import tornado.template

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

FEED_URL = "http://www.thehindu.com/news/?service=rss"
FEED_COUNT = 30

f = feedparser.parse(FEED_URL)
feeds = []

for feed in f['entries'][0:FEED_COUNT]:
    feeds.append({
        'title': feed['title'],
        'published': time.strftime("%a %H:%M", feed['published_parsed']),
        'summary': feed['summary']
    })

with open(os.path.join(ROOT_DIR, 'rss_log.html'), 'r') as fp:
    print(tornado.template.Template(fp.read()).generate(feeds=json.dumps(feeds)))
