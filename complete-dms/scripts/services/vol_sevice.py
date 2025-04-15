from fastapi import APIRouter, Body, Path
from scripts.handlers.vol_handler import *
from scripts.models.volume_model import *
from scripts.constants.api_endpoints import Endpoints
from scripts.logging.logger import logger

volume_router = APIRouter()


@volume_router.post(Endpoints.VOLUME_CREATE)
def create_volume_advanced(
    data: VolumeCreateRequest = Body(...),
):
    logger.info(f"Creating volume with params: {data.dict(exclude_unset=True)}")
    return create_volume_with_params(data)


@volume_router.delete(Endpoints.VOLUME_DELETE)
def delete_volume(
    name: str = Path(..., description="Name of the Docker volume"),
    params: VolumeRemoveRequest = Body(...)
):
    logger.info(f"Deleting volume '{name}' with options: {params.dict(exclude_unset=True)}")
    return remove_volume_with_params(name, params)


