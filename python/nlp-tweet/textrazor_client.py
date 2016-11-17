import codecs
import json
import pprint
import time
import requests

import textrazor as talib

talib.api_key = "88d801087aa7ca4fff63a51dcd5f42ccf3b7b00a7c1528e50dfa2e9e"

client = talib.TextRazor(extractors=["entities", "topics"])

with codecs.open('tweet.json', 'r', 'utf8') as fh:
    tweets = json.load(fh)

textrazor = {}

for key, tweet in tweets.items():
    time.sleep(1)
    try:
        res = client.analyze(tweet['text'])
        entities = []
        for entity in res.entities():
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
        textrazor[key] = {'entities': entities}
        print '%s processed' % key
    except Exception as e:
        print e
        continue
    except talib.TextRazorAnalysisException as e:
	print e
	continue

with codecs.open('textrazor.json', 'w', 'utf8') as fh:
    json.dump(textrazor, fh, indent=2)
