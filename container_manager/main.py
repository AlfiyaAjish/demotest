from fastapi import FastAPI
from scripts.handler import handler

app = FastAPI(title="Docker Container Manager")

app.include_router(handler.router)
