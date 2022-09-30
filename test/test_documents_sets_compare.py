import unittest
import string

from document_sets_compare import CompareDocumentSets
from test_doc_analyzer import TheDocAnalyzer
from document_generator import generate_documents

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here
        comparator = CompareDocumentSets(TheDocAnalyzer())
        docs = generate_documents(0,1,1,1,1)
        comparator.run()


if __name__ == '__main__':
    unittest.main()
