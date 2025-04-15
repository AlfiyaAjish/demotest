from fastapi import APIRouter, Query, Body
from scripts.handlers.image_handler import *
from scripts.models.image_model import *
from scripts.constants.api_endpoints import Endpoints
from scripts.logging.logger import logger

image_router = APIRouter()


@image_router.post(Endpoints.IMAGE_BUILD_ADV)
def build_image_with_kwargs(data: ImageBuildRequest):
    logger.info(f"Building Docker image with data: {data.dict(exclude_unset=True)}")
    return build_image_kwargs(data)


@image_router.post(Endpoints.IMAGE_LIST)
def list_images_advanced(filters: ImageListRequest = Body(...)):
    logger.info(f"Listing Docker images with filters: {filters.dict(exclude_unset=True)}")
    return list_images_with_filters(
        name=filters.name,
        all=filters.all,
        filters=filters.filters
    )


@image_router.post(Endpoints.DOCKER_LOGIN)
def dockerhub_login_view(data: DockerLoginRequest):
    logger.info(f"Logging into DockerHub with username: {data.username}")
    return dockerhub_login(data.username, data.password)


@image_router.post(Endpoints.IMAGE_PUSH)
def push_image(request: ImagePushRequest):
    logger.info(f"Pushing image from local tag '{request.local_tag}' to remote repo '{request.remote_repo}'")
    return push_image(request.local_tag, request.remote_repo)


@image_router.post(Endpoints.IMAGE_PULL)
def pull_image(request: ImagePullRequest):
    logger.info(f"Pulling image from '{request.repository}' with tag '{request.local_tag}'")
    return pull_image(request.repository, request.local_tag)


@image_router.delete(Endpoints.IMAGE_DELETE)
def delete_image(
    image_name: str = Query(..., description="Full image name with optional tag"),
    params: ImageRemoveRequest = Body(...),
):
    logger.info(f"Removing image '{image_name}' with params: {params.dict(exclude_unset=True)}")
    return remove_image_with_params(image_name, params)
