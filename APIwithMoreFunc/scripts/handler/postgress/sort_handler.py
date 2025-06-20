from fastapi import HTTPException
from scripts.utils.database_utils import run_query
from scripts.constants.app_constants import ERROR_MESSAGES

def sort_data(table_name: str, sort_input: dict):
    try:
        if not sort_input:
            raise HTTPException(status_code=400, detail="Missing sort input")

        query = f"SELECT * FROM {table_name}"
        sort_parts = [f"{field} {'DESC' if direction.lower() == 'desc' else 'ASC'}"
                      for field, direction in sort_input.items()]
        query += " ORDER BY " + ", ".join(sort_parts)

        return run_query(query)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{ERROR_MESSAGES['error_sorting']}: {str(e)}")
