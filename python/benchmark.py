import codecs
import json
import pprint
import re

from python.datasets.textrazor import TextrazorDataset
from python.datasets.rosette import RosetteDataset
from python.datasets.meaningcloud import MeaningCloudNlpDataset
from python.datasets.opencalais import OpenCalaisNlpDataset


def extract_topic(url):
    try:
        words = re.match('http://dbpedia.org/resource/(.*)', url).group(1).split("_")
    except AttributeError:
        return url
    return " ".join(words)


def make_dataset(old):
    return {
        _id: {
            u"text": _tweet[u"text"],
            u"n_entities": len(_tweet.get(u"entities", [])),
            u"n_nonNIL_entities": len([1 for it in _tweet.get(u"entities", []) if it["url"].startswith("NIL")]),
            u"entities": [
                {
                    u"start": _entity[u"start"],
                    u"end": _entity[u"end"],
                    u"url": _entity[u"url"],
                    u"topic_text": extract_topic(_entity[u"url"]),
                } for _entity in _tweet.get(u"entities", [])
            ]
        }
        for _id, _tweet in old.iteritems()
    }

tweet = make_dataset(json.load(codecs.open('tweet.json', 'r', 'utf8')))

textrazor = TextrazorDataset('textrazor.json').map_dataset()
rosette = RosetteDataset('rosette.json').map_dataset()
meaningcloud = MeaningCloudNlpDataset('meaningcloud.json').map_dataset()
opencalais = OpenCalaisNlpDataset('opencalais.json').map_dataset()

def compare_topic_alias(reference_topic, topic):
    reference_token = "".join(re.findall(r'[a-zA-Z]+', reference_topic))
    token = "".join(re.findall(r'[a-zA-Z]+', topic))
    return reference_token == token

def compare(reference_entity, entity, strict=False):
    matched = False
    if entity['start'] == reference_entity['start'] and entity['end'] == reference_entity['end']:
        matched = True
    if compare_topic_alias(entity['topic_text'], reference_entity['topic_text']):
        matched = True
    if not strict:
        return matched

def compare_result(test_dataset):
    matched_entity_count = {}

    for key, reference_sample in tweet.items():
        if key not in test_dataset or len(reference_sample['entities']) == 0:
            continue
        sample = test_dataset[key]
        total_topic = 0
        count_matched = 0
        for reference_entity in reference_sample['entities']:
            if reference_entity['url'].startswith('NIL'):
                continue
            total_topic += 1
            for entity in sample['entities']:
                is_matched = compare(reference_entity, entity)
                if is_matched:
                    count_matched += 1
                    break
        if total_topic == 0:
            continue
        matched_entity_count[key] = {
            'entity_count': total_topic,
            'matched_count': count_matched,
            'rate': count_matched * 1.0 / total_topic,
        }

    mean_rate = sum([res['rate'] for res in matched_entity_count.values()]) / len(matched_entity_count.values())
    return mean_rate, matched_entity_count
