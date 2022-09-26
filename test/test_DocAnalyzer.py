import unittest
import string

from doc_analyzer import DocAnalyzer, AttributeImportance, DocsAttributesDistribution, AnalyzedDocumentsSet


class TheDocAnalyzer(DocAnalyzer):

    def get_classifier(self, doc: dict) -> string:
        if 'classifier' in doc:
            return doc['classifier']
        return 'unclassified'

    def _get_field_importance(self, doc: dict, field_name: string) -> AttributeImportance:
        if field_name.startswith(AttributeImportance.EXISTENCE_RELEVANT.name):
            return AttributeImportance.EXISTENCE_RELEVANT
        elif field_name.startswith(AttributeImportance.VALUE_RELEVANT.name):
            return AttributeImportance.VALUE_RELEVANT
        elif field_name.startswith(AttributeImportance.PART_OF_DOC_KEY.name):
            return AttributeImportance.PART_OF_DOC_KEY
        else:
            return AttributeImportance.NOT_RELEVANT

    def _doc_ignored(self, doc: dict) -> bool:
        return False


class TestDocAnalyzer(unittest.TestCase):

    def test_the_analyzer_classifier(self):
        analyzer = TheDocAnalyzer()
        self.assertEqual(analyzer.get_classifier({'a': 'a'}), 'unclassified')
        self.assertEqual(analyzer.get_classifier({'classifier': 'a', 'b': 'a'}), 'a')

    def test_the_analyzer_attribute_doc_uniqueness_relevant(self):
        analyzer = TheDocAnalyzer()
        self.assertFalse(analyzer.doc_uniqueness_relevant({'a': 'a'}, 'a'))
        self.assertFalse(analyzer.doc_uniqueness_relevant({'a': 'a'}, 'b'))
        self.assertTrue(analyzer.doc_uniqueness_relevant({AttributeImportance.PART_OF_DOC_KEY.name + 'x': 'x'},
                                                         AttributeImportance.PART_OF_DOC_KEY.name + 'x'))

    def test_the_analyzer_attribute_value_relevant(self):
        analyzer = TheDocAnalyzer()
        self.assertTrue(analyzer.field_value_relevant({AttributeImportance.PART_OF_DOC_KEY.name + 'x': 'x'},
                                                      AttributeImportance.PART_OF_DOC_KEY.name + 'x'))
        self.assertFalse(analyzer.field_value_relevant({
            'x': 'x', AttributeImportance.PART_OF_DOC_KEY.name + 'x': 'x'
        }, 'x'))
        self.assertTrue(analyzer.field_value_relevant({
            AttributeImportance.PART_OF_DOC_KEY.name + 'x': 'x',
            AttributeImportance.VALUE_RELEVANT.name + 'x': 'x'},
            AttributeImportance.VALUE_RELEVANT.name + 'x'))

    def test_the_analyzer_attribute_exist_relevant(self):
        analyzer = TheDocAnalyzer()
        self.assertFalse(analyzer.field_existence_relevant({'x': 'x'}, 'x'))
        self.assertFalse(analyzer.field_existence_relevant({AttributeImportance.EXISTENCE_RELEVANT.name + 'x': 'x'},
                                                           AttributeImportance.EXISTENCE_RELEVANT.name + 'x'))
        self.assertTrue(analyzer.field_existence_relevant({
            AttributeImportance.PART_OF_DOC_KEY.name + 'x': 'x',
            AttributeImportance.EXISTENCE_RELEVANT.name + 'x': 'x'},
            AttributeImportance.EXISTENCE_RELEVANT.name + 'x'))

    def test_the_analyzer_get_key(self):
        analyzer = TheDocAnalyzer()
        doc = {
            'a': 'a',
            'classifier': 'classifier_x',
            AttributeImportance.PART_OF_DOC_KEY.name + '_x2': 'part_of_key_x2_value',
            AttributeImportance.PART_OF_DOC_KEY.name + '_x3': 'part_of_key_x3_value',
            AttributeImportance.PART_OF_DOC_KEY.name + '_x1': 'part_of_key_x1_value',
            'b': 'b'}
        key = analyzer.get_key(doc)
        self.assertEqual(
            'PART_OF_DOC_KEY_x1=part_of_key_x1_value#PART_OF_DOC_KEY_x2=part_of_key_x2_value#PART_OF_DOC_KEY_x3=part_of_key_x3_value',
            analyzer.get_key(doc))


class TestDocsSummary(unittest.TestCase):

    def test_if_only_existence_no_value(self):
        analyzer = TheDocAnalyzer()
        doc1 = {
            AttributeImportance.PART_OF_DOC_KEY.name + '_1': 'key_1_value',
            AttributeImportance.EXISTENCE_RELEVANT.name + '_1': 'exist_1_value',
            AttributeImportance.EXISTENCE_RELEVANT.name + '_2': 'exist_2_value',
        }
        doc2 = {
            AttributeImportance.PART_OF_DOC_KEY.name + '_1': 'key_1_value',
            AttributeImportance.EXISTENCE_RELEVANT.name + '_1': 'exist_1_value',
            AttributeImportance.EXISTENCE_RELEVANT.name + '_2': 'exist_2_value_other',
        }
        summary = DocsAttributesDistribution(analyzer)
        summary.add(doc1);
        summary.add(doc2);
        self.assertEqual(summary.get(), {'count_docs': 2, 'attributes_usage': {'PART_OF_DOC_KEY_1': 2, 'EXISTENCE_RELEVANT_1': 2, 'EXISTENCE_RELEVANT_2': 2}, 'attributes_distribution': {'PART_OF_DOC_KEY_1': {'key_1_value'}}})

    def test_more(self):
        analyzer = TheDocAnalyzer()
        doc1 = {
            'a': 'a',
            'classifier': 'classifier_x',
            AttributeImportance.PART_OF_DOC_KEY.name + '_1': 'key_1_value',
            AttributeImportance.PART_OF_DOC_KEY.name + '_2': 'key_2_value',
            AttributeImportance.EXISTENCE_RELEVANT.name + '_1': 'exist_1_value',
            AttributeImportance.EXISTENCE_RELEVANT.name + '_2': 'exist_2_value',
            AttributeImportance.VALUE_RELEVANT.name + '_1': 'value_relevant_1_value',
            AttributeImportance.VALUE_RELEVANT.name + '_2': 'value_relevant_2_value',
            'b': 'b'}
        doc2 = {
            'a': 'a',
            'classifier': 'classifier_x',
            AttributeImportance.PART_OF_DOC_KEY.name + '_1': 'key_1_value',
            AttributeImportance.PART_OF_DOC_KEY.name + '_2': 'key_2_value_other',
            AttributeImportance.EXISTENCE_RELEVANT.name + '_1': 'exist_1_value',
            AttributeImportance.EXISTENCE_RELEVANT.name + '_2': 'exist_2_value_other',
            AttributeImportance.VALUE_RELEVANT.name + '_1': 'value_relevant_1_value_other',
            AttributeImportance.VALUE_RELEVANT.name + '_2': 'value_relevant_2_value_other',
            'b': 'b'}
        summary = DocsAttributesDistribution(analyzer)
        summary.add(doc1);
        summary.add(doc2);
        print(summary.get())
        self.assertEqual({'count_docs': 2, 'attributes_usage': {'PART_OF_DOC_KEY_1': 2, 'PART_OF_DOC_KEY_2': 2, 'EXISTENCE_RELEVANT_1': 2, 'EXISTENCE_RELEVANT_2': 2, 'VALUE_RELEVANT_1': 2, 'VALUE_RELEVANT_2': 2}, 'attributes_distribution': {'PART_OF_DOC_KEY_1': {'key_1_value'}, 'PART_OF_DOC_KEY_2': {'key_2_value', 'key_2_value_other'}, 'VALUE_RELEVANT_1': {'value_relevant_1_value', 'value_relevant_1_value_other'}, 'VALUE_RELEVANT_2': {'value_relevant_2_value', 'value_relevant_2_value_other'}}},summary.get())


if __name__ == '__main__':
    unittest.main()
