import docker
from scripts.utils.response_handler import handle_exception
from fastapi import HTTPException
from scripts.models.volume_model import *

client = docker.from_env()

def create_volume_with_params(data: VolumeCreateRequest):
    try:
        opts = data.dict(exclude_unset=True)
        volume = client.volumes.create(**opts)
        return {
            "message": f"Volume '{volume.name}' created successfully.",
            "name": volume.name,
            "driver": volume.attrs.get("Driver"),
            "labels": volume.attrs.get("Labels")
        }
    except Exception as e:
        handle_exception(e, "Failed to create volume with parameters")

def remove_volume_with_params(name: str, params: VolumeRemoveRequest):
    try:
        opts = params.dict(exclude_unset=True)
        volume = client.volumes.get(name)
        volume.remove(**opts)
        return {"message": f"Volume '{name}' removed successfully."}
    except Exception as e:
        handle_exception(e, f"Failed to remove volume '{name}'")