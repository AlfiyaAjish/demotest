from fastapi import FastAPI

# Create a FastAPI instance
app = FastAPI()

# Define a simple route
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}



