
from fastapi import APIRouter,Query
from scripts.services import docker_service
from scripts.models.schemas import *

# Routers grouped by topic
image_router = APIRouter(prefix="/docker-images", tags=["Docker Images"])
container_router = APIRouter(prefix="/docker-containers", tags=["Docker Containers"])
volume_router = APIRouter(prefix="/docker-volumes", tags=["Docker Volumes"])

# ─────────────────────────────
# Docker Image Endpoints
# ─────────────────────────────


# @image_router.post("/build")
# def build_image(data: ImageBuildRequest):
#     return docker_service.build_image(data.dockerfile_path, data.tag)

@image_router.post("/build-advanced")
def build_image_with_kwargs(data: ImageBuildRequest):
    return docker_service.build_image_kwargs(data)

# @image_router.get("")
# def list_images():
#     return docker_service.list_images()

from fastapi import Body

@image_router.post("/list")
def list_images_advanced(filters: ImageListRequest = Body(...)):
    return docker_service.list_images_with_filters(
        name=filters.name,
        all=filters.all,
        filters=filters.filters
    )



# ─────────────────────────────
# Docker Container Endpoints
# ─────────────────────────────

@container_router.post("/run-advanced")
def run_container_advanced_view(data: ContainerRunAdvancedRequest):
    return docker_service.run_container_advanced(data)


# @container_router.post("/run")
# def run_container(data: ContainerRunRequest):
#     return docker_service.run_container(
#         image=data.image,
#         name=data.name,
#         host_port=data.host_port,
#         container_port=data.container_port,
#         volume_name=data.volume_name,
#         container_path=data.container_path
#     )

@container_router.post("/run-advanced")
def run_container_advanced_view(data: ContainerRunAdvancedRequest):
    return docker_service.run_container_advanced(data)

# @container_router.get("")
# def list_containers():
#     return docker_service.list_containers()

@container_router.post("/list")
def list_containers_advanced(params: ContainerListRequest):
    return docker_service.list_containers_with_filters(params)


from fastapi import Body
from scripts.models.schemas import ContainerLogsRequest

@container_router.post("/{name}/logs")
def get_logs_schema(
    name: str,
    params: ContainerLogsRequest = Body(...),
):
    return docker_service.get_logs_with_params(name, params)



# @container_router.post("/{name}/stop")
# def stop_container(name: str):
#     return docker_service.stop_container(name)

from fastapi import Query

@container_router.post("/{name}/stop")
def stop_container(name: str, timeout: Optional[float] = Query(None, description="Timeout in seconds before force stop")):
    return docker_service.stop_container(name, timeout)


@container_router.post("/{name}/start")
def start_container(name: str):
    return docker_service.start_container(name)

from fastapi import Body
from scripts.models.schemas import ContainerRemoveRequest

@container_router.post("/{name}/remove")
def remove_container(
    name: str,
    params: ContainerRemoveRequest = Body(...),
):
    return docker_service.remove_container_with_params(name, params)


# ─────────────────────────────
# Docker Volume Endpoints
# ─────────────────────────────

# @volume_router.post("")
# def create_volume(data: VolumeCreateRequest):
#     return docker_service.create_volume(data.name)

from fastapi import Body
from scripts.models.schemas import VolumeCreateRequest

@volume_router.post("")
def create_volume_advanced(
    data: VolumeCreateRequest = Body(...),
):
    return docker_service.create_volume_with_params(data)


from scripts.models.schemas import VolumeRemoveRequest

@volume_router.delete("/{name}")
def delete_volume(
    name: str,
    params: VolumeRemoveRequest = Body(...)
):
    return docker_service.remove_volume_with_params(name, params)


@volume_router.get("")
def list_volumes():
    return docker_service.list_volumes()

@volume_router.get("/{name}/inspect")
def inspect_volume(name: str):
    return docker_service.inspect_volume(name)

@volume_router.delete("/{name}")
def delete_volume(name: str):
    return docker_service.delete_volume(name)


@image_router.post("/login")
def dockerhub_login_view(data: DockerLoginRequest):
    return docker_service.dockerhub_login(data.username, data.password)

@image_router.post("/push")
def push_image(request: ImagePushRequest):
    return docker_service.push_image(request.local_tag, request.remote_repo)


@image_router.post("/pull")
def pull_image(request: ImagePullRequest):
    return docker_service.pull_image(request.repository, request.local_tag)


from scripts.models.schemas import ImageRemoveRequest

@image_router.delete("")
def delete_image(
    image_name: str = Query(..., description="Full image name with optional tag"),
    params: ImageRemoveRequest = Body(...),
):
    return docker_service.remove_image_with_params(image_name, params)





