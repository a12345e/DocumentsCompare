import string
from enum import Enum
from abc import ABC, abstractmethod


class FieldType(Enum):
    PART_OF_KEY = 'part_of_key'
    VALUE_RELEVANT = 'value_relevant'
    VALUE_IGNORE = 'value_ignore'
    KEY_IGNORE = 'key_ignore'


class DocAnalyzer:
    def __init__(self):
        pass

    @abstractmethod
    def get_field_type(self, field_name: string) -> FieldType:
        pass

    @abstractmethod
    def get_doc_classifier(self, doc: dict) -> string:
        pass


class AnalyzedDocument:
    def __init__(self,
                 doc: dict,
                 analyzer: DocAnalyzer):
        self._doc = doc

        self._classifier = analyzer.get_doc_classifier(doc)
        self._field_lists = {}
        for field_type in FieldType:
            self._field_lists[field_type] = []
        for key in doc.keys():
            self._field_lists[analyzer.get_field_type(key)].append(key)
        for key in self._field_lists.keys():
            self._field_lists[key].sort()

        self._key = '#'.join(map(lambda x: x + '_' + str(doc[x]), self._field_lists[FieldType.PART_OF_KEY]))

    def get_key(self):
        return self._key

    def get_key_lists(self):
        return self._field_lists

    def get_classifier(self):
        return self._classifier

    def get_doc(self):
        return self._doc
