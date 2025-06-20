from fastapi import APIRouter, Body
from scripts.models.models import QueryRequest
from scripts.handler.postgress.dispatcher_handler import dispatch_operation
from scripts.handler.mongo.dispatcher_handler import dispatch_operation_mongo
from fastapi import UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from scripts.handler.bulk_update.db_postgres import upload_to_postgres
from scripts.handler.bulk_update.db_mongo import upload_to_mongo
import pandas as pd
import io
router = APIRouter()

# @router.post("/records")
# def handle_query(request: QueryRequest):
#     return dispatch_operation(request.dict())

@router.post("/records")
def handle_query(
    request: QueryRequest = Body(
        ...,
        example={
            "table": "table_name",
            "operation": "operation name(search,filter,sort)",
            "filter_input": { "field_name1": ["value1.1","value1.2"],"field_name2":"value2" },
            "search_input": { "field_name": "value" },
            "sort_input": { "field_name": "(asc or desc)" },
            "page": 1,
            "limit": 10
        }
    )
):
    return dispatch_operation(request.dict())

@router.post("/mongo-records")
def handle_query(request: QueryRequest = Body(
        ...,
        example={
            "table": "table_name",
            "operation": "operation name(search,filter,sort)",
            "filter_input": { "field_name1": ["value1.1","value1.2"],"field_name2":"value2" },
            "search_input": { "field_name": "value" },
            "sort_input": { "field_name": "(asc or desc)" },
            "page": 1,
            "limit": 10
        }
    )
):
    return dispatch_operation_mongo(request.dict())


@router.post("/upload-csv/")
async def upload_csv(
        file: UploadFile,
        db_type: str = Form(..., description="mongo or postgres"),
        table_name: str = Form(..., description="Target table or collection name"),
        create_new: bool = Form(..., description="True = create new, False = insert into existing"),
):
    try:
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed.")

        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))

        if df.empty:
            raise HTTPException(status_code=400, detail="CSV is empty.")

        if db_type == "postgres":
            upload_to_postgres(df, table_name, create_new)
        elif db_type == "mongo":
            upload_to_mongo(df, table_name, create_new)
        else:
            raise HTTPException(status_code=400, detail="db_type must be 'mongo' or 'postgres'")

        return JSONResponse(content={"message": f"Uploaded to {db_type} successfully."})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))