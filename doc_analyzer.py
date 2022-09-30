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

    def get_key(self, doc: dict):
        key_fields = [x for x in doc.keys() if self._get_field_importance(doc, x)
                      <= AttributeImportance.PART_OF_DOC_KEY.value]
        key_fields.sort()
        return '#'.join(map(lambda x: x + '=' + str(doc[x]), key_fields))

    def doc_uniqueness_relevant(self, doc: dict, field_name: string) -> bool:
        return not self.doc_ignored(doc) and field_name in doc.keys() and \
               self._get_field_importance(doc, field_name) <= AttributeImportance.PART_OF_DOC_KEY.value

    def doc_projection_beyond_key(self, doc) -> [string, dict]:
        projected = {}
        for key, value in doc.items():
            if not self.doc_uniqueness_relevant(doc, key):
                projected[key] = value
        key = self.get_key(doc)
        return key, projected

    def field_value_relevant(self, doc: dict, field_name: string) -> bool:
        return not self.doc_ignored(doc) and field_name in doc.keys() and \
               self._get_field_importance(doc, field_name) <= AttributeImportance.VALUE_RELEVANT.value

    def field_existence_relevant(self, doc: dict, field_name: string) -> bool:
        ignore = self.doc_ignored(doc)
        field_name_in_doc_keys = field_name in doc.keys()
        importance = self._get_field_importance(doc, field_name)
        return not ignore and field_name_in_doc_keys and \
                importance <= AttributeImportance.EXISTENCE_RELEVANT.value

    @abstractmethod
    def doc_ignored(self, doc: dict) -> bool:
        pass

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
    class Result(Enum):
        DOCS_COUNT = 'docs_count'
        FIELD_USAGE = 'field_usage'
        FIELD_VALUES = 'field_values'

    def __init__(self, analyzer: DocAnalyzer):
        self._fields_values = {}
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
                    if field_name not in self._fields_values:
                        self._fields_values[field_name] = set([doc[field_name]])
                    else:
                        self._fields_values[field_name].add(doc[field_name])

    def get(self):
        return {
            self.Result.DOCS_COUNT.value: self.get_docs_count(),
            self.Result.FIELD_USAGE.value: self.get_fields_usage(),
            self.Result.FIELD_VALUES.value: self.get_fields_values()
        }

    def get_docs_count(self) -> int:
        return self._count_docs

    def get_fields_usage(self):
        return self._fields_usage_count

    def get_fields_used(self):
        return set(self._fields_usage_count.keys())

    def get_field_usage(self, name: string) -> int:
        if name in self._fields_usage_count.keys():
            return self._fields_usage_count[name]
        else:
            return 0

    def get_fields_values(self) -> dict:
        return self._fields_values

    def get_field_values(self, name: string):
        if name in self._fields_values.keys():
            return self._fields_values[name]
        else:
            return set()

    def __repr__(self):
        return self.get()

    def __str__(self):
        return str(self.get())


class AnalyzeDocuments:
    class Results(Enum):
        FIELDS = 'fields'
        KEYS = 'keys'
        CLASSIFIER = 'classifier'
        DOCS_COUNT = 'count_docs'

    def __init__(self, analyzer: DocAnalyzer, docs: [dict]):
        self._analyzer = analyzer
        self._build_report = {
            self.Results.FIELDS.value: DocsAttributesDistribution(self._analyzer),
            self.Results.KEYS.value: {}
        }
        self._count_docs = 0
        self._count_docs_ignored = 0
        self._add_docs(docs)

    def _add_docs(self, docs: [dict] ):
        for doc in docs:
            self.add(doc)

    def _add(self, doc: dict):
        self._count_docs = self._count_docs + 1
        self.get_fields().add(doc)
        key, projection = self._analyzer.doc_projection_beyond_key(doc)
        if key not in self.get_keys():
            self._build_report[self.Results.KEYS.value][key] = DocsAttributesDistribution(self._analyzer)
        self._build_report[self.Results.KEYS.value][key].add(projection)

    def get(self):
        key_results = {}
        for key in self.get_keys():
            key_results[key] = self.get_key(key).get()
        return {
            self.Results.DOCS_COUNT.value: self.get_docs_count(),
            self.Results.FIELDS.value: self.get_fields().get(),
            self.Results.KEYS.value: key_results
        }

    def get_docs_count(self):
        return self._count_docs

    def get_fields(self) -> DocsAttributesDistribution:
        return self._build_report[self.Results.FIELDS.value]

    def get_keys(self):
        return set(self._build_report[self.Results.KEYS.value].keys())

    def get_key(self, key) -> DocsAttributesDistribution:
        return self._build_report[self.Results.KEYS.value][key]

    def __repr__(self):
        return self.get()

    def __str__(self):
        return str(self.get())
