import string
from enum import Enum
from abc import ABC, abstractmethod


class FieldImportance(Enum):
    FIELD_PART_OF_KEY = 0
    FIELD_VALUE_RELEVANT = 1
    FIELD_NAME_RELEVANT = 2
    FIELD_NOT_RELEVANT = 3


class DocAnalyzer(ABC):
    """
    The is placehoder for functions required to analyze document contents
    """

    def __init__(self):
        pass

    def get_key(self, doc: dict):
        if self._doc_ignored(doc):
            return None
        key_fields = [x for x in doc.keys() if self._get_field_importance(doc, x) <= FieldImportance.FIELD_PART_OF_KEY.value]
        key_fields.sort()
        return '#'.join(map(lambda x: x + '_' + str(doc[x]), key_fields))

    def field_key_relevant(self, doc:dict, field_name: string) -> bool:
        return not self._doc_ignored(doc) and field_name in doc.keys() and \
               self._get_field_importance(doc, field_name) <= FieldImportance.FIELD_PART_OF_KEY

    def field_value_relevant(self, doc:dict, field_name: string) -> bool:
        return not self._doc_ignored(doc) and field_name in doc.keys() and \
               self._get_field_importance(doc, field_name) <= FieldImportance.FIELD_VALUE_RELEVANT

    def field_name_relevant(self, doc:dict, field_name: string) -> bool:
        return not self._doc_ignored(doc) and field_name in doc.keys() and \
               self._get_field_importance(doc, field_name) <= FieldImportance.FIELD_NAME_RELEVANT

    @abstractmethod
    def _doc_ignored(self, doc: dict) -> bool:
        pass

    @abstractmethod
    def _get_field_importance(self, doc: dict, field_name: string) -> FieldImportance:
        """
        create Map (field type => set of fields of that type)
        :param field_name:
        :param doc:
        :return: enum FieldType
        """
        pass

    @abstractmethod
    def _get_classifier(self, doc: dict) -> string:
        """
        Get classification for the document
        :param doc:
        :return: string
        """
        pass


class ReportDocsFieldNameUsage:
    def __init__(self, analyzer: DocAnalyzer):
        self._fields_usage_count = {}
        self._fields_value_distribution = {}
        self._analyzer = analyzer
        pass

    def report_usage(self, doc: dict):
        for field_name in doc.keys():
            if self._analyzer.field_name_relevant(doc,field_name):
                if field_name not in self._fields_usage_count:
                    self._fields_usage_count[field_name] = 1
                else:
                    self._fields_usage_count[field_name] = self._fields_usage_count[field_name] + 1
                if self._analyzer.field_value_relevant(doc, field_name):
                    if field_name not in self._fields_value_distribution:
                        self._fields_value_distribution[field_name] = set([doc[field_name]])
                    else:
                        self._fields_value_distribution[field_name].add(doc[field_name])

    def get_results(self):
        return {'fields_usage_count': self._fields_usage_count, 'fields_value_count': self._fields_value_distribution_count }


class AnalyzedDocumentsSet:
    """
    Analyzed document is a wrapper the holds the document with analyzed information about its content
    """

    def __init__(self,analyzer: DocAnalyzer):
        self._analyzer = analyzer
        self._report_by_classifier = {}

    def add(self, doc: dict):
        if self._analyzer.doc_ignored(doc):
            return

        classifier = self._analyzer.get_classifier(doc)
        key = self._analyzer.get_key(doc)
        if classifier not in self._report_by_classifier:
            self._report_by_classifier[classifier] = {
                'fields': ReportDocsFieldNameUsage(self._analyzer),
                'doc_keys': {}
                }

        report = self._report_by_classifier[classifier]
        report['fields'].add(doc)
        doc_for_key = {}
        for key, value in doc:
            if not self._analyzer.field_key_relevant(doc, key):
                doc_for_key[key] = value
        if key not in report['doc_keys'].keys():
            report['doc_keys'][key] = {
                'count_docs': 0,
                'fields': ReportDocsFieldNameUsage(self._analyzer)
            }
        report['doc_keys'][key]['count_docs'] = report['doc_keys'][key]['count_docs'] + 1
        report['doc_keys'][key]['fields'].add(doc_for_key)

    def get_report(self):
        return self._report_by_classifier


