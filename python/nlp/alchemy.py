import codecs
import json
import pprint
import time
import requests

url = 'https://gateway-a.watsonplatform.net/calls/url/URLGetRankedNamedEntities'

with codecs.open('tweet.json', 'r', 'utf8') as fh:
    tweets = json.load(fh)

def base_data():
    return {
        'apikey': '3941a89d992332fb3106e83f580465b97b1109f4',
    }

for key, tweet in tweets.items():
    time.sleep(1)
    try:
        res = requests.post(url, data=tweet['text'].encode('utf-8'), headers=headers).json()
        alchemy[key] = res
    except Exception as e:
        print e
        continue

with codecs.open('alchemy.json', 'w', 'utf8') as fh:
    json.dump(alchemy, fh, indent=2)
