import unittest


from document_sets_compare import CompareDocumentSets
from test_doc_analyzer import TheDocAnalyzer
from document_generator import generate_document


class MyTestCase(unittest.TestCase):

    def test_one_same_doc(self):
        comparator = CompareDocumentSets(TheDocAnalyzer())
        doc = generate_document('class1', ['k=k1'],['v=v1'],['exist=exist1'],['garbage=g1'])
        summary = comparator.run([doc], [doc], "ut_directory", "./tmp")
        print(summary)

    def test_one_doc_different_garbage_value(self):
        comparator = CompareDocumentSets(TheDocAnalyzer())
        doce = generate_document('class1', ['k=k1'],['v=v1'],['exist=exist1'],['garvage=g1'])
        doct = generate_document('class1', ['k=k1'],['v=v1'],['exist=exist1'],['garbage=21'])
        summary = comparator.run([doce], [doct], "ut_directory", "./tmp")
        print(summary)


if __name__ == '__main__':
    unittest.main()
