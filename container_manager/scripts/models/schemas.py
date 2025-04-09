from pydantic import BaseModel
from typing import Optional, Dict

class ImageBuildRequest(BaseModel):
    dockerfile_path: str
    tag: str

class ContainerRunRequest(BaseModel):
    image: str
    name: str

class VolumeCreateRequest(BaseModel):
    name: str

class VolumeUpdateRequest(BaseModel):
    name: str
    labels: Dict[str, str]
