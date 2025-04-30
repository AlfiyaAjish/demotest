import os
from sqlmodel import Session, select
from fastapi import HTTPException
from ..model.model import FileRecord

UPLOAD_FOLDER = "uploads/"



def save_file_record(db: Session, reference_name: str, filename: str):
    """Save file record with absolute path in the database."""
    file_path = os.path.abspath(os.path.join(UPLOAD_FOLDER, filename))  # Get absolute path
    file_record = FileRecord(reference_name=reference_name, filename=filename, file_path=file_path)

    db.add(file_record)
    db.commit()
    db.refresh(file_record)

    return file_record


def get_files(db: Session):
    """Retrieve all file records from the database."""
    return db.exec(select(FileRecord)).all()
