from fastapi import APIRouter
from scripts.models.schemas import *
from scripts.services import docker_service

router = APIRouter()

@router.post("/images/build")
def build_image(data: ImageBuildRequest):
    return docker_service.build_image(data.dockerfile_path, data.tag)

@router.get("/images")
def list_images():
    return docker_service.list_images()

@router.post("/containers/run")
def run_container(data: ContainerRunRequest):
    return docker_service.run_container(
        image=data.image,
        name=data.name,
        host_port=data.host_port,
        container_port=data.container_port,
        volume_name=data.volume_name,
        container_path=data.container_path
    )


@router.get("/containers")
def list_containers():
    return docker_service.list_containers()

@router.post("/containers/{name}/stop")
def stop_container(name: str):
    return docker_service.stop_container(name)

@router.post("/containers/{name}/start")
def start_container(name: str):
    return docker_service.start_container(name)


@router.get("/containers/{name}/logs")
def get_logs(name: str):
    return docker_service.get_logs(name)

@router.delete("/containers/{name}")
def delete_container(name: str):
    return docker_service.delete_container(name)

@router.post("/volumes")
def create_volume(data: VolumeCreateRequest):
    return docker_service.create_volume(data.name)

@router.get("/volumes")
def list_volumes():
    return docker_service.list_volumes()

@router.put("/volumes")
def update_volume(data: VolumeUpdateRequest):
    return docker_service.update_volume(data.name, data.labels)

@router.delete("/volumes/{name}")
def delete_volume(name: str):
    return docker_service.delete_volume(name)
