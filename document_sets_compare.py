from doc_analyzer import DocsAttributesDistribution
import string
from enum import Enum


class CompareDocumentSets:
    class DifferenceCases(Enum):
        DOCS_COUNT = 'docs_count'
        FIELD_EXISTENCE = 'field_existence'
        FIELD_DOC_COUNT = 'field_doc_count'
        FIELD_VALUES = 'field_values'

    class ReportKeys(Enum):
        DIFFERENCE_TYPES = 'difference_types'
        TESTED_ONLY = 'tested_only'
        EXPECTED_ONLY = 'tested_only'

    def __init(self, verbose=True):
        self._verbose = verbose

    @staticmethod
    def compare_attributes(expected, tested):
        result = {'differences_types': set()}
        if expected[DocsAttributesDistribution.Result.DOCS_COUNT.value] == \
                tested[DocsAttributesDistribution.Result.DOCS_COUNT.value]:
            result['same_docs_number'] = tested[DocsAttributesDistribution.Result.DOCS_COUNT.value]
        else:
            result['docs_number'] = tuple(expected[DocsAttributesDistribution.Result.DOCS_COUNT.value],
                                          tested[DocsAttributesDistribution.Result.DOCS_COUNT.value])
            result[CompareDocumentSets.ReportKeys.DIFFERENCE_TYPES.value].add(
                CompareDocumentSets.DifferenceCases.DOCS_COUNT.value)
        result[CompareDocumentSets.ReportKeys.TESTED_ONLY.value] = set(tested[DocsAttributesDistribution.Result.FIELDS_USAGE].keys()). \
            difference(set(expected[DocsAttributesDistribution.Result.FIELDS_USAGE].keys()))
        result[CompareDocumentSets.ReportKeys.EXPECTED_ONLY.value] = set(expected[DocsAttributesDistribution.Result.FIELDS_USAGE].keys()). \
            difference(set(tested[DocsAttributesDistribution.Result.FIELDS_USAGE].keys()))
        result['common_fields'] = set(tested[DocsAttributesDistribution.Result.FIELDS_USAGE].keys()). \
            intersection(set(tested[DocsAttributesDistribution.Result.FIELDS_USAGE].keys()))
        if len(result['tested_only_fields']) > 0 or len(result['expected_only_fields']) > 0:
            result[CompareDocumentSets.ReportKeys.DIFFERENCE_TYPES.value].add(
                CompareDocumentSets.DifferenceCases.FIELD_EXISTENCE.value)
        result_per_field = {}
        for field in result['common_fields']:
            diff = {}
            if tested[DocsAttributesDistribution.Result.FIELDS_USAGE][field] == \
                    expected[DocsAttributesDistribution.Result.FIELDS_USAGE][field]:
                diff['same_docs_count'] = expected[DocsAttributesDistribution.Result.FIELDS_USAGE][field]
            else:
                diff['docs_count'] = tuple(expected[DocsAttributesDistribution.Result.FIELDS_USAGE][field],
                                           tested[DocsAttributesDistribution.Result.FIELDS_USAGE][field])
                result[CompareDocumentSets.ReportKeys.DIFFERENCE_TYPES.value]. \
                    add(CompareDocumentSets.DifferenceCases.FIELD_DOC_COUNT.value)
            diff[CompareDocumentSets.ReportKeys.TESTED_ONLY.value] = set(tested[DocsAttributesDistribution.Result.FIELD_VALUES][field]). \
                difference(set(expected[DocsAttributesDistribution.Result.FIELD_VALUES][field]))
            diff[CompareDocumentSets.ReportKeys.EXPECTED_ONLY.value] = set(expected[DocsAttributesDistribution.Result.FIELD_VALUES][field]). \
                difference(set(tested[DocsAttributesDistribution.Result.FIELD_VALUES][field]))
            diff['same_values_count'] = len(
                set(expected[DocsAttributesDistribution.Result.FIELD_VALUES][field]).
                intersection(set(tested[DocsAttributesDistribution.Result.FIELD_VALUES][field])))
            if len(diff[CompareDocumentSets.ReportKeys.TESTED_ONLY.value])> 0 or len(diff[CompareDocumentSets.ReportKeys.TESTED_ONLY.value]) > 0:
                result[CompareDocumentSets.ReportKeys.DIFFERENCE_TYPES.value]. \
                    add(CompareDocumentSets.DifferenceCases.FIELD_VALUES.value)
            result_per_field[field] = diff
        result['fields'] = result_per_field
        return result
