from fastapi import FastAPI
from scripts.service import service
import uvicorn

app = FastAPI()
app.include_router(service.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)