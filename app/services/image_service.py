import uuid
from pathlib import Path
from fastapi import UploadFile
from typing import Optional
from app.config import settings


class ImageService:
    """Handles image storage operations"""

    @staticmethod
    def generate_image_id() -> str:
        return str(uuid.uuid4())

    @staticmethod
    async def save_image(file: UploadFile, image_id: str) -> str:
        # Get file extension
        ext = Path(file.filename).suffix if file.filename else ".jpg"
        filename = f"{image_id}{ext}"
        file_path = settings.upload_dir / filename

        # Save file
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)

        return str(file_path)

    @staticmethod
    def get_image_path(image_id: str) -> Optional[Path]:
        # Check for configured file extensions
        for ext in settings.allowed_file_extensions:
            file_path = settings.upload_dir / f"{image_id}{ext}"
            if file_path.exists():
                return file_path
        return None

    @staticmethod
    def image_exists(image_id: str) -> bool:
        #Check if an image exists in storage
        return ImageService.get_image_path(image_id) is not None
