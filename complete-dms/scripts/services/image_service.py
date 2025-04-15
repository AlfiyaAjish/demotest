from fastapi import APIRouter, Query, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from scripts.handlers.image_handler import *
from scripts.models.image_model import *
from scripts.constants.api_endpoints import Endpoints
from scripts.logging.logger import logger
from scripts.utils.jwt_utils import decode_access_token

image_router = APIRouter()

# Setting up OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


# Dependency function to get the current user from the token
def get_current_user(token: str = Depends(oauth2_scheme)):
    username = decode_access_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return username


@image_router.post(Endpoints.IMAGE_BUILD_ADV)
def build_image_with_kwargs(data: ImageBuildRequest, username: str = Depends(get_current_user)):
    logger.info(f"User '{username}' is building Docker image with data: {data.dict(exclude_unset=True)}")
    return build_image_kwargs(data)


@image_router.post(Endpoints.IMAGE_LIST)
def list_images_advanced(filters: ImageListRequest = Body(...), username: str = Depends(get_current_user)):
    logger.info(f"User '{username}' is listing Docker images with filters: {filters.dict(exclude_unset=True)}")
    return list_images_with_filters(
        name=filters.name,
        all=filters.all,
        filters=filters.filters
    )


@image_router.post(Endpoints.DOCKER_LOGIN)
def dockerhub_login_view(data: DockerLoginRequest, username: str = Depends(get_current_user)):
    logger.info(f"User '{username}' is logging into DockerHub with username: {data.username}")
    return dockerhub_login(data.username, data.password)


@image_router.post(Endpoints.IMAGE_PUSH)
def push_image(request: ImagePushRequest, username: str = Depends(get_current_user)):
    logger.info(
        f"User '{username}' is pushing image from local tag '{request.local_tag}' to remote repo '{request.remote_repo}'")
    return push_image(request.local_tag, request.remote_repo)


@image_router.post(Endpoints.IMAGE_PULL)
def pull_image(request: ImagePullRequest, username: str = Depends(get_current_user)):
    logger.info(f"User '{username}' is pulling image from '{request.repository}' with tag '{request.local_tag}'")
    return pull_image(request.repository, request.local_tag)


@image_router.delete(Endpoints.IMAGE_DELETE)
def delete_image(
        image_name: str = Query(..., description="Full image name with optional tag"),
        params: ImageRemoveRequest = Body(...),
        username: str = Depends(get_current_user),
):
    logger.info(f"User '{username}' is removing image '{image_name}' with params: {params.dict(exclude_unset=True)}")
    return remove_image_with_params(image_name, params)