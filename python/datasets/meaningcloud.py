from python.datasets.base import AbstractNlpDataset


class MeaningCloudNlpDataset(AbstractNlpDataset):

    def has_semantic_type(self, response, types):
        return (
            "sementity" in response
            and "type" in response["sementity"]
            and any([
                response["sementity"]["type"].lower().endswith(_type.lower())
                for _type in types
            ])
        )

    def clean_response(self, response):
        """
        Map to common output.
        """
        entities = []
        n_entities = len(response["entity_list"])
        n_nonNIL_entities = 0
        n_implicit_entities = len(response["concept_list"])
        for _entity in response["entity_list"]:
            if self.has_semantic_type(response, ["url"]):
                n_nonNIL_entities += 1
                continue
            for _variant in _entity["variant_list"]:
                entities.append({
                    u"start": _variant[u"inip"],
                    u"end": _variant[u"endp"],
                    u"url": self.parse_provider_urls(_entity[u"semld_list"]) if u"semld_list" in _entity else {},
                    u"topic_text": _variant[u"form"],
                })

        return {
            u"text": None,
            u"n_entities": n_entities,
            u"n_nonNIL_entities": n_nonNIL_entities,
            u"n_implicit_entities": n_implicit_entities,
            u"entities": entities
        }
