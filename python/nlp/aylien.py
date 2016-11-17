import codecs
import json
import pprint
import time
import requests

url = 'https://api.aylien.com/api/v1/entities'

headers = {
    "X-AYLIEN-TextAPI-Application-Key": "f7a479909e02c05863773dd5bfa15303",
    "X-AYLIEN-TextAPI-Application-ID": "58fb7b2b",
}

with codecs.open('tweet.json', 'r', 'utf8') as fh:
    tweets = json.load(fh)

aylien = {}

for key, tweet in tweets.items():
    time.sleep(1)
    try:
        res = requests.post(url, data={'text': tweet['text'].encode('utf-8')}, headers=headers).json()
        aylien[key] = res
        print '%s processed' % key
    except Exception as e:
        print e
        continue

with codecs.open('aylien.json', 'w', 'utf8') as fh:
    json.dump(aylien, fh, indent=2)
