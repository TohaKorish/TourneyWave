import uuid
from pathlib import Path

from fastapi import UploadFile

from app.api.config.settings import settings


class ImageService:
    IMAGES_FOLDER = 'static/images/'

    def store(self, file: UploadFile) -> str:
        extension = file.filename.split('.')[-1]
        filename = uuid.uuid4().hex + f".{extension}"

        path = Path(__file__).resolve().parent.parent.parent.parent / self.IMAGES_FOLDER

        file_path = path / filename

        with open(file_path, 'wb') as f:
            f.write(file.file.read())

        return f"{settings.BACKEND_URL}{self.IMAGES_FOLDER}{filename}"

