from pydantic import BaseModel,ConfigDict
from typing import Optional, Union, IO, Any, Dict, List,Tuple,Literal
# from io import StringIO
# from docker.types import Mount, Ulimit, EndpointConfig
from datetime import datetime


class VolumeCreateRequest(BaseModel):
    name: Optional[str] = None
    driver: Optional[str] = None
    driver_opts: Optional[Dict[str, Any]] = None
    labels: Optional[Dict[str, str]] = None

class VolumeRemoveRequest(BaseModel):
    force: Optional[bool] = False