# from fastapi import APIRouter
# from scripts.models.schemas import *
# from scripts.services import docker_service
#
# router = APIRouter()
#
#
# @router.post("/images/build")
# def build_image(data: ImageBuildRequest):
#     return docker_service.build_image(data.dockerfile_path, data.tag)
#
# @router.get("/images")
# def list_images():
#     return docker_service.list_images()
#
# @router.post("/containers/run")
# def run_container(data: ContainerRunRequest):
#     return docker_service.run_container(
#         image=data.image,
#         name=data.name,
#         host_port=data.host_port,
#         container_port=data.container_port,
#         volume_name=data.volume_name,
#         container_path=data.container_path
#     )
#
#
# @router.get("/containers")
# def list_containers():
#     return docker_service.list_containers()
#
# @router.post("/containers/{name}/stop")
# def stop_container(name: str):
#     return docker_service.stop_container(name)
#
# @router.post("/containers/{name}/start")
# def start_container(name: str):
#     return docker_service.start_container(name)
#
#
# @router.get("/containers/{name}/logs")
# def get_logs(name: str):
#     return docker_service.get_logs(name)
#
# @router.delete("/containers/{name}")
# def delete_container(name: str):
#     return docker_service.delete_container(name)
#
# @router.post("/volumes")
# def create_volume(data: VolumeCreateRequest):
#     return docker_service.create_volume(data.name)
#
# @router.get("/volumes")
# def list_volumes():
#     return docker_service.list_volumes()
#
# @router.put("/volumes")
# def update_volume(data: VolumeUpdateRequest):
#     return docker_service.update_volume(data.name, data.labels)
#
# @router.delete("/volumes/{name}")
# def delete_volume(name: str):
#     return docker_service.delete_volume(name)


from fastapi import APIRouter
from scripts.services import docker_service
from scripts.models.schemas import *

# Routers grouped by topic
auth_router = APIRouter(prefix="/docker-auth", tags=["Docker Auth"])
image_router = APIRouter(prefix="/docker-images", tags=["Docker Images"])
container_router = APIRouter(prefix="/docker-containers", tags=["Docker Containers"])
volume_router = APIRouter(prefix="/docker-volumes", tags=["Docker Volumes"])

# ─────────────────────────────
# Docker Image Endpoints
# ─────────────────────────────

@image_router.post("/build")
def build_image(data: ImageBuildRequest):
    return docker_service.build_image(data.dockerfile_path, data.tag)

@image_router.get("")
def list_images():
    return docker_service.list_images()

# ─────────────────────────────
# Docker Container Endpoints
# ─────────────────────────────

@container_router.post("/run")
def run_container(data: ContainerRunRequest):
    return docker_service.run_container(
        image=data.image,
        name=data.name,
        host_port=data.host_port,
        container_port=data.container_port,
        volume_name=data.volume_name,
        container_path=data.container_path
    )

@container_router.get("")
def list_containers():
    return docker_service.list_containers()

@container_router.get("/{name}/logs")
def get_logs(name: str):
    return docker_service.get_logs(name)

@container_router.post("/{name}/stop")
def stop_container(name: str):
    return docker_service.stop_container(name)

@container_router.post("/{name}/start")
def start_container(name: str):
    return docker_service.start_container(name)

@container_router.delete("/{name}")
def delete_container(name: str):
    return docker_service.delete_container(name)

# ─────────────────────────────
# Docker Volume Endpoints
# ─────────────────────────────

@volume_router.post("")
def create_volume(data: VolumeCreateRequest):
    return docker_service.create_volume(data.name)

@volume_router.get("")
def list_volumes():
    return docker_service.list_volumes()

@volume_router.get("/{name}/inspect")
def inspect_volume(name: str):
    return docker_service.inspect_volume(name)

@volume_router.put("")
def update_volume(data: VolumeUpdateRequest):
    return docker_service.update_volume(data.name, data.labels)

@volume_router.delete("/{name}")
def delete_volume(name: str):
    return docker_service.delete_volume(name)

from fastapi import Body

@auth_router.post("/login")
def docker_login(username: str = Body(...), password: str = Body(...)):
    return docker_service.docker_login(username, password)

@auth_router.post("/logout")
def docker_logout():
    return docker_service.docker_logout()

@auth_router.post("/push")
def push_image(local_tag: str, remote_repo: str, token: str):
    return docker_service.push_image(local_tag, remote_repo, token)

@auth_router.post("/pull")
def pull_image(repository: str, token: str):
    return docker_service.pull_image(repository, token)

#
# @router.post("/docker-login")
# def docker_login(username: str = Body(...), password: str = Body(...)):
#     return docker_service.docker_login(username, password)
#
# @router.post("/docker-logout")
# def docker_logout():
#     return docker_service.docker_logout()
#
# @router.post("/docker-images/push")
# def push_image(local_tag: str, remote_repo: str, token: str):
#     return docker_service.push_image(local_tag, remote_repo, token)
#
# @router.post("/docker-images/pull")
# def pull_image(repository: str, token: str):
#     return docker_service.pull_image(repository, token)
