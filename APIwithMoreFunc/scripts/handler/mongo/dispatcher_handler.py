from scripts.handler.mongo.filter_handler import filter_data
from scripts.handler.mongo.search_handler import search_data
from scripts.handler.mongo.sort_handler import sort_data
from scripts.utils.pagination import paginate
from fastapi import HTTPException
from scripts.constants.app_constants import ERROR_MESSAGES, DEFAULT_PAGE, DEFAULT_LIMIT,ALLOWED_TABLES
from scripts.utils.serialization import serialize_documents

def dispatch_operation_mongo(payload: dict):
    op = payload.get("operation")
    table = payload.get("table")
    if not table or table not in ALLOWED_TABLES:
        raise HTTPException(status_code=400, detail=ERROR_MESSAGES["invalid_table"])
    table_name = ALLOWED_TABLES[table]
    page = payload.get("page", DEFAULT_PAGE)
    limit = payload.get("limit", DEFAULT_LIMIT)
    filter_input = payload.get("filter_input", {})
    search_input = payload.get("search_input", {})
    sort_input = payload.get("sort_input", {})

    # dispatcher = {
    #     "filter": lambda: filter_data(filter_input,table_name, sort_input,),
    #     "search": lambda: search_data(search_input, filter_input,table_name,sort_input,),
    #     "sort":   lambda: sort_data(sort_input,table_name),
    # }
    #
    # if op not in dispatcher:
    #     raise HTTPException(status_code=400, detail=ERROR_MESSAGES["invalid_operation"])
    #
    # raw_data = dispatcher[op]()
    # serialized_data = serialize_documents(raw_data)
    # return paginate(serialized_data, page, limit)

    dispatcher = {
        "filter": lambda: _run_filter(filter_input,table_name, sort_input),
        "search": lambda: _run_search(search_input, filter_input,table_name,sort_input),
        "sort":   lambda: _run_sort(sort_input,table_name),
    }

    if op not in dispatcher:
        raise HTTPException(status_code=400, detail=ERROR_MESSAGES["invalid_operation"])

    raw_data = dispatcher[op]()
    serialized_data = serialize_documents(raw_data)
    return paginate(serialized_data, page, limit)

def _run_filter(filter_input, sort_input,table_name):
    if not filter_input:
        raise HTTPException(status_code=400, detail=ERROR_MESSAGES["empty_filter"])
    return filter_data(filter_input, table_name, sort_input)

def _run_search(search_input, filter_input, sort_input,table_name):
    if not search_input:
        raise HTTPException(status_code=400, detail=ERROR_MESSAGES["empty_search"])
    return search_data(search_input, filter_input, sort_input,table_name)

def _run_sort(sort_input, table_name):
    if not sort_input:
        raise HTTPException(status_code=400, detail=ERROR_MESSAGES["empty_sort"])
    return sort_data(sort_input, table_name)



