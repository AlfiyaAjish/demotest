# from fastapi import FastAPI
# from scripts.handler import handler
#
# app = FastAPI(title="Docker Container Manager")
#
# app.include_router(handler.router)


from fastapi import FastAPI
from scripts.handler.handler import image_router, container_router, volume_router

app = FastAPI(title="Docker Container Manager")

app.include_router(image_router)
app.include_router(container_router)
app.include_router(volume_router)
