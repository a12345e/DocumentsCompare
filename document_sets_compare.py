from doc_analyzer import DocsAttributesDistribution, AnalyzeDocuments, DocAnalyzer
import string
import os
from enum import Enum


def pretty(d, indent=0):
    str_value = ''
    jump = '  '
    for key, value in d.items():
        str_value += (jump * indent) + str(key) + ': '
        if isinstance(value, dict):
            str_value += '\n' + pretty(value, indent + 1)
        else:
            str_value += str(value) + '\n'
    return str_value


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

    def __init__(self, analyzer: DocAnalyzer):
        self._analyzer = analyzer

    def compare_analyzed_attributes(self, expected: DocsAttributesDistribution, tested: DocsAttributesDistribution):
        result = {
            self.Results.DIFFERENCE_TYPES.value: set(),
            self.Results.DOCS_COUNT.value: tuple([expected.get_docs_count(),
                                            tested.get_docs_count()])
        }
        if result[self.Results.DOCS_COUNT.value][0] != result[self.Results.DOCS_COUNT.value][1]:
            result[CompareDocumentSets.Results.DIFFERENCE_TYPES.value].add(
                CompareDocumentSets.DifferenceCases.DOCS_COUNT.value)
        result[CompareDocumentSets.Results.TESTED_ONLY.value] = tested.get_fields_used(). \
            difference(expected.get_fields_used())
        result[CompareDocumentSets.Results.EXPECTED_ONLY.value] = \
            expected.get_fields_used().difference(tested.get_fields_used())
        common_fields = expected.get_fields_used().intersection(tested.get_fields_used())
        result[self.Results.SAME.value] = len(common_fields)
        if len(result[CompareDocumentSets.Results.TESTED_ONLY.value]) > 0 or \
                len(result[CompareDocumentSets.Results.EXPECTED_ONLY.value]) > 0:
            result[CompareDocumentSets.Results.DIFFERENCE_TYPES.value].add(
                CompareDocumentSets.DifferenceCases.FIELD_EXISTENCE.value)
        result_per_field = {}
        for field in common_fields:
            diff = {}
            diff[self.Results.DOCS_COUNT.value] = tuple([expected.get_field_usage(field),
                                                         tested.get_field_usage(field)])
            if tested.get_field_usage(field) != \
                    expected.get_field_usage(field):
                result[CompareDocumentSets.Results.DIFFERENCE_TYPES.value]. \
                    add(CompareDocumentSets.DifferenceCases.FIELD_DOC_COUNT.value)
            diff[CompareDocumentSets.Results.TESTED_ONLY.value] = \
                tested.get_field_values(field).difference(expected.get_field_values(field))
            diff[CompareDocumentSets.Results.EXPECTED_ONLY.value] = \
                expected.get_field_values(field).difference(tested.get_field_values(field))
            diff[self.Results.SAME.value] = len(expected.get_field_values(field).
                                                intersection(tested.get_field_values(field)))
            if len(diff[CompareDocumentSets.Results.EXPECTED_ONLY.value]) > 0 or len(
                    diff[CompareDocumentSets.Results.TESTED_ONLY.value]) > 0:
                result[CompareDocumentSets.Results.DIFFERENCE_TYPES.value]. \
                    add(CompareDocumentSets.DifferenceCases.FIELD_VALUES.value)
            result_per_field[field] = diff
        result[self.Results.FIELDS.value] = result_per_field
        return result

    def compare_analyzed_document_sets(self, expected: AnalyzeDocuments, tested: AnalyzeDocuments):
        result = {self.Results.DIFFERENCE_TYPES.value: set(),
                  self.Results.DOCS_COUNT.value: tuple([expected.get_docs_count(),
                                                        tested.get_docs_count()])}
        if result[self.Results.DOCS_COUNT.value][0] != result[self.Results.DOCS_COUNT.value][1]:
            result[self.Results.DIFFERENCE_TYPES.value].add(
                self.DifferenceCases.DOCS_COUNT.value)
        result[self.Results.FIELDS.value] = self.compare_analyzed_attributes(expected.get_fields(), tested.get_fields())
        result[self.Results.DIFFERENCE_TYPES.value] = \
            result[self.Results.DIFFERENCE_TYPES.value].union(
                result[self.Results.FIELDS.value][self.Results.DIFFERENCE_TYPES.value])
        result[CompareDocumentSets.Results.TESTED_ONLY.value] = tested.get_keys(). \
            difference(expected.get_keys())
        result[CompareDocumentSets.Results.EXPECTED_ONLY.value] = expected.get_keys().difference(tested.get_keys())
        common_keys = expected.get_keys().intersection(tested.get_keys())
        result[self.Results.SAME.value] = len(common_keys)
        if len(result[self.Results.TESTED_ONLY.value]) > 0 or len(result[self.Results.EXPECTED_ONLY.value]) > 0:
            result[CompareDocumentSets.Results.DIFFERENCE_TYPES.value].add(
                CompareDocumentSets.DifferenceCases.KEY_EXISTENCE.value)
        result[self.Results.KEYS.value] = {}
        for key in common_keys:
            result[self.Results.KEYS.value][key] = self.compare_analyzed_attributes(expected.get_key(key),
                                                                                    tested.get_key(key))
            result[self.Results.DIFFERENCE_TYPES.value] = \
                result[self.Results.DIFFERENCE_TYPES.value].union(
                    result[self.Results.KEYS.value][key][self.Results.DIFFERENCE_TYPES.value])
        return result

    def run(self, expected: [dict], tested: [dict], ut: string, root_dir: string):
        classifiers = set(map(lambda x: self._analyzer.get_classifier(x), expected))
        summary = {}
        ut_dir = os.path.join(root_dir, ut)
        os.makedirs(ut_dir, exist_ok=True)
        for classifier in classifiers:
            summary[classifier] = {}
            expected_analyzed = AnalyzeDocuments(self._analyzer,
                                                 filter(lambda x:
                                                        not self._analyzer.doc_ignored(x) and
                                                        self._analyzer.get_classifier(x) == classifier, expected)
                                                 )
            file_name = os.path.join(ut_dir, classifier + '.expected_analyzed.txt')
            print('\t', file_name)
            with open(file_name, 'w') as f:
                tmp = expected_analyzed.get()
                f.write(pretty(expected_analyzed.get(), 0))
            tested_analyzed = AnalyzeDocuments(self._analyzer,
                                               filter(lambda x:
                                                      not self._analyzer.doc_ignored(x) and
                                                      self._analyzer.get_classifier(x) == classifier, tested)
                                               )
            file_name = os.path.join(ut_dir, classifier + '.tested_analyzed.txt')
            print('\t', file_name)
            with open(file_name, 'w') as f:
                f.write(pretty(tested_analyzed.get(), 0))
            result = self.compare_analyzed_document_sets(expected_analyzed, tested_analyzed)
            file_name = os.path.join(ut_dir, classifier + '.compare.txt')
            print('\t', file_name)
            with open(file_name, 'w') as f:
                f.write(pretty(result, 0))
            summary[classifier][self.Results.DOCS_COUNT.value] = result[self.Results.DOCS_COUNT.value]
            summary[classifier][self.Results.DIFFERENCE_TYPES.value] = result[self.Results.DIFFERENCE_TYPES.value]
            print(pretty(summary, 1))
        return summary
