from fastapi import HTTPException
from scripts.utils.database_utils import run_query
from scripts.constants.app_constants import ERROR_MESSAGES

def filter_data(filter_input: dict, table_name: str, sort_input: dict = None):
    try:
        base_query = f"SELECT * FROM {table_name} WHERE 1=1"
        params = []

        # Filtering
        for key, value in filter_input.items():
            if key == "date_of_birth":
                values = value if isinstance(value, list) else [value]
                date_clauses = []
                for val in values:
                    if val.startswith("____-__-"):
                        date_clauses.append("TO_CHAR(date_of_birth, 'DD') = %s")
                        params.append(val[-2:])
                    elif val.startswith("____-"):
                        date_clauses.append("TO_CHAR(date_of_birth, 'MM') = %s")
                        params.append(val.split("-")[1])
                    elif val.endswith("-__-__"):
                        date_clauses.append("TO_CHAR(date_of_birth, 'YYYY') = %s")
                        params.append(val.split("-")[0])
                    else:
                        date_clauses.append("date_of_birth = %s")
                        params.append(val)
                if date_clauses:
                    base_query += " AND (" + " OR ".join(date_clauses) + ")"
            else:
                if isinstance(value, list):
                    placeholders = ','.join(['%s'] * len(value))
                    base_query += f" AND {key} IN ({placeholders})"
                    params.extend(value)
                else:
                    base_query += f" AND {key} = %s"
                    params.append(value)

        # Sorting
        if sort_input:
            sort_parts = [f"{field} {'DESC' if direction.lower() == 'desc' else 'ASC'}"
                          for field, direction in sort_input.items()]
            base_query += " ORDER BY " + ", ".join(sort_parts)

        return run_query(base_query, tuple(params))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{ERROR_MESSAGES['error_filtering']}: {str(e)}")

