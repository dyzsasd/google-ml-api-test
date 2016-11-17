import codecs
import json
import pprint
import time
import requests

from python.datasets.daily import get_user_videos_from_file
from python.datasets.opencalais import OpenCalaisNlpDataset
from python.models.daily import Video

url = 'https://api.thomsonreuters.com/permid/calais'

headers = {
    'content-type': 'text/raw; charset=utf-8',
    'outputFormat': 'application/json',
    'x-ag-access-token': 'GXQIObbWfQHX0qv5KEOOxeoQHyDUKhS7',
    'x-calais-language': 'English',
}

# user_videos = get_user_videos_from_file("videos.json")
user_videos_new = get_user_videos_from_file("selected_videos.json")
user_videos = {'embed': []}
for it in user_videos_new:
    try:
        user_videos['embed'].append(Video(str(it["video_id"])).meta)
    except Exception:
        continue

opencalais_parser = OpenCalaisNlpDataset("")

for user, videos in user_videos.items():
    for video in videos:
        res = {}
        parsed_res={}
        try:
            r = requests.post(url, data=video['title'].encode('utf-8'), headers=headers).json()
            res['title'] = r
            parsed_res['title'] = opencalais_parser.clean_response(r)
            print 'processed %s title' % video['id']
        except Exception as e:
            print e

        try:
            r = requests.post(url, data=video['description'].encode('utf-8'), headers=headers).json()
            res['description'] = r
            parsed_res['description'] = opencalais_parser.clean_response(r)
            print 'processed %s description' % video['id']
        except Exception as e:
            print e

        try:
            r = requests.post(url, data=' '.join(video['tags']).encode('utf-8'), headers=headers).json()
            res['tags'] = r
            parsed_res['tags'] = opencalais_parser.clean_response(r)
            print 'processed %s tags' % video['id']
        except Exception as e:
            print e
        video['results'] = res
        video['parsed_results'] = parsed_res

with codecs.open('dailymotion-embed-opencalais.json', 'w', 'utf8') as fh:
    json.dump(user_videos, fh, indent=2)
