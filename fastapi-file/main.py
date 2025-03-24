from fastapi import FastAPI
from scripts.handlers.handler import router as file_router
from scripts.database.database import create_db_and_tables

app = FastAPI(title="FastAPI File Upload Service", version="1.0")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(file_router)
