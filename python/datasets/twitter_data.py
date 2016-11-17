import codecs
import json
import os
import time

from twitter import *


_root_path = os.path.dirname(os.path.realpath(__file__)) + '/../..'

id_file = (
    _root_path +
    '/data/nlp/benchmark/en-US/neel' +
    '/microposts2016-neel-training-tweets-ids.tsv'
)

tweets_file = (
    _root_path +
    '/data/nlp/benchmark/en-US/neel' +
    '/tweets.json'
)

settings = {
    'oauth_access_token': "112545403-e5WXEiTz6pgC9teinMC3aQScee8eJ02tKuw3ys54",
    'oauth_access_token_secret': "gwfEIQqTFDY42NncABqD6nuAVR0woxcF9EQgjeWO2DmsP",
    'consumer_key': "jkFqoo1LZ8HYLOTSq8TdClXJ3",
    'consumer_secret': "siuFdr9ijwcdroiDwujiywFVWUfpYhp7df3cN5UTyo5HwTg2Cj"
}

t = Twitter(auth=OAuth(
    settings['oauth_access_token'],
    settings['oauth_access_token_secret'],
    settings['consumer_key'],
    settings['consumer_secret']
))

tweets = []

with codecs.open(id_file) as id_file_handle:
    for tweet_id in id_file_handle.read().splitlines():
        retry = 0
        while True:
            retry = retry + 1
            try:
                res = t.statuses.show(_id=tweet_id)
                with codecs.open(tweets_file, 'a', 'utf8') as tweets_file_handle:
                    tweets_file_handle.write(json.dumps(res) + '\n')
                time.sleep(2)
                print 'saved tweet of %s' % tweet_id
                break
            except Exception as e:
                print "%s fetch failed in retry = %s" % (tweet_id, retry)
                time.sleep(10)
                if retry < 3:
                    continue
                else:
                    break
