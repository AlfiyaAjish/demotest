from pydantic import BaseModel
from typing import Optional, Dict

class ImageBuildRequest(BaseModel):
    dockerfile_path: str
    tag: str

class ContainerRunRequest(BaseModel):
    image: str
    name: str
    host_port: Optional[int] = None
    container_port: Optional[int] = None
    volume_name: Optional[str] = None
    container_path: Optional[str] = None


class VolumeCreateRequest(BaseModel):
    name: str

class VolumeUpdateRequest(BaseModel):
    name: str
    labels: Dict[str, str]
