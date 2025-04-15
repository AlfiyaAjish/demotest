from fastapi import APIRouter, Query, Body
from scripts.handlers.cont_handler import *
from scripts.models.cont_model import *
from scripts.constants.api_endpoints import Endpoints
from scripts.logging.logger import logger

container_router = APIRouter()

@container_router.post(Endpoints.CONTAINER_RUN)
def run_container(request: ContainerRunAdvancedRequest):
    logger.info("Running container with basic params")
    return run_container_advanced(request)


@container_router.post(Endpoints.CONTAINER_RUN_ADV)
def run_container_advanced_view(data: ContainerRunAdvancedRequest):
    logger.info("Running container with advanced params")
    return run_container_advanced(data)


@container_router.post(Endpoints.CONTAINER_LIST)
def list_containers_advanced(params: ContainerListRequest):
    logger.info("Listing containers with filters")
    return list_containers_with_filters(params)


@container_router.post(Endpoints.CONTAINER_LOGS)
def get_logs_schema(name: str, params: ContainerLogsRequest = Body(...)):
    logger.info(f"Fetching logs for container: {name}")
    return get_logs_with_params(name, params)


@container_router.post(Endpoints.CONTAINER_STOP)
def stop_container(name: str, timeout: Optional[float] = Query(None, description="Timeout in seconds before force stop")):
    logger.info(f"Stopping container: {name} with timeout={timeout}")
    return stop_container(name, timeout)


@container_router.post(Endpoints.CONTAINER_START)
def start_container(name: str):
    logger.info(f"Starting container: {name}")
    return start_container(name)


@container_router.post(Endpoints.CONTAINER_REMOVE)
def remove_container(name: str, params: ContainerRemoveRequest = Body(...)):
    logger.info(f"Removing container: {name} with params: {params.dict(exclude_unset=True)}")
    return remove_container_with_params(name, params)
