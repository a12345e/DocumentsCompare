from doc_analyzer import DocAnalyzer, FieldImportance, AnalyzedDocument
import string

_TESTED = 'tested'
_EXPECTED = 'expected'
_COMMON = 'common'
_DIFF = 'diff'
_COUNT = 'count'
_CLASSIFIER = 'group'
_NAMES = 'names'

"""
we separate for classifiers.
Then we start compare content per classifier
    1) Compare fields names not ignored for all documents
      1.2) for each field that is common and value not ignored we count:
        documents including it tested/expected
        how many different values for tested/expected
        how many common different values
        one sample for values difference
    2) show difference of key sets
       count all, count common, difference of keys
    3) for each common documents key we compare:
       count documents 
       we show here the count total for tested,expected and then the count of common
    Then we show difference of the key sets
    Then for each key that is common for both we compare:
        count of documents (tested, expected)
        We collect the value relevant keys for each document:
        these are value_relevant
        We make diff of those keys
"""

def compue_key_value_distribution_per_field_type(docs: [],field_names: set):

def compue_key_value_distribution_per_classifier(docs: [AnalyzedDocument]):

    field_types_partition = {}
    for doc in docs:
        field_types_partition = doc.
        for field_name in field_types_partitions[field_type]:
            if field_name not in field_values[field_type]:
                field_values[field_type][field_name] = set([doc.get_doc()[field_name]])
            else:
                field_values[field_type][field_name].add(doc.get_doc()[field_name])


def compue_key_value_distribution(docs: [dict], classifier, min_field_importance: FieldImportance,analyzer: DocAnalyzer):
    analyzed_docs: [AnalyzedDocument] = \
        map(lambda x: AnalyzedDocument(x, analyzer),
            filter(lambda x: x.get_classifier() == classifier, docs))
    analyzed_docs_by_classifier = {}
    report = {}
    field_values = {}
    for doc in analyzed_docs:
        field_types_partitions = analyzer.partition_fields_by_type(doc)
        for field_name in field_types_partitions[field_type]:
            if not field_name in field_values[field_type]:
                field_values[field_type][field_name] = set([doc.get_doc()[field_name]])
            else:
                field_values[field_type][field_name].add(doc.get_doc()[field_name])


class DocumentSetsComparator:
    """
    We create analyzed documents partitioned by (classifier, key)
    """

    def __init__(self, analyzer: DocAnalyzer, tested_docs: [dict],
                 expected_docs: [dict]):
        self._tested_partition = self._partition_docs(tested_docs, analyzer)
        self._expected_partition = self._partition_docs(expected_docs, analyzer)
        self._diff = \
            {_CLASSIFIER:
                {
                    _COMMON: len(set(self._tested_partition.keys()).intersection(set(self._expected_partition.keys()))),
                    _TESTED: len(set(self._tested_partition.keys()).difference(set(self._expected_partition.keys()))),
                    _EXPECTED: len(set(self._expected_partition.keys()).difference(set(self._tested_partition.keys())))
                }}

    @staticmethod
    def compare_classifier(self, tested_partitioned_by_key: dict, expected_partitioned_by_key: dict):
        summary_by_keys = self.compare_keys(tested_partitioned_by_key, expected_partitioned_by_key)

    @staticmethod
    def compare_keys(self, tested: dict, expected: dict):
        report = {_COUNT: {
            _TESTED: len(tested.keys()),
            _EXPECTED: len(expected.keys()),
            _COMMON: len(set(expected.keys()).intersection(set(tested.keys())))
        },
            _DIFF: {
                _EXPECTED: set(expected.keys()).difference_update(set(tested.keys())),
                _TESTED: set(tested.keys()).difference_update(set(expected.keys())),
            }
        }
        return report

    @staticmethod
    def _partition_docs(docs: [dict], analyzer: DocAnalyzer) -> dict:
        partition = {}
        for doc in docs:
            analyzed_doc = AnalyzedDocument(doc, analyzer)
            if analyzed_doc.get_classifier() not in partition:
                partition[analyzed_doc.get_classifier()] = {}
            if analyzed_doc.get_key() not in partition[analyzed_doc.get_classifier()]:
                partition[analyzed_doc.get_classifier()][analyzed_doc.get_key()] = [analyzed_doc]
            else:
                partition[analyzed_doc.get_classifier()][analyzed_doc.get_key()].append(analyzed_doc)
        return partition
