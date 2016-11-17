import codecs
import json
import os
import urllib

from cached_property import cached_property
import dailymotion as dailymotion_api


class Channel(object):
    def __init__(self, channel_id):
        self.client = dailymotion_api.Dailymotion()
        self._id = channel_id

    @cached_property
    def meta(self):
        fields = ','.join([
            'tags', 'title', 'description', 'embed_html', 'channel.name'])
        return self.client.get('/channel/%s?fields=%s' % (self._id, fields))

    def get_videos(self, limit=10, sort='recent', **kwargs):
        args = kwargs or {}
        args.update({
            'limit': limit,
            'sort': sort,
            'fields': ','.join(['id', 'updated_time']),
        })
        query = urllib.urlencode(args, True)
        return self.client.get('/channel/%s/videos?%s' % (self._id, query))


class User(object):
    def __init__(self, user_id):
        self.client = dailymotion_api.Dailymotion()
        self._id = user_id

    @cached_property
    def meta(self):
        fields = ','.join([
            'username', 'description', 'website_url'])
        return self.client.get('/user/%s?fields=%s' % (self._id, fields))

    def get_video_ids(self, limit=10, sort='recent', **kwargs):
        args = kwargs or {}
        args.update({
            'limit': limit,
            'sort': sort,
            'fields': ','.join(['id', 'updated_time']),
        })
        query = urllib.urlencode(args, True)
        return self.client.get('/user/%s/videos?%s' % (self._id, query))

    def get_videos(self, limit=10):
        posted_videos = self.get_video_ids(limit=limit)['list']
        return [Video(video[u'id']) for video in posted_videos]


class Video(object):
    def __init__(self, video_id):
        self.client = dailymotion_api.Dailymotion()
        self._id = video_id

    @cached_property
    def meta(self):
        fields = ','.join([
            'id', 'tags', 'title', 'description', 'embed_html', 'owner.id', 'owner.username', 'language'])
        return self.client.get('/video/%s?fields=%s' % (self._id, fields))


class VideoMeta(object):
    _data = None

    def __init__(self, language='en-US'):
        self.id_file = id_file % language
        self.meta_file = meta_file % language

    @property
    def data(self):
        if self._data is None:
            self._load_data()
        return self._data

    def _load_data(self):
        if not os.path.exists(self.meta_file):
            self._get_metas()
        with codecs.open(self.meta_file, 'r', 'utf8') as meta_file_handle:
            self._data = json.load(meta_file_handle)

    def _get_metas(self):
        client = dailymotion_api.Dailymotion()
        metas = []
        with codecs.open(self.id_file, 'r', 'utf8') as id_file_handle:
            for video_id in id_file_handle.read().splitlines():
                if not video_id:
                    continue
                metas.append(client.get(
                    '/video/%s?fields=id,title,description' % video_id))
        with codecs.open(self.meta_file, 'w', 'utf8') as meta_file_handle:
            json.dump(metas, meta_file_handle)
