import json
import re
from urlparse import urlparse


class AbstractNlpDataset(object):

    def __init__(self, filepath):
        self.filepath = filepath

    @classmethod
    def load_dataset(cls, filepath):
        return json.load(open(filepath))

    @classmethod
    def parse_provider_urls(cls, urls):
        """Parse urls to extract provider (ex.: wikipedia) to url map.
            Keeps only en.wikipedia if multiple
        """
        res = {}
        parsed = {
            _url: urlparse(_url) for _url in urls
        }
        for _url, parsed in parsed.iteritems():
            matched = re.match(r"(?P<prefix>[a-zA-Z0-9]+)\.(?P<domain>.*)\.[a-zA-Z0-9]+", parsed.netloc)
            if matched:
                matched_dict = matched.groupdict()
                if matched_dict["domain"] == 'wikipedia' and matched_dict["prefix"] != 'en':
                    continue
                res[matched_dict["domain"]] = _url
        return res

    def map_dataset(self):
        initial_dataset = self.load_dataset(self.filepath)
        return {
            _id: self.clean_response(_resp)
            for _id, _resp in initial_dataset.iteritems()
        }

    def clean_response(self, response):
        """Clean api response.

        :param resp: the api response.
        :type resp: dict
        :returns: the mapped response with fields:
            n_entities, n_nonNIL_entities,
            entities (keys: start, end, urls (keys: dbpedia, wikidata, ...), graph_ids (keys: dbpedia, wikidata, ...), topic_text),
            optionals: text, n_implicit_entities
        :rtypes: dict
        """
        raise NotImplementedError("Should be implemented in children classes.")
