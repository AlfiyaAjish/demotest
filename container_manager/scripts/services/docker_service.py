import docker
from scripts.constants.constants import *
from scripts.utils.response_handler import handle_exception

client = docker.DockerClient(base_url='unix://var/run/docker.sock')

def build_image(path: str, tag: str):
    try:
        image, _ = client.images.build(path=path, tag=tag)
        return {"message": IMAGE_BUILD_SUCCESS.format(tag=tag)}
    except Exception as e:
        handle_exception(e, "Failed to build image")

def list_images():
    try:
        return [img.tags for img in client.images.list()]
    except Exception as e:
        handle_exception(e, "Failed to list images")

def run_container(
    image: str,
    name: str,
    host_port: int = None,
    container_port: int = None,
    volume_name: str = None,
    container_path: str = None
):
    try:
        ports = {f"{container_port}/tcp": host_port} if host_port and container_port else None
        volumes = {volume_name: {'bind': container_path, 'mode': 'rw'}} if volume_name and container_path else None

        container = client.containers.run(
            image=image,
            name=name,
            ports=ports,
            volumes=volumes,
            detach=True
        )
        return {"message": f"Container '{name}' started successfully."}
    except Exception as e:
        handle_exception(e, "Failed to run container")

def list_containers():
    try:
        return [{"name": c.name, "image": c.image.tags, "status": c.status} for c in client.containers.list(all=True)]
    except Exception as e:
        handle_exception(e, "Failed to list containers")

# Stop a running container
def stop_container(name: str):
    try:
        container = client.containers.get(name)
        container.stop()
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


def get_logs(container_name: str):
    try:
        container = client.containers.get(container_name)
        return {"logs": container.logs().decode()}
    except Exception as e:
        handle_exception(e, "Failed to get logs")

def delete_container(container_name: str):
    try:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()
        return {"message": CONTAINER_DELETE_SUCCESS.format(name=container_name)}
    except Exception as e:
        handle_exception(e, "Failed to delete container")

def create_volume(name: str):
    try:
        client.volumes.create(name=name)
        return {"message": VOLUME_CREATE_SUCCESS.format(name=name)}
    except Exception as e:
        handle_exception(e, "Failed to create volume")

def list_volumes():
    try:
        return [v.name for v in client.volumes.list()]
    except Exception as e:
        handle_exception(e, "Failed to list volumes")

def update_volume(name: str, labels: dict):
    try:
        volume = client.volumes.get(name)
        volume.reload()
        return {"message": f"Volume '{name}' updated (note: actual label update requires recreation)."}
    except Exception as e:
        handle_exception(e, "Failed to update volume")

def delete_volume(name: str):
    try:
        volume = client.volumes.get(name)
        volume.remove()
        return {"message": VOLUME_DELETE_SUCCESS.format(name=name)}
    except Exception as e:
        handle_exception(e, "Failed to delete volume")
