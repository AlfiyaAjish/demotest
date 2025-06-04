from fastapi import FastAPI
from app.k8s_client import list_pods

app = FastAPI()

@app.get("/pods")
def get_pods():
    return list_pods()
