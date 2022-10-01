import string
from doc_analyzer import AttributeImportance


def add_attribute(doc, prefix: string , attr: string):
    doc[prefix+attr.split('=')[0]] = attr.split('=')[1]


def generate_document(classifier: string,
                      keys: [string],
                      values: [string],
                      exists: [string],
                      garbage: [string]
                       ) -> dict:
    doc = {}
    if classifier:
        doc['classifer'] = classifier
    for attr in keys:
        add_attribute(doc, AttributeImportance.PART_OF_DOC_KEY.name, attr)
    for attr in values:
        add_attribute(doc, AttributeImportance.VALUE_RELEVANT.name, attr)
    for attr in exists:
        add_attribute(doc, AttributeImportance.EXISTENCE_RELEVANT.name, attr)
    for attr in garbage:
        add_attribute(doc, AttributeImportance.NOT_RELEVANT.name, attr)
    return doc
