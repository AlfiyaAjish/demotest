# APIwithMoreFunc

FastAPI-based backend that allows flexible data operations such as **filtering**, **searching**, **sorting**, and **paginated retrieval** on both **PostgreSQL** and **MongoDB**. It also supports **CSV upload** to create or update database tables.

---

## Features

### Unified Multi-Functional Endpoint
- One endpoint supports **filtering**, **searching**, **sorting**, or any combination.
- Uses a **dispatcher pattern** to dynamically route operations based on request input.

## Operations

### Search
Search can be performed alone or combined with filter and sort operations.

#### Global Search
Searches the input value across the entire table.

**Example:**
"search_input": { "`__all__`": "value" }

## inputs
you can provide multiple input values for both search and filter operations.
- Single value (field-specific):
> *Example:* 
> - "search_input": { "field_name": "value" }
- Multiple values for a field:
> *Example:* 
> - "search_input": { "field_name": ["v1", "v2"] }
- Multiple fields with values:
> *Example:* 
> -"search_input": {
  "field_name1": ["value1.1", "value1.2"],
  "field_name2": "value2"
}
- Ascending or Descending sort on a field:
> *Example:* 
> -"sort_input": { "field_name": "asc" }

### Pattern Matching in Date Fields (Search)
- Flexible search on `date_of_birth` using partials:
  - `YYYY-MM-__` (match by month)
  - `YYYY-__-DD` (match by day in a year)
  - `____-MM-DD` (match by month + day across all years)
  - `YYYY-__-__`
  - `____-MM-__`
  - `____-__-DD`

### ✅ Multi-Database Support
- PostgreSQL: Filtering, searching, sorting, uploading.
- MongoDB: Filtering, searching, sorting,uploading

###  CSV Uploading
- Upload CSV files to:
  - Create new PostgreSQL or MongoDB collections.
  - Update existing ones.
- Choose whether to **create a new table/collection** or append to an existing one.
- Automatically infers schema for PostgreSQL using column names as `TEXT`.

###  Pagination Support
-  Includes `limit`, `page`, `total`, and `total_pages` in every response.

> TABLE COLUMNS
> - user_id
> - first_name
> - last_name
> - sex
> - email
> - phone
> - job_title
> - date_of_birth