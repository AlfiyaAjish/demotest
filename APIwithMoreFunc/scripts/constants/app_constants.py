ALLOWED_TABLES = {
    "people": "people",
    "companies": "companies",
} # allowed table names, add more if needed
DEFAULT_PAGE = 1    #page number
DEFAULT_LIMIT = 10   # limit per page

# Error messages
ERROR_MESSAGES = {
    "invalid_operation": "Invalid operation type. Choose from: 'search', 'filter', or 'sort'.",
    "empty_filter": "Filter input cannot be empty for 'filter' operation.",
    "empty_search": "Search input cannot be empty for 'search' operation.",
    "empty_sort": "Sort input cannot be empty for 'sort' operation.",
    "invalid_table": "Invalid or missing table name.",
    "database_connection_failed": "Database connection failed",
    "query_execution_failed": "Query execution failed",
    "error_filtering": "error while filtering",
    "invalid_dob": "invalid date of birth format",
    "error_searching": "error while searching",
    "error_sorting": "error while sorting"
}