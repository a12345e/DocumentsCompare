import unittest
import string

from document_sets_compare import CompareDocumentSets
from test_doc_analyzer import TheDocAnalyzer
from document_generator import generate_documents


class MyTestCase(unittest.TestCase):

    def test_something(self):
        comparator = CompareDocumentSets(TheDocAnalyzer())
        docs = generate_documents(0, 1, 1, 1)
        summary = comparator.run(docs, docs, "ut_directory", "./tmp")
        print(summary)


if __name__ == '__main__':
    unittest.main()
