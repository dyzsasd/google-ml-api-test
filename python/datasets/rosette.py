from python.datasets.base import AbstractNlpDataset


class RosetteDataset(AbstractNlpDataset):
    def clean_response(self, response):
        entities = []
        n_entities = 0
        n_nonNIL_entities = 0

        for entity in response.get('entities', []):
            parsed_entity = {
                'start': -1,
                'end': -1,
                'urls': {},
                'topic_text': entity['mention']
            }
            if entity['entityId'].startswith('Q'):
                parsed_entity['graph_ids'] = {
                    'wikidata': entity['entityId']
                }
                n_nonNIL_entities += 1
            n_entities += 1
            entities.append(parsed_entity)

        return {
            u"text": None,
            u"n_entities": n_entities,
            u"n_nonNIL_entities": n_nonNIL_entities,
            u"entities": entities
        }
