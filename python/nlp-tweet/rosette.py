import codecs
import json
import pprint
import time
import requests

url = 'https://api.rosette.com/rest/v1/entities'

headers = {
    'Content-Type': 'application/json',
    'X-RosetteAPI-Key': '6cc868dc04722856f894ba594182ed81',
}

with codecs.open('tweet.json', 'r', 'utf8') as fh:
    tweets = json.load(fh)

rosette = {}

for key, tweet in tweets.items():
    time.sleep(1)
    try:
        payload = {
            'content': tweet['text'].encode('utf-8')
        }
        res = requests.post(url, json=payload, headers=headers).json()
        rosette[key] = res
        print '%s processed' % key
    except Exception as e:
        print e
        continue

with codecs.open('rosette.json', 'w', 'utf8') as fh:
    json.dump(rosette, fh, indent=2)
