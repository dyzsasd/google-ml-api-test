import codecs
import json
import pprint
import time
import requests

url = 'https://api.meaningcloud.com/topics-2.0'

def base_data():
    return {
        'key': 'c0382b3360117a9ab83b1b613bb8e4d6',
        'lang': 'en',
        'tt': 'a'
    }

with codecs.open('tweet.json', 'r', 'utf8') as fh:
    tweets = json.load(fh)

meaningcloud = {}

for key, tweet in tweets.items():
    time.sleep(1)
    data = base_data()
    data['txt'] = tweet['text'].encode('utf-8')
    try:
        res = requests.post(url, data=data).json()
        meaningcloud[key] = res
        print '%s processed' % key
    except Exception as e:
        print e
        continue

with codecs.open('meaningcloud.json', 'w', 'utf8') as fh:
    json.dump(meaningcloud, fh, indent=2)
