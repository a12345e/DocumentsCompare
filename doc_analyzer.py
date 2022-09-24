import string
from enum import Enum
from abc import ABC, abstractmethod


class FieldType(Enum):
    PART_OF_KEY = 'part_of_key'
    VALUE_RELEVANT = 'value_relevant'
    VALUE_IGNORE = 'value_ignore'
    KEY_IGNORE = 'key_ignore'


class DocAnalyzer(ABC):
    """
    The is placehoder for functions required to analyze document contents
    """

    def __init__(self):
        pass

    @abstractmethod
    def doc_ignored(self, doc: dict) -> bool:
        pass

    @abstractmethod
    def partition_fields_by_type(self, doc: dict) -> dict:
        """
        create Map (field type => list of fields of that type)
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


class AnalyzedDocument:
    """
    Analyzed document is a wrapper the holds the document with analyzed information about its content
    """

    def __init__(self,
                 doc: dict,
                 analyzer: DocAnalyzer):
        self._ignored = analyzer.doc_ignored(doc)
        if not self._ignored:
            self._classifier = analyzer.get_classifier(doc)
            self._fields_partition = analyzer.partition_fields_by_type(doc)
            for key in self._fields_partition.keys():
                self._fields_partition[key].sort()
            self._key = '#'.join(map(lambda x: x + '_' + str(doc[x]), self._fields_partition[FieldType.PART_OF_KEY]))
            self._doc = doc

    def get_key(self) -> string:
        """
        get the key of the document
        :return: string
        """
        return self._key

    def get_field_names_partitioned_by_field_type(self) -> dict:
        """
        returns dictionary of lists of field names partitioned by field types
        :return: map (FieldType -> list of field names of that type)
        """
        return self._fields_partition

    def get_classifier(self):
        """
        return the document classifier - document must have one classifier
        :return:
        """
        return self._classifier

    def get_doc(self):
        """
        return the original document
        :return: document
        """
        return self._doc
