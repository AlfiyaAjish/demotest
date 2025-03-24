import os
from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlmodel import Session
from ..services.service import save_file_record, get_files
from ..model.model import FileRecord
from ..database.database import get_db

router = APIRouter(prefix="/v1/files", tags=["Files"])

UPLOAD_FOLDER = "uploads/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/", status_code=201)
async def upload_file(reference_name: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a file and save its record in the database."""
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_location, "wb") as buffer:
        buffer.write(await file.read())

    file_record = save_file_record(db, reference_name, file.filename)
    return {"message": "File uploaded successfully", "file": file_record}


@router.get("/")
async def list_files(db: Session = Depends(get_db)):
    """Retrieve the list of uploaded files."""
    return get_files(db)
