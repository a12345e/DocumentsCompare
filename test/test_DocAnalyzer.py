import unittest
import string
from abc import ABC

from doc_analyzer import DocAnalyzer, FieldType, AnalyzedDocument


class TheDocAnalyzer(DocAnalyzer):

    def doc_ignored(self, doc: dict) -> bool:
        return False

    def partition_fields_by_type(self, doc: string) -> FieldType:
        if doc.startswith(FieldType.KEY_IGNORE.name):
            return FieldType.KEY_IGNORE
        if doc.startswith(FieldType.VALUE_IGNORE.name):
            return FieldType.VALUE_IGNORE
        if doc.startswith(FieldType.VALUE_RELEVANT.name):
            return FieldType.VALUE_RELEVANT
        return FieldType.PART_OF_KEY

    def get_classifier(self, doc: dict) -> string:
        if 'classifier' in doc:
            return doc['classifier']
        return 'unclassified'


class TestDocAnalyzer(unittest.TestCase):

    def test_the_analyzer_classifier(self):
        analyzer = TheDocAnalyzer()
        self.assertEqual(analyzer.get_classifier({'a': 'a'}), 'unclassified')
        self.assertEqual(analyzer.get_classifier({'classifier': 'a', 'b': 'a'}), 'a')

    def test_the_analyzer_field_typing(self):
        analyzer = TheDocAnalyzer()
        self.assertEqual(analyzer.partition_fields('a'), FieldType.PART_OF_KEY)
        self.assertEqual(analyzer.partition_fields('PART_OF_KEY_x'), FieldType.PART_OF_KEY)
        self.assertEqual(analyzer.partition_fields('KEY_IGNORE'), FieldType.KEY_IGNORE)
        self.assertEqual(analyzer.partition_fields('VALUE_IGNORE_y'), FieldType.VALUE_IGNORE)
        self.assertEqual(analyzer.partition_fields('VALUE_RELEVANT_u'), FieldType.VALUE_RELEVANT)

    def test_analyze_document(self):
        analyzer = TheDocAnalyzer()
        analyzed_document = AnalyzedDocument({
            'a': 'a',
            'classifier': 'classifier_x',
            'PART_OF_KEY_x': 'part_of_key_x_value',
            'PART_OF_KEY_y': 'part_of_key_y_value',
            'KEY_IGNORE_x': 'key_ignore_x_value',
            'KEY_IGNORE_y': 'key_ignore_y_value',
            'VALUE_IGNORE_x': 'value_ignore_x_value',
            'VALUE_IGNORE_y': 'value_ignore_y_value',
            'VALUE_RELEVANT_x': 'value_relevant_x_value',
            'VALUE_RELEVANT_y': 'value_relevant_y_value',
            'VALUE_RELEVANT_z': None
        }, analyzer)
        self.assertEqual(analyzed_document.get_classifier(), 'classifier_x')
        self.assertEqual(set(analyzed_document.get_key_partitions_lists()[FieldType.KEY_IGNORE]),
                         set(['KEY_IGNORE_y', 'KEY_IGNORE_x']))
        self.assertEqual(set(analyzed_document.get_key_partitions_lists()[FieldType.PART_OF_KEY]),
                         set(['PART_OF_KEY_y', 'PART_OF_KEY_x', 'a', 'classifier']))
        self.assertEqual(set(analyzed_document.get_key_partitions_lists()[FieldType.VALUE_IGNORE]),
                         set(['VALUE_IGNORE_x', 'VALUE_IGNORE_y']))
        self.assertEqual(set(analyzed_document.get_key_partitions_lists()[FieldType.VALUE_RELEVANT]),
                         set(['VALUE_RELEVANT_x', 'VALUE_RELEVANT_y', 'VALUE_RELEVANT_z']))
        self.assertEqual(analyzed_document.get_key(),'PART_OF_KEY_x_part_of_key_x_value#PART_OF_KEY_y_part_of_key_y_value#a_a#classifier_classifier_x')

    def test_aaaa(self):
        analyzer = TheDocAnalyzer()
        analyzed_document = AnalyzedDocument({
            'a': 'a',
            'classifier': 'classifier_x',
            'PART_OF_KEY_x': 'part_of_key_x_value',
            'PART_OF_KEY_y': 'part_of_key_y_value',
            'KEY_IGNORE_x': 'key_ignore_x_value',
            'KEY_IGNORE_y': 'key_ignore_y_value',
            'VALUE_IGNORE_x': 'value_ignore_x_value',
            'VALUE_IGNORE_y': 'value_ignore_y_value',
            'VALUE_RELEVANT_x': 'value_relevant_x_value',
            'VALUE_RELEVANT_y': 'value_relevant_y_value',
            'VALUE_RELEVANT_z': None
        }, analyzer)


if __name__ == '__main__':
    unittest.main()
