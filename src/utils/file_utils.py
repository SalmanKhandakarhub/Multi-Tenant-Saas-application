import os
from fastapi import HTTPException, status
from fastapi.responses import FileResponse
from core.config import settings  


def get_uploaded_file(filename: str):
    file_path = os.path.join(settings.UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

    return FileResponse(file_path)