import argparse
import codecs
import json

from python.models.daily import Video, User

def generate_datasets(user_ids):
    user_videos = {}
    for _id in user_ids:
        videos = get_user_videos(_id)
        user_videos[_id] = videos
    return user_videos

def get_user_videos(user_id):
    user = User(user_id)
    return [
        video.meta for video in user.get_videos()
    ]

def get_user_videos_from_file(file_path):
    with codecs.open(file_path, 'r', 'utf8') as fh:
        return json.load(fh)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('user_file', type=str)
    parser.add_argument('output_file', type=str)
    args = parser.parse_args()

    user_ids = []

    with codecs.open(args.user_file, 'r', 'utf8') as fh:
        for line in fh.read().splitlines():
            items = line.split('\t')
            user_ids.append(items[0])

    user_videos = generate_datasets(user_ids)

    with codecs.open(args.output_file, 'w', 'utf8') as fh:
        json.dump(user_videos, fh, indent=2)
