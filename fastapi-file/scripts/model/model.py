from sqlmodel import SQLModel, Field
from typing import Optional

class FileRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    reference_name: str
    filename: str
    file_path: str
