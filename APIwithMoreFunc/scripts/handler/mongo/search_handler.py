from scripts.utils.mongodb_utils import get_mongo_collection
from scripts.handler.mongo.filter_handler import filter_data
import functools

def get_nested_value(data, nested_key):
    keys = nested_key.split('.')
    for key in keys:
        data = data.get(key, {})
    return data if data != {} else None

def search_data(search_input: dict, filter_input: dict,table_name: str, sort_input: dict = None,):
    collection = get_mongo_collection(table_name)
    base_data = filter_data(filter_input,table_name) if filter_input else list(collection.find({}))


    def match(doc):
        for key, val in search_input.items():
            if key == "__all__":
                if any(str(v).lower().find(val.lower()) != -1 for v in doc.values()):
                    return True
            elif isinstance(val, list):
                if str(doc.get(key, "")).lower() not in [str(v).lower() for v in val]:
                    return False
            else:
                if val.lower() not in str(doc.get(key, "")).lower():
                    return False
        return True

    filtered_results = list(filter(match, base_data))

    if sort_input:
        sort_fields = list(sort_input.items())
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

        filtered_results.sort(key=functools.cmp_to_key(compare_docs))

    return filtered_results
