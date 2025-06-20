from fastapi import HTTPException
from datetime import datetime
from scripts.utils.mongodb_utils import get_mongo_collection
from scripts.constants.app_constants import ERROR_MESSAGES

def filter_data(filter_input: dict, table_name: str, sort_input: dict = None):
    try:
        collection = get_mongo_collection(table_name)
        query = {}
        expr_conditions = []

        for key, value in filter_input.items():
            if key == "date_of_birth":
                values = value if isinstance(value, list) else [value]
                for val in values:
                    try:
                        if val.startswith("____-__-"):
                            day = int(val[-2:])
                            expr_conditions.append({"$eq": [{"$dayOfMonth": "$date_of_birth"}, day]})
                        elif val.startswith("____-"):
                            month = int(val.split("-")[1])
                            expr_conditions.append({"$eq": [{"$month": "$date_of_birth"}, month]})
                        elif val.endswith("-__-__"):
                            year = int(val.split("-")[0])
                            expr_conditions.append({"$eq": [{"$year": "$date_of_birth"}, year]})
                        else:
                            parsed = datetime.strptime(val, "%Y-%m-%d")
                            query.setdefault("date_of_birth", {"$in": []})["$in"].append(parsed)
                    except Exception:
                        raise HTTPException(status_code=400, detail=f"{ERROR_MESSAGES['invalid_dob']}: {str(e)}")
            else:
                query[key] = {"$in": value} if isinstance(value, list) else value


        if expr_conditions:
            query["$expr"] = {"$or": expr_conditions} if len(expr_conditions) > 1 else expr_conditions[0]

        sort_fields = []
        if sort_input:
            for field, direction in sort_input.items():
                sort_fields.append((field, 1 if direction.lower() == "asc" else -1))

        cursor = collection.find(query)
        if sort_fields:
            cursor = cursor.sort(sort_fields)

        return list(cursor)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{ERROR_MESSAGES['error_filtering']}: {str(e)}")



