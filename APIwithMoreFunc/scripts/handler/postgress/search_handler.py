from fastapi import HTTPException
from scripts.handler.postgress.filter_handler import filter_data
from scripts.utils.database_utils import run_query
from scripts.constants.app_constants import ERROR_MESSAGES

def search_data(search_input: dict, filter_input: dict, sort_input: dict, table_name: str):
    try:
        data = filter_data(filter_input, table_name,sort_input) if filter_input else run_query(f"SELECT * FROM {table_name}")
        if not search_input:
            return data

        def match(record):
            for key, val in search_input.items():
                if key == "__all__":
                    if any(str(v).lower().find(str(val).lower()) != -1 for v in record.values()):
                        return True

                elif key == "date_of_birth":
                    dob = str(record.get("date_of_birth", ""))
                    if not dob:
                        return False

                    val_str = str(val)

                    # Full exact match YYYY-MM-DD
                    if val_str.count("-") == 2 and "__" not in val_str and "____" not in val_str:
                        if dob != val_str:
                            return False

                    elif val_str.endswith("-__") and val_str.count("-") == 2 and "____" not in val_str:
                        if not dob.startswith(val_str[:7]):
                            return False

                    # YYYY-__-DD (match year and day)
                    elif val_str[4:6] == "__" and val_str.count("-") == 2:
                        year = val_str[:4]
                        day = val_str[-2:]
                        if not (dob.startswith(year) and dob.endswith(f"-{day}")):
                            return False

                    elif val_str.startswith("____-") and val_str.count("-") == 2:
                        mm_dd = val_str[5:]
                        if not dob.endswith(mm_dd):
                            return False

                    elif val_str.endswith("-__-__"):
                        if not dob.startswith(val_str[:4]):
                            return False

                    elif val_str.startswith("____-") and val_str.endswith("-__"):
                        month = val_str[5:7]
                        if dob.split("-")[1] != month:
                            return False

                    elif val_str.startswith("____-__-"):
                        day = val_str[-2:]
                        if dob.split("-")[2] != day:
                            return False

                    else:
                        return False

                elif isinstance(val, list):
                    if str(record.get(key, "")).lower() not in [str(v).lower() for v in val]:
                        return False

                else:
                    if str(val).lower() not in str(record.get(key, "")).lower():
                        return False

            return True
        return list(filter(match, data))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{ERROR_MESSAGES['error_searching']}: {str(e)}")
