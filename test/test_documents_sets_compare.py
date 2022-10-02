import unittest


from document_sets_compare import CompareDocumentSets, pretty
from test_doc_analyzer import TheDocAnalyzer
from document_generator import generate_document


class MyTestCase(unittest.TestCase):

    def test_one_same_doc(self):
        comparator = CompareDocumentSets(TheDocAnalyzer())
        doc = generate_document('class1', ['k=k1'],['v=v1'],['exist=exist1'],['garbage=g1'])
        summary,result = comparator.run([doc], [doc], "ut_directory", "./tmp")
        self.assertEqual({'unclassified': {'docs_count': (1, 1), 'summed_difference_types': set()}}, summary)

    def test_one_doc_different_garbage_value(self):
        comparator = CompareDocumentSets(TheDocAnalyzer())
        doce = generate_document('class1', ['k=k1'],['v=v1'],['exist=exist1'],['garvage=g1'])
        doct = generate_document('class1', ['k=k1'],['v=v1'],['exist=exist1'],['garbage=g1'])
        summary, result = comparator.run([doce], [doct], "ut_directory", "./tmp")
        self.assertEqual({'unclassified': {'docs_count': (1, 1), 'summed_difference_types': set()}}, summary)

    def test_one_doc_different_garbage_key(self):
        comparator = CompareDocumentSets(TheDocAnalyzer())
        doce = generate_document('class1', ['k=k1'],['v=v1'],['exist=exist1'],['garvage1=g1'])
        doct = generate_document('class1', ['k=k1'],['v=v1'],['exist=exist1'],['garbage2=g2'])
        summary, result = comparator.run([doce], [doct], "ut_directory", "./tmp")
        self.assertEqual({'unclassified': {'docs_count': (1, 1), 'summed_difference_types': set()}}, summary)

    def test_one_doc_different_exist_only_key_value(self):
        comparator = CompareDocumentSets(TheDocAnalyzer())
        doce = generate_document('class1', ['k=k1'],['v=v1'],['exist=exist1'],['garvage1=g1'])
        doct = generate_document('class1', ['k=k1'],['v=v1'],['exist=exist2'],['garbage2=g2'])
        summary,result = comparator.run([doce], [doct], "ut_directory", "./tmp")
        self.assertEqual({'unclassified': {'docs_count': (1, 1), 'summed_difference_types': set()}}, summary)
        print(pretty(result))

    def test_one_doc_different_exist_only_key(self):
        comparator = CompareDocumentSets(TheDocAnalyzer())
        doce = generate_document('class1', ['k=k1'],['v=v1'],['exist1=exist1'],['garvage1=g1'])
        doct = generate_document('class1', ['k=k1'],['v=v1'],['exist2=exist2'],['garbage2=g2'])
        summary, result = comparator.run([doce], [doct], "ut_directory", "./tmp")
        self.assertEqual({'unclassified': {'docs_count': (1, 1), 'summed_difference_types': {'field_existence'}}},
                         summary)
        self.assertEqual(
            {'summed_difference_types': {'field_existence'}, 'docs_count': (1, 1),
         'fields': {'summed_difference_types': {'field_existence'}, 'docs_count': (1, 1),
                    'field_usage_summary': {'tested_only': {'EXISTENCE_RELEVANTexist2'},
                                            'expected_only': {'EXISTENCE_RELEVANTexist1'}, 'same': 2},
                    'common_fields_with_relevant_values_value_distribution': {
                        'PART_OF_DOC_KEYk': {'docs_count': (1, 1), 'tested_only': set(), 'expected_only': set(),
                                             'same': 1},
                        'VALUE_RELEVANTv': {'docs_count': (1, 1), 'tested_only': set(), 'expected_only': set(),
                                            'same': 1}}}, 'keys': {'common_values': {
            'PART_OF_DOC_KEYk=k1': {'summed_difference_types': {'field_existence'}, 'docs_count': (1, 1),
                                    'field_usage_summary': {'tested_only': {'EXISTENCE_RELEVANTexist2'},
                                                            'expected_only': {'EXISTENCE_RELEVANTexist1'}, 'same': 1},
                                    'common_fields_with_relevant_values_value_distribution': {
                                        'VALUE_RELEVANTv': {'docs_count': (1, 1), 'tested_only': set(),
                                                            'expected_only': set(), 'same': 1}}}},
                                                                   'summary': {'tested_only': set(),
                                                                               'expected_only': set(), 'same': 1}}},result)

    def test_one_doc_different_value_relevant_value(self):
        comparator = CompareDocumentSets(TheDocAnalyzer())
        doce = generate_document('class1', ['k=k1'],['v=v1'],[],[])
        doct = generate_document('class1', ['k=k1'],['v=v2'],[],[])
        summary, result = comparator.run([doce], [doct], "ut_directory", "./tmp")
        self.assertEqual({'summed_difference_types': {'field_values'}, 'docs_count': (1, 1), 'fields': {'summed_difference_types': {'field_values'}, 'docs_count': (1, 1), 'field_usage_summary': {'tested_only': set(), 'expected_only': set(), 'same': 2}, 'common_fields_with_relevant_values_value_distribution': {'PART_OF_DOC_KEYk': {'docs_count': (1, 1), 'tested_only': set(), 'expected_only': set(), 'same': 1}, 'VALUE_RELEVANTv': {'docs_count': (1, 1), 'tested_only': {'v2'}, 'expected_only': {'v1'}, 'same': 0}}}, 'keys': {'common_values': {'PART_OF_DOC_KEYk=k1': {'summed_difference_types': {'field_values'}, 'docs_count': (1, 1), 'field_usage_summary': {'tested_only': set(), 'expected_only': set(), 'same': 1}, 'common_fields_with_relevant_values_value_distribution': {'VALUE_RELEVANTv': {'docs_count': (1, 1), 'tested_only': {'v2'}, 'expected_only': {'v1'}, 'same': 0}}}}, 'summary': {'tested_only': set(), 'expected_only': set(), 'same': 1}}}, result)
        self.assertEqual({'unclassified': {'docs_count': (1, 1), 'summed_difference_types': {'field_values'}}},summary)

    def test_one_doc_different_value_relevant_key(self):
        comparator = CompareDocumentSets(TheDocAnalyzer())
        doce = generate_document('class1', ['k=k1'],['v1=v'],[],[])
        doct = generate_document('class1', ['k=k1'],['v2=v'],[],[])
        summary, result = comparator.run([doce], [doct], "ut_directory", "./tmp")
        self.assertEqual({'summed_difference_types': {'field_existence'}, 'docs_count': (1, 1), 'fields': {'summed_difference_types': {'field_existence'}, 'docs_count': (1, 1), 'field_usage_summary': {'tested_only': {'VALUE_RELEVANTv2'}, 'expected_only': {'VALUE_RELEVANTv1'}, 'same': 1}, 'common_fields_with_relevant_values_value_distribution': {'PART_OF_DOC_KEYk': {'docs_count': (1, 1), 'tested_only': set(), 'expected_only': set(), 'same': 1}}}, 'keys': {'common_values': {'PART_OF_DOC_KEYk=k1': {'summed_difference_types': {'field_existence'}, 'docs_count': (1, 1), 'field_usage_summary': {'tested_only': {'VALUE_RELEVANTv2'}, 'expected_only': {'VALUE_RELEVANTv1'}, 'same': 0}, 'common_fields_with_relevant_values_value_distribution': {}}}, 'summary': {'tested_only': set(), 'expected_only': set(), 'same': 1}}}, result)
        self.assertEqual({'unclassified': {'docs_count': (1, 1), 'summed_difference_types': {'field_existence'}}},summary)

    def test_one_doc_different_key_value(self):
        comparator = CompareDocumentSets(TheDocAnalyzer())
        doce = generate_document('class1', ['k=k1'],['v1=v1'],[],[])
        doct = generate_document('class1', ['k=k2'],['v1=v1'],[],[])
        summary, result = comparator.run([doce], [doct], "ut_directory", "./tmp")
        self.assertEqual({'summed_difference_types': {'field_values', 'content_key_existence'}, 'docs_count': (1, 1), 'fields': {'summed_difference_types': {'field_values'}, 'docs_count': (1, 1), 'field_usage_summary': {'tested_only': set(), 'expected_only': set(), 'same': 2}, 'common_fields_with_relevant_values_value_distribution': {'VALUE_RELEVANTv1': {'docs_count': (1, 1), 'tested_only': set(), 'expected_only': set(), 'same': 1}, 'PART_OF_DOC_KEYk': {'docs_count': (1, 1), 'tested_only': {'k2'}, 'expected_only': {'k1'}, 'same': 0}}}, 'keys': {'common_values': {}, 'summary': {'tested_only': {'PART_OF_DOC_KEYk=k2'}, 'expected_only': {'PART_OF_DOC_KEYk=k1'}, 'same': 0}}}, result)
        self.assertEqual({'unclassified': {'docs_count': (1, 1), 'summed_difference_types': {'field_values', 'content_key_existence'}}},summary)

if __name__ == '__main__':
    unittest.main()
