from fastapi import FastAPI

# Create a FastAPI instance
app = FastAPI(root_path="/hello")

# Define a simple route
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


