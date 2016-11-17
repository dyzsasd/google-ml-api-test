import codecs
import json
import pprint
import time
import requests

from python.datasets.daily import get_user_videos_from_file
import textrazor as talib
from python.datasets.textrazor import TextrazorDataset


talib.api_key = "a7e0115736177c0ba698d921c7a49b864aaca7d47cef44933ba7706d"

client = talib.TextRazor(extractors=["entities", "topics"])

textrazor = {}

user_videos = get_user_videos_from_file("videos.json")

textrazor_parser = TextrazorDataset('')

for user, videos in user_videos.items():
    for video in videos:
        res = {}
        parsed_res={}
        try:
            r = client.analyze(video['title'])
            entities = []
            for entity in r.entities():
                entity_dict = {
                    'id': entity.id,
                    'custom_entity_id': entity.custom_entity_id,
                    'confidence_score': entity.confidence_score,
                    'dbpedia_types': entity.dbpedia_types,
                    'freebase_types': entity.freebase_types,
                    'freebase_id': entity.freebase_id,
                    'wikidata_id': entity.wikidata_id,
                    'matched_positions': entity.matched_positions,
                    'matched_words': entity.matched_words,
                    'matched_text': entity.matched_text,
                    'data': entity.data,
                    'relevance_score': entity.relevance_score,
                    'wikipedia_link': entity.wikipedia_link,
                }
                entities.append(entity_dict)
            res['title'] = {'entities': entities}
            parsed_res['title'] = textrazor_parser.clean_response({'entities': entities})
            print 'processed %s title' % video['id']
        except Exception as e:
            print e
        except talib.TextRazorAnalysisException as e:
            print e

        try:
            r = client.analyze(video['description'])
            entities = []
            for entity in r.entities():
                entity_dict = {
                    'id': entity.id,
                    'custom_entity_id': entity.custom_entity_id,
                    'confidence_score': entity.confidence_score,
                    'dbpedia_types': entity.dbpedia_types,
                    'freebase_types': entity.freebase_types,
                    'freebase_id': entity.freebase_id,
                    'wikidata_id': entity.wikidata_id,
                    'matched_positions': entity.matched_positions,
                    'matched_words': entity.matched_words,
                    'matched_text': entity.matched_text,
                    'data': entity.data,
                    'relevance_score': entity.relevance_score,
                    'wikipedia_link': entity.wikipedia_link,
                }
                entities.append(entity_dict)
            res['description'] = {'entities': entities}
            parsed_res['description'] = textrazor_parser.clean_response({'entities': entities})
            print 'processed %s description' % video['id']
        except Exception as e:
            print e
        except talib.TextRazorAnalysisException as e:
            print e

        try:
            r = client.analyze(' '.join(video['tags']))
            entities = []
            for entity in r.entities():
                entity_dict = {
                    'id': entity.id,
                    'custom_entity_id': entity.custom_entity_id,
                    'confidence_score': entity.confidence_score,
                    'dbpedia_types': entity.dbpedia_types,
                    'freebase_types': entity.freebase_types,
                    'freebase_id': entity.freebase_id,
                    'wikidata_id': entity.wikidata_id,
                    'matched_positions': entity.matched_positions,
                    'matched_words': entity.matched_words,
                    'matched_text': entity.matched_text,
                    'data': entity.data,
                    'relevance_score': entity.relevance_score,
                    'wikipedia_link': entity.wikipedia_link,
                }
                entities.append(entity_dict)
            res['tags'] = {'entities': entities}
            parsed_res['tags'] = textrazor_parser.clean_response({'entities': entities})
            print 'processed %s tags' % video['id']
        except Exception as e:
            print e
        except talib.TextRazorAnalysisException as e:
            print e

        video['results'] = res
        video['parsed_results'] = parsed_res

with codecs.open('dailymotion-textrazor.json', 'w', 'utf8') as fh:
    json.dump(user_videos, fh, indent=2)
