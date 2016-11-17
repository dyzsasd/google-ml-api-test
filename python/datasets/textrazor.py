from python.datasets.base import AbstractNlpDataset


class TextrazorDataset(AbstractNlpDataset):
    def clean_response(self, response):
        entities = []
        n_entities = 0
        n_nonNIL_entities = 0

        for entity in response.get('entities', []):
            parsed_entity = {
                'start': entity['matched_positions'][0],
                'end': -1,
                'urls': {},
                'graph_ids': {},
                'topic_text': entity['matched_text'],
            }
            is_noNIL_entity = False
            if 'wikipedia_link' in entity and entity['wikipedia_link']:
                parsed_entity['urls']['wikipedia'] = entity['wikipedia_link']
                is_noNIL_entity = True
            if 'freebase_id' in entity and entity['freebase_id']:
                parsed_entity['graph_ids']['freebase'] = entity['freebase_id']
                is_noNIL_entity = True
            if 'wikidata_id' in entity and entity['wikidata_id']:
                parsed_entity['graph_ids']['wikidata'] = entity['wikidata_id']
                is_noNIL_entity = True
            if is_noNIL_entity:
                n_nonNIL_entities += 1
            n_entities += 1
            entities.append(parsed_entity)

        return {
            u"text": None,
            u"n_entities": n_entities,
            u"n_nonNIL_entities": n_nonNIL_entities,
            u"entities": entities
        }
