import codecs
import json
import pprint
import time
import requests

url = 'https://svc02.api.bitext.com/entities/'

headers = {
  "Authorization": "bearer 885a77761db04b8b8f7bfcc0ef333296",
  "Content-Type": "application/json"
}

def base_data():
    return {
        'language': 'eng',
    }

with codecs.open('tweet.json', 'r', 'utf8') as fh:
    tweets = json.load(fh)

bitext = {}

for key, tweet in tweets.items():
    time.sleep(1)
    try:
        data = base_data()
        data['text'] = tweet['text'].encode('utf-8')
        print data
        res = requests.post(url, data=json.dumps(data), headers=headers).json()
        bitext[key] = res
        print res
        break
        print '%s processed' % key
    except Exception as e:
        print e
        continue

with codecs.open('bitext.json', 'w', 'utf8') as fh:
    json.dump(bitext, fh, indent=2)
