import codecs
import json
import pprint
import time
import requests

from python.dataset.daily import get_user_videos

url = 'https://api.thomsonreuters.com/permid/calais'

headers = {
    'content-type': 'text/raw; charset=utf-8',
    'outputFormat': 'application/json',
    'x-ag-access-token': 'GXQIObbWfQHX0qv5KEOOxeoQHyDUKhS7',
    'x-calais-language': 'English',
}

with codecs.open('tweet.json', 'r', 'utf8') as fh:
    tweets = json.load(fh)

user_videos = get_user_videos("videos.json")

opencalais = {}

for key, tweet in tweets.items():
    time.sleep(1)
    try:
        res = requests.post(url, data=tweet['text'].encode('utf-8'), headers=headers).json()
        opencalais[key] = res
    except Exception as e:
        print e
        continue

with codecs.open('dailymotion-opencalais.json', 'w', 'utf8') as fh:
    json.dump(opencalais, fh, indent=2)
