import re

from python.datasets.base import AbstractNlpDataset


class OpenCalaisNlpDataset(AbstractNlpDataset):

    def _has_typeReference(self, response, type_references):
        return (
            u"_typeReference" in response
            and any([
                response[u"_typeReference"].endswith(_tr)
                for _tr in type_references
            ])
        )


    def clean_response(self, response):
        """
        Map to common output.

        types:
        ArmedAttack, CandidatePosition, City, Company, CompanyInvestigation,
        ContactDetails, Continent, Conviction, Country, CreditRating, Date,
        DiplomaticRelations, EmailAddress, EmploymentChange, EntertainmentAwardEvent,
        Facility, Holiday, IndustryTerm, ManMadeDisaster, MarketIndex, MedicalCondition,
        MedicalTreatment, MilitaryAction, Movie, NaturalFeature, Organization, Person,
        PersonCareer, PersonLocation, PersonTravel, Position, Product, ProductIssues,
        ProductRecall, ProvinceOrState, PublishedMedium, Quotation, Region, SportsEvent,
        SportsLeague, Technology, URL

        Notes:
        - We count as NIL entities the entities which does not show an instance in the text.
        """
        entities = []
        n_entities = 0
        n_nonNIL_entities = 0
        n_implicit_entities= 0

        for k, v in response.iteritems():
            if "_typeGroup" in v and v["_typeGroup"] == "socialTag":
                entities.append({
                    u"start": -1,
                    u"end": -1,
                    u"url": {'opencalais': v['id']},  # url not working
                    u"topic_text": v[u"name"],  # base text (not topic text)
                })
            # Remove non entities values
            if k.endswith("ComponentVersions") or k.endswith("DefaultLangId"):
                continue
            n_entities += 1
            # Remove NIL entities
            if not "instances" in v or v[u"_type"] in [u"URL"]:
                continue

            # Selecting implicit typeReference
            if self._has_typeReference(v, ["ContactDetails"]):
                continue
            elif self._has_typeReference(
                    v, [
                        "Conviction", "PersonCareer", "PersonLocation", "PersonTravel",
                        "CompanyInvestigation", "ArmedAttack", "ProductRecall", "ProductIssues", "DiplomaticRelations",
                        "Quotation", "MilitaryAction", "ManMadeDisaster", "CreditRating", "CandidatePosition", "EmploymentChange"
                    ]):
                n_implicit_entities += 1
                continue

            n_nonNIL_entities += 1
            # map all instances (usually only one)
            for _inst in v[u"instances"]:
                try:
                    entities.append({
                        u"start": _inst[u"offset"],
                        u"end": _inst[u"offset"] + _inst[u"length"],
                        u"url": {"opencalais": k},  # url not working
                        u"topic_text": v[u"name"],  # base text (not topic text)
                    })
                except Exception as e:
                    raise Exception("Check parsing - exception: %s" % e)
        return {
            u"text": None,
            u"n_entities": n_entities,
            u"n_nonNIL_entities": n_nonNIL_entities,
            u"n_implicit_entities": n_implicit_entities,
            u"entities": entities
        }
