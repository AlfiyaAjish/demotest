import docker
import re
from fastapi import HTTPException
from typing import Dict, Any
from scripts.utils.response_handler import handle_exception
from scripts.models.image_model import *
from scripts.constants.app_constants import *

client = docker.from_env()

def is_valid_docker_tag(tag: str) -> bool:
    return bool(re.match(r"^[a-z0-9][a-z0-9_.-]*(/[a-z0-9][a-z0-9_.-]*)*(?::[a-zA-Z0-9_.-]+)?$", tag))

def build_image_kwargs(data: ImageBuildRequest):
    try:
        build_args = data.dict(exclude_unset=True)

        if not build_args.get("path") and not build_args.get("fileobj"):
            raise HTTPException(status_code=400, detail=INVALID_REQUEST)

        tag = build_args.get("tag")
        if tag:
            if not is_valid_docker_tag(tag):
                raise HTTPException(status_code=400, detail=INVALID_REQUEST)
        else:
            build_args["tag"] = "default:latest"

        image, _ = client.images.build(**build_args)

        return {
            "message": IMAGE_BUILD_SUCCESS.format(tag=build_args['tag']),
            "id": image.id,
            "tags": image.tags or ["<none>:<none>"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=IMAGE_BUILD_FAILURE)

def list_images_with_filters(name: str = None, all: bool = False, filters: Dict[str, Any] = None):
    try:
        kwargs = {}
        if name is not None:
            kwargs["name"] = name
        if all:
            kwargs["all"] = True
        if filters is not None:
            kwargs["filters"] = filters

        images = client.images.list(**kwargs)
        return {
            "message": IMAGE_LIST_SUCCESS,
            "images": [{"id": img.id, "tags": img.tags} for img in images]
        }

    except Exception as e:
        handle_exception(e, IMAGE_LIST_RETRIEVED)

docker_logged_in = False

def dockerhub_login(username: str, password: str):
    global docker_logged_in
    try:
        client.login(username=username, password=password)
        docker_logged_in = True
        return {"message": AUTH_LOGIN_SUCCESS}
    except Exception as e:
        handle_exception(e, AUTH_LOGIN_FAILURE)

def push_image(local_tag: str, remote_repo: str):
    if not docker_logged_in:
        raise HTTPException(status_code=401, detail=UNAUTHORIZED)

    try:
        image = client.images.get(local_tag)
        image.tag(remote_repo)
        result = client.images.push(remote_repo)
        return {"message": IMAGE_PUSH_SUCCESS, "result": result}
    except Exception as e:
        handle_exception(e, IMAGE_PUSH_FAILURE)

def pull_image(repository: str, local_tag: str = None):
    try:
        image = client.images.pull(repository)
        if local_tag:
            image.tag(local_tag)

        return {
            "message": IMAGE_PULL_SUCCESS,
            "tags": image.tags,
            "retagged_as": local_tag if local_tag else "Not retagged"
        }

    except docker.errors.APIError as e:
        if "unauthorized" in str(e).lower() or "authentication required" in str(e).lower():
            raise HTTPException(status_code=401, detail=UNAUTHORIZED)
        handle_exception(e, IMAGE_PULL_FAILURE)

def remove_image_with_params(image_name: str, params: ImageRemoveRequest):
    try:
        opts = params.dict(exclude_unset=True)
        client.images.remove(image=image_name, **opts)
        return {
            "message": IMAGE_REMOVE_SUCCESS,
            "used_options": opts
        }
    except docker.errors.ImageNotFound:
        raise HTTPException(status_code=404, detail=IMAGE_NOT_FOUND)
    except Exception as e:
        handle_exception(e, IMAGE_REMOVE_FAILURE)
