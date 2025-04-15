import docker
from scripts.constants.constants import *
from scripts.utils.response_handler import handle_exception
from fastapi import HTTPException
from scripts.models.schemas import *

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

# def build_image(path: str, tag: str):
#     try:
#         image, _ = client.images.build(path=path, tag=tag)
#         return {"message": IMAGE_BUILD_SUCCESS.format(tag=tag)}
#     except Exception as e:
#         handle_exception(e, "Failed to build image")

import re

def clean_advanced_container_data(data: ContainerRunAdvancedRequest):
    """
    Convert all fields with value "string" or empty string to None
    """
    cleaned_data = data.dict()
    for key, value in cleaned_data.items():
        if isinstance(value, str) and value.strip().lower() == "string":
            cleaned_data[key] = None
        if isinstance(value, str) and value.strip() == "":
            cleaned_data[key] = None
    return cleaned_data


def is_valid_docker_tag(tag: str) -> bool:
    # Docker tag validation pattern
    return bool(re.match(r"^[a-z0-9][a-z0-9_.-]*(/[a-z0-9][a-z0-9_.-]*)*(?::[a-zA-Z0-9_.-]+)?$", tag))

def build_image_kwargs(data: ImageBuildRequest):
    try:
        build_args = data.dict(exclude_unset=True)

        # Ensure build context is provided
        if not build_args.get("path") and not build_args.get("fileobj"):
            raise HTTPException(status_code=400, detail="Missing required 'path' or 'fileobj' for Docker build.")

        # Validate the tag format
        tag = build_args.get("tag")
        if tag:
            if not is_valid_docker_tag(tag):
                raise HTTPException(status_code=400, detail=f"Invalid Docker image tag: '{tag}'")
        else:
            build_args["tag"] = "default:latest"  # Fallback tag if none provided

        image, _ = client.images.build(**build_args)

        return {
            "message": IMAGE_BUILD_SUCCESS.format(tag=build_args['tag']),
            "id": image.id,
            "tags": image.tags or ["<none>:<none>"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Docker build failed: {str(e)}")



# def list_images():
#     try:
#         return [img.tags for img in client.images.list()]
#     except Exception as e:
#         handle_exception(e, "Failed to list images")

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
        return [{"id": img.id, "tags": img.tags} for img in images]
    except Exception as e:
        handle_exception(e, "Failed to list images with filters")


# def run_container(
#     image: str,
#     name: str,
#     host_port: int = None,
#     container_port: int = None,
#     volume_name: str = None,
#     container_path: str = None
# ):
#     try:
#         ports = {f"{container_port}/tcp": host_port} if host_port and container_port else None
#         volumes = {volume_name: {'bind': container_path, 'mode': 'rw'}} if volume_name and container_path else None
#
#         container = client.containers.run(
#             image=image,
#             name=name,
#             ports=ports,
#             volumes=volumes,
#             detach=True
#         )
#         return {"message": f"Container '{name}' started successfully."}
#     except Exception as e:
#         handle_exception(e, "Failed to run container")

def run_container_advanced(data: ContainerRunAdvancedRequest):
    try:
        kwargs = data.dict(exclude_unset=True)
        image = kwargs.pop("image")
        command = kwargs.pop("command", None)

        container = client.containers.run(image=image, command=command, **kwargs)

        return {
            "message": f"Container '{container.name}' started successfully.",
            "id": container.id,
            "status": container.status
        }
    except Exception as e:
        handle_exception(e, "Failed to run container with advanced parameters")
#
#
# def list_containers():
#     try:
#         return [{"name": c.name, "image": c.image.tags, "status": c.status} for c in client.containers.list(all=True)]
#     except Exception as e:
#         handle_exception(e, "Failed to list containers")

def list_containers_with_filters(params: ContainerListRequest):
    try:
        kwargs = params.dict(exclude_unset=True)
        containers = client.containers.list(**kwargs)

        return [
            {
                "name": c.name,
                "id": c.id,
                "image": c.image.tags,
                "status": c.status
            } for c in containers
        ]
    except Exception as e:
        handle_exception(e, "Failed to list containers with filters")


# Stop a running container
# def stop_container(name: str):
#     try:
#         container = client.containers.get(name)
#         container.stop()
#         return {"message": f"Container '{name}' stopped successfully."}
#     except Exception as e:
#         handle_exception(e, f"Failed to stop container '{name}'")

def stop_container(name: str, timeout: float = None):
    try:
        container = client.containers.get(name)
        stop_args = {"timeout": timeout} if timeout is not None else {}
        container.stop(**stop_args)
        return {"message": f"Container '{name}' stopped successfully."}
    except Exception as e:
        handle_exception(e, f"Failed to stop container '{name}'")


# Start a stopped container
def start_container(name: str):
    try:
        container = client.containers.get(name)
        container.start()
        return {"message": f"Container '{name}' started successfully."}
    except Exception as e:
        handle_exception(e, f"Failed to start container '{name}'")


def get_logs_with_params(
    name: str,
    params: ContainerLogsRequest
):
    try:
        container = client.containers.get(name)
        opts = params.dict(exclude_unset=True)
        # Docker SDK expects stream=True only if follow=True
        if opts.pop("follow", False):
            return container.logs(stream=True, **opts)

        raw = container.logs(stream=False, **opts)
        return {"logs": raw.decode(errors="ignore")}
    except Exception as e:
        handle_exception(e, f"Failed to get logs for '{name}'")


def remove_container_with_params(name: str, params: ContainerRemoveRequest):
    try:
        container = client.containers.get(name)
        opts = params.dict(exclude_unset=True)
        container.remove(**opts)
        return {"message": f"Container '{name}' removed successfully."}
    except Exception as e:
        handle_exception(e, f"Failed to remove container '{name}'")


# def create_volume(name: str):
#     try:
#         client.volumes.create(name=name)
#         return {"message": VOLUME_CREATE_SUCCESS.format(name=name)}
#     except Exception as e:
#         handle_exception(e, "Failed to create volume")
#
# def list_volumes():
#     try:
#         return [v.name for v in client.volumes.list()]
#     except Exception as e:
#         handle_exception(e, "Failed to list volumes")

from scripts.models.schemas import VolumeCreateRequest

def create_volume_with_params(data: VolumeCreateRequest):
    try:
        opts = data.dict(exclude_unset=True)
        # Docker SDK: client.volumes.create(name=None, driver=None, driver_opts=None, labels=None)
        volume = client.volumes.create(**opts)
        return {
            "message": f"Volume '{volume.name}' created successfully.",
            "name": volume.name,
            "driver": volume.attrs.get("Driver"),
            "labels": volume.attrs.get("Labels")
        }
    except Exception as e:
        handle_exception(e, "Failed to create volume with parameters")

#
# def delete_volume(name: str):
#     try:
#         volume = client.volumes.get(name)
#         volume.remove()
#         return {"message": VOLUME_DELETE_SUCCESS.format(name=name)}
#     except Exception as e:
#         handle_exception(e, "Failed to delete volume")

from scripts.models.schemas import VolumeRemoveRequest

def remove_volume_with_params(name: str, params: VolumeRemoveRequest):
    try:
        opts = params.dict(exclude_unset=True)
        volume = client.volumes.get(name)
        volume.remove(**opts)
        return {"message": f"Volume '{name}' removed successfully."}
    except Exception as e:
        handle_exception(e, f"Failed to remove volume '{name}'")



def push_image(local_tag: str, remote_repo: str):
    if not docker_logged_in:
        raise HTTPException(status_code=401, detail="Unauthorized: Please login to DockerHub first")

    try:
        image = client.images.get(local_tag)
        image.tag(remote_repo)
        result = client.images.push(remote_repo)
        return {"message": f"Pushed to {remote_repo}", "result": result}
    except Exception as e:
        handle_exception(e, f"Failed to push image '{local_tag}'")

def pull_image(repository: str, local_tag: str = None):
    try:
        # Attempt to pull without requiring login (works for public images)
        image = client.images.pull(repository)
        if local_tag:
            image.tag(local_tag)

        return {
            "message": f"Pulled {repository}",
            "tags": image.tags,
            "retagged_as": local_tag if local_tag else "Not retagged"
        }

    except docker.errors.APIError as e:
        # Catch unauthorized access — means it's a private repo
        if "unauthorized" in str(e).lower() or "authentication required" in str(e).lower():
            raise HTTPException(
                status_code=401,
                detail="Private repository: Please login to DockerHub first using /docker-images/login"
            )
        # Other errors
        handle_exception(e, f"Failed to pull image '{repository}'")




docker_logged_in = False
def dockerhub_login(username: str, password: str):
    global docker_logged_in
    try:
        client.login(username=username, password=password)
        docker_logged_in = True
        return {"message": f"DockerHub login successful as '{username}'."}
    except Exception as e:
        handle_exception(e, "DockerHub login failed")

#
# def delete_image(image_name: str):
#     try:
#         client.images.remove(image=image_name, force=True)
#         return {"message": f"Image '{image_name}' deleted successfully."}
#     except Exception as e:
#         handle_exception(e, f"Failed to delete image '{image_name}'")



def remove_image_with_params(image_name: str, params: ImageRemoveRequest):
    try:
        opts = params.dict(exclude_unset=True)
        client.images.remove(image=image_name, **opts)
        return {"message": f"Image '{image_name}' removed successfully.", "used_options": opts}
    except Exception as e:
        handle_exception(e, f"Failed to remove image '{image_name}'")
