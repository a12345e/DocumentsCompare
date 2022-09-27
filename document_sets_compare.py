from doc_analyzer import DocsAttributesDistribution, AnalyzeDocuments, DocAnalyzer
import string
import os
from enum import Enum


class CompareDocumentSets:
    class DifferenceCases(Enum):
        DOCS_COUNT = 'docs_count'
        FIELD_EXISTENCE = 'field_existence'
        KEY_EXISTENCE = 'content_key_existence'
        FIELD_DOC_COUNT = 'field_doc_count'
        FIELD_VALUES = 'field_values'

    class Results(Enum):
        DIFFERENCE_TYPES = 'difference_types'
        DOCS_COUNT = 'docs_count'
        TESTED_ONLY = 'tested_only'
        EXPECTED_ONLY = 'expected_only'
        COMMON = 'common'
        SAME = 'same'
        FIELDS = 'fields'
        KEYS = 'keys'

    def __init__(self):
        self._result = None

    def __init(self, analyzer: DocAnalyzer):
        self._analyzer = analyzer
        pass

    def compare_analyzed_attributes(self, expected: DocsAttributesDistribution, tested: DocsAttributesDistribution):
        result = {self.Results.DIFFERENCE_TYPES: set(), self.Results.DOCS_COUNT: tuple(expected.get_docs_count(),
                                                                                       tested.get_docs_count())}
        if [self.Results.DOCS_COUNT][0] != [self.Results.DOCS_COUNT][1]:
            result[CompareDocumentSets.Results.DIFFERENCE_TYPES.value].add(
                CompareDocumentSets.DifferenceCases.DOCS_COUNT.value)
        result[CompareDocumentSets.Results.TESTED_ONLY.value] = tested.get_fields_used(). \
            difference(expected.get_fields_used())
        result[CompareDocumentSets.Results.EXPECTED_ONLY.value] = \
            expected.get_fields_used().difference(tested.get_fields_used())
        common_fields = expected.get_fields_used().intersection(tested.get_fields_used())
        result[self.Results.SAME] = len(common_fields)
        if len(result[self.Results.TESTED_ONLY]) > 0 or len(result[self.Results.EXPECTED_ONLY]) > 0:
            result[CompareDocumentSets.Results.DIFFERENCE_TYPES.value].add(
                CompareDocumentSets.DifferenceCases.FIELD_EXISTENCE.value)
        result_per_field = {}
        for field in common_fields:
            diff = {}
            if tested.get_field_usage(field) == \
                    expected.get_fields_used(field):
                diff[self.Results.SAME_DOCS_COUNT] = expected.get_field_usage(field)
            else:
                diff[self.Results.DOCS_COUNT] = tuple(expected.get_field_usage(field),
                                                      tested.get_field_usage(field))
                result[CompareDocumentSets.Results.DIFFERENCE_TYPES.value]. \
                    add(CompareDocumentSets.DifferenceCases.FIELD_DOC_COUNT.value)
            diff[CompareDocumentSets.Results.TESTED_ONLY.value] = \
                tested.get_field_values(field).difference(expected.get_field_values(field))
            diff[CompareDocumentSets.Results.EXPECTED_ONLY.value] = \
                expected.get_field_values(field).difference(tested.get_field_values(field))
            diff[self.Results.SAME] = len(expected.get_field_values(field).
                                          intersection(tested.get_field_values(field)))
            if len(diff[CompareDocumentSets.Results.EXPECTED_ONLY_ONLY.value]) > 0 or len(
                    diff[CompareDocumentSets.Results.TESTED_ONLY.value]) > 0:
                result[CompareDocumentSets.Results.DIFFERENCE_TYPES.value]. \
                    add(CompareDocumentSets.DifferenceCases.FIELD_VALUES.value)
            result_per_field[field] = diff
        result[self.Results.FIELDS] = result_per_field
        return result

    def compare_analysed_document_sets(self, expected: AnalyzeDocuments, tested: AnalyzeDocuments):
        result = {self.Results.DIFFERENCE_TYPES: set(), self.Results.DOCS_COUNT: tuple(expected.get_docs_count(),
                                                                                       tested.get_docs_count())}
        if [self.Results.DOCS_COUNT][0] != [self.Results.DOCS_COUNT][1]:
            result[CompareDocumentSets.Results.DIFFERENCE_TYPES.value].add(
                CompareDocumentSets.DifferenceCases.DOCS_COUNT.value)
        result[self.Results.FIELDS] = self.compare_analyzed_attributes(expected.get_docs_count(), tested.get_fields())
        result[self.Results.DIFFERENCE_TYPES] = \
            result[self.Results.DIFFERENCE_TYPES].union(result[self.Results.FIELDS][self.Results.DIFFERENCE_TYPES])
        result[CompareDocumentSets.Results.TESTED_ONLY.value] = tested.get_keys(). \
            difference(expected.get_keys())
        result[CompareDocumentSets.Results.EXPECTED_ONLY.value] = expected.get_keys().difference(tested.get_keys())
        common_keys = expected.get_keys().intersection(tested.get_key())
        result[self.Results.SAME] = len(common_keys)
        if len(result[self.Results.TESTED_ONLY]) > 0 or len(result[self.Results.EXPECTED_ONLY]) > 0:
            result[CompareDocumentSets.Results.DIFFERENCE_TYPES.value].add(
                CompareDocumentSets.DifferenceCases.KEY_EXISTENCE.value)
        result[self.Results.KEYS] = {}
        for key in common_keys:
            result[self.Results.KEYS][key] = self.compare_analyzed_attributes(expected.get_keys(key),
                                                                              tested.get_key(key))
            result[self.Results.DIFFERENCE_TYPES] = \
                result[self.Results.DIFFERENCE_TYPES].union(
                    result[self.Results.KEYS][key][self.Results.DIFFERENCE_TYPES])
        return result

    def compare(self, expected: [dict], tested: [dict], classifier: string):
        expected_4_classifier = filter(lambda x: classifier == self._analyzer.get_classifier(x), expected)
        tested_4_classifier = filter(lambda x: classifier == self._analyzer.get_classifier(x), tested)
        return self.compare_analysed_document_sets(expected_4_classifier, tested_4_classifier)

    def compare(self, expected: [dict], tested: [dict]):
        self._result = {}
        classifiers = set(map(lambda x: self._analyzer.get_classifier(x), expected))
        expected_not_ignored = map(lambda x: not self._analyzer.doc_ignored(x), expected)
        tested_not_ignored = map(lambda x: not self._analyzer.doc_ignored(x), tested)
        for classifier in classifiers:
            self._result[classifier] = self.compare(expected_not_ignored, tested_not_ignored, classifier)
        return self._result

    def run(self, expected: [dict], tested: [dict], ut: string, root_dir: string):
        result = self.compare(expected, tested)
        print(ut)
        for key in result.keys():
            file_name = os.path.join(root_dir, ut, key+'.compare.txt')
            print('\t', file_name)
            with open(file_name, 'w') as f:
                f.write(result[key])
            print('\t\tcount=', result[key][self.Results.DOCS_COUNT])
            print('\t\tdifference:', result[key][self.Results.DIFFERENCE_TYPES])
        return result
