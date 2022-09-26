import string
from enum import Enum
from abc import ABC, abstractmethod


class AttributeImportance(Enum):
    PART_OF_DOC_KEY = 0
    VALUE_RELEVANT = 1
    EXISTENCE_RELEVANT = 2
    NOT_RELEVANT = 3


class DocAnalyzer(ABC):
    """
    The is placehoder for functions required to analyze document contents
    """

    def __init__(self):
        pass

    def doc_ignored(self, doc: dict):
        if not self._doc_ignored(doc):
            list_key_fields = [x for x in doc.keys() if self._get_field_importance(doc, x).value
                        <= AttributeImportance.PART_OF_DOC_KEY.value]
            return len(list_key_fields) == 0
        else:
            return False

    def get_key(self, doc: dict):
        key_fields = [x for x in doc.keys() if self._get_field_importance(doc, x).value
                      <= AttributeImportance.PART_OF_DOC_KEY.value]
        key_fields.sort()
        return '#'.join(map(lambda x: x + '=' + str(doc[x]), key_fields))

    def doc_uniqueness_relevant(self, doc: dict, field_name: string) -> bool:
        return not self.doc_ignored(doc) and field_name in doc.keys() and \
               self._get_field_importance(doc, field_name).value <= AttributeImportance.PART_OF_DOC_KEY.value

    def field_value_relevant(self, doc: dict, field_name: string) -> bool:
        return not self.doc_ignored(doc) and field_name in doc.keys() and \
               self._get_field_importance(doc, field_name).value <= AttributeImportance.VALUE_RELEVANT.value

    def field_existence_relevant(self, doc: dict, field_name: string) -> bool:
        return not self.doc_ignored(doc) and field_name in doc.keys() and \
               self._get_field_importance(doc, field_name).value <= AttributeImportance.EXISTENCE_RELEVANT.value

    @abstractmethod
    def _doc_ignored(self, doc: dict) -> bool:
        return False

    @abstractmethod
    def _get_field_importance(self, doc: dict, field_name: string) -> AttributeImportance:
        """
        create Map (field type => set of fields of that type)
        :param field_name:
        :param doc:
        :return: enum FieldType
        """
        pass

    @abstractmethod
    def get_classifier(self, doc: dict) -> string:
        """
        Get classification for the document
        :param doc:
        :return: string
        """
        pass


class DocsAttributesDistribution:
    def __init__(self, analyzer: DocAnalyzer):
        self._fields_value_distribution = {}
        self._fields_usage_count = {}
        self._analyzer = analyzer
        self._count_docs = 0
        pass

    def add(self, doc: dict):
        self._count_docs = self._count_docs + 1
        for field_name in doc.keys():
            if self._analyzer.field_existence_relevant(doc, field_name):
                if field_name not in self._fields_usage_count:
                    self._fields_usage_count[field_name] = 1
                else:
                    self._fields_usage_count[field_name] = self._fields_usage_count[field_name] + 1
                if self._analyzer.field_value_relevant(doc, field_name):
                    if field_name not in self._fields_value_distribution:
                        self._fields_value_distribution[field_name] = set([doc[field_name]])
                    else:
                        self._fields_value_distribution[field_name].add(doc[field_name])

    def get(self):
        return {'count_docs': self._count_docs,
                'attributes_usage': self._fields_usage_count,
                'attributes_distribution': self._fields_value_distribution}


class AnalyzedDocumentsSet:
    """
    Analyzed document is a wrapper the holds the document with analyzed information about its content
    """

    def __init__(self, analyzer: DocAnalyzer):
        self._analyzer = analyzer
        self._count_docs = 0
        self._count_docs_ignored = 0
        self._report_by_classifier = {}

    def add(self, doc: dict):
        self._count_docs = self._count_docs +1
        if self._analyzer.doc_ignored(doc):
            self._count_docs_ignored = self._count_docs_ignored + 1
            return

        classifier = self._analyzer.get_classifier(doc)
        key = self._analyzer.get_key(doc)
        if classifier not in self._report_by_classifier:
            self._report_by_classifier[classifier] = {
                'fields': DocsAttributesDistribution(self._analyzer),
                'doc_keys': {}
            }

        report = self._report_by_classifier[classifier]
        report['fields'].add(doc)
        doc_for_key = {}
        for key, value in doc:
            if not self._analyzer.doc_uniqueness_relevant(doc, key):
                doc_for_key[key] = value
        if key not in report['doc_keys'].keys():
            report['doc_keys'][key] = {
                'count_docs': 0,
                'fields': DocsAttributesDistribution(self._analyzer)
            }
        report['doc_keys'][key]['fields'].add(doc_for_key)

    def get_report(self):
        return self._report_by_classifier
