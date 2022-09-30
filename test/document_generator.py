import string
from doc_analyzer import AttributeImportance


def set_attribute(docs: [dict], name, value):
    for doc in docs:
        doc[name] = value


def generate_documents(start_index: int,
                       keys_count: int,
                       other_name_per_key: int,
                       other_value_per_name: int,
                       ):
    docs = []
    for i in range(start_index, keys_count+start_index):
        key_name = AttributeImportance.PART_OF_DOC_KEY.name
        key_value = 'key_value_' + str(i)
        doc = {
            key_name: key_value,
        }
        for name_index in range(start_index, other_name_per_key+start_index):
            value_relevant_name = AttributeImportance.VALUE_RELEVANT.name + str(name_index)
            exist_relevant_name = AttributeImportance.EXISTENCE_RELEVANT.name + str(name_index)
            for value_index in range(start_index,other_value_per_name+start_index):
                value_relevant_value = AttributeImportance.VALUE_RELEVANT.name + '_v_' + str(value_index)
                exist_relevant_value = AttributeImportance.EXISTENCE_RELEVANT.name + '_v_' + str(value_index)
                tmp_doc = dict(doc)
                tmp_doc[value_relevant_name] = value_relevant_value
                tmp_doc[exist_relevant_name] = exist_relevant_value
                docs.append(tmp_doc)
    return docs
