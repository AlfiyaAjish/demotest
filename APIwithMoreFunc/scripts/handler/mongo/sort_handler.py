from scripts.utils.mongodb_utils import get_mongo_collection
import functools

def get_nested_value(data, nested_key):
    keys = nested_key.split('.')
    for key in keys:
        data = data.get(key, {})
    return data if data != {} else None

def sort_data(sort_input: dict,table_name: str):
    collection = get_mongo_collection(table_name)
    base_data = list(collection.find({}))  # No filtering applied

    if not sort_input:
        return base_data

    sort_fields = list(sort_input.items())  # e.g. [("first_name", "asc"), ("last_name", "desc")]
    reverse_flags = [direction.lower() == "desc" for _, direction in sort_fields]

    def sort_key(doc):
        return tuple(get_nested_value(doc, field) for field, _ in sort_fields)

    def compare_docs(a, b):
        for idx, reverse in enumerate(reverse_flags):
            a_val = sort_key(a)[idx]
            b_val = sort_key(b)[idx]
            if a_val != b_val:
                if reverse:
                    return (b_val > a_val) - (b_val < a_val)
                else:
                    return (a_val > b_val) - (a_val < b_val)
        return 0

    base_data.sort(key=functools.cmp_to_key(compare_docs))
    return base_data
