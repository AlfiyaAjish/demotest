from fastapi import HTTPException
from scripts.constants.app_constants import ALLOWED_TABLES,ERROR_MESSAGES,DEFAULT_LIMIT,DEFAULT_PAGE
from scripts.handler.postgress.filter_handler import filter_data
from scripts.handler.postgress.search_handler import search_data
from scripts.handler.postgress.sort_handler import sort_data
from scripts.utils.pagination import paginate


def dispatch_operation(payload: dict):
    table = payload.get("table")
    if not table or table not in ALLOWED_TABLES:
        raise HTTPException(status_code=400, detail=ERROR_MESSAGES["invalid_table"])

    table_name = ALLOWED_TABLES[table]

    op = payload.get("operation")
    page = payload.get("page", DEFAULT_PAGE)
    limit = payload.get("limit", DEFAULT_LIMIT)
    filter_input = payload.get("filter_input", {})
    search_input = payload.get("search_input", {})
    sort_input = payload.get("sort_input", {})


    dispatcher = {
        "filter": lambda: _run_filter(filter_input, sort_input,table_name),
        "search": lambda: _run_search(search_input, filter_input, sort_input,table_name),
        "sort":   lambda: _run_sort(sort_input, table_name),
    }

    if op not in dispatcher:
        raise HTTPException(status_code=400, detail=ERROR_MESSAGES["invalid_operation"])

    data = dispatcher[op]()
    return paginate(data, page, limit)

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



