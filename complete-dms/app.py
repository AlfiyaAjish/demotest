from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scripts.services.image_service import router as image_router
from scripts.services.cont_service import container_router as cont_vol_router
from scripts.services.vol_service import v as cont_vol_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Docker Management API",
        description="APIs to manage Docker Images, Containers and Volumes",
        version="1.0.0",
        root_path="/cdms"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(image_router, prefix="/docker_auth", tags=["Authentication"])
    app.include_router(image_router, prefix="/image", tags=["Image Operations"])
    app.include_router(cont_vol_router, prefix="/container_volume", tags=["Container & Volume Operations"])

    return app