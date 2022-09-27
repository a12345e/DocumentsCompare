from doc_analyzer import DocsAttributesDistribution, AnalyzeDocuments
import string
from enum import Enum


class CompareDocumentSets:
    class DifferenceCases(Enum):
        DOCS_COUNT = 'docs_count'
        FIELD_EXISTENCE = 'field_existence'
        FIELD_DOC_COUNT = 'field_doc_count'
        FIELD_VALUES = 'field_values'

    class Results(Enum):
        DIFFERENCE_TYPES = 'difference_types'
        SAME_DOCS_COUNT = 'same_docs_count'
        DOCS_COUNT_DIFF = 'docs_count_diff'
        TESTED_ONLY = 'tested_only'
        EXPECTED_ONLY = 'expected_only'
        COMMON = 'common'
        SAME = 'same'
        FIELDS = 'fields'

    def __init(self):
        pass

    def compare_analyzed_attributes(self, expected: DocsAttributesDistribution, tested: DocsAttributesDistribution):

        result = {self.Results.DIFFERENCE_TYPES: set()}
        if expected.get_docs_count() == tested.get_docs_count():
            result[self.Results.SAME_DOCS_COUNT] = tested.get_docs_count()
        else:
            result[self.Results.DOCS_COUNT_DIFF] = tuple(expected.get_docs_count(),
                                                         tested.get_docs_count())
            result[CompareDocumentSets.Results.DIFFERENCE_TYPES.value].add(
                CompareDocumentSets.DifferenceCases.DOCS_COUNT.value)
        result[CompareDocumentSets.Results.TESTED_ONLY.value] = tested.get_fields_usage(). \
            difference(expected.get_fields_usage())
        result[CompareDocumentSets.Results.EXPECTED_ONLY.value] = \
            expected.get_fields_usage().difference(tested.get_fields_usage())
        common_fields = expected.get_fields_usage().intersection(tested.get_fields_usage())
        result[self.Results.SAME] = len(common_fields)
        if len(result[self.Results.TESTED_ONLY]) > 0 or len(result[self.Results.EXPECTED_ONLY]) > 0:
            result[CompareDocumentSets.Results.DIFFERENCE_TYPES.value].add(
                CompareDocumentSets.DifferenceCases.FIELD_EXISTENCE.value)
        result_per_field = {}
        for field in common_fields:
            diff = {}
            if tested.get_field_usage(field) == \
                    expected.get_fields_usage(field):
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
        """
         return {
            self.Result.DOCS_COUNT.value: self._count_docs,
            self.Result.FIELD_USAGE.value: self._fields_usage_count,
            self.Result.FIELD_VALUES: self._fields_values
        }

                return {
            self.Results.CLASSIFIER: self._classifier,
            self.Results.DOCS_COUNT_IGNORE: self._count_docs_ignored,
            self.Results.COUNT_DOCS_IGNORE_EMPTY_KEY: self._count_docs_ignored_because_missing_key,
            self.Results.FIELDS: self._build_report[self.Results.FIELDS].get(),
            self.Results.KEYS: key_results
        }

        :param expected:
        :param tested:
        :return:
        """
        result = {self.Results.DIFFERENCE_TYPES: set()}
        if expected.get_docs_count() == tested.get_docs_count():
            result[self.Results.SAME_DOCS_COUNT] = tested.get_docs_count()
        else:
            result[self.Results.DOCS_COUNT_DIFF] = tuple(expected.get_docs_count(), tested.get_docs_count())
        result[self.Results.FIELDS] = self.compare_analyzed_attributes(expected.get_docs_count(), tested.get_fields())

