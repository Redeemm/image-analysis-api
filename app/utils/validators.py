"""Validation utilities for image uploads"""
from fastapi import HTTPException, UploadFile
from typing import Tuple
from app.config import settings


async def validate_image_upload(file: UploadFile) -> Tuple[bool, str]:
    """
    Validate uploaded image file.

    Args:
        file: The uploaded file object

    Returns:
        Tuple of (is_valid, error_message)

    Raises:
        HTTPException: If validation fails
    """
    # Check content type
    if file.content_type not in settings.allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: JPEG, PNG. Got: {file.content_type}"
        )

    # Read file content to check size
    contents = await file.read()
    file_size = len(contents)

    # Reset file pointer for later reading
    await file.seek(0)

    # Check file size
    if file_size > settings.max_file_size:
        max_mb = settings.max_file_size / 1024 / 1024
        actual_mb = file_size / 1024 / 1024
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {max_mb:.0f}MB. Got: {actual_mb:.2f}MB"
        )

    if file_size == 0:
        raise HTTPException(
            status_code=400,
            detail="Empty file uploaded"
        )

    return True, ""


def validate_file_extension(filename: str) -> bool:
    """Check if filename has a valid extension"""
    return any(filename.lower().endswith(ext) for ext in settings.allowed_file_extensions)
