from fastapi import APIRouter, File, UploadFile, HTTPException
from app.utils.validators import validate_image_upload
from app.services.image_service import ImageService
from app.models.responses import UploadResponse
from app.utils.logger import get_logger

router = APIRouter()
image_service = ImageService()
logger = get_logger(__name__)


@router.post("/upload", response_model=UploadResponse, status_code=201)
async def upload_image(file: UploadFile = File(..., description="Image file (JPEG or PNG, max 5MB)")):
    try:
        logger.info(f"Processing upload request for file: {file.filename}")

        # Validate the uploaded file
        await validate_image_upload(file)

        # Get file size for response
        contents = await file.read()
        file_size = len(contents)
        await file.seek(0)  # Reset for saving

        # Generate unique image ID
        image_id = image_service.generate_image_id()
        logger.info(f"Generated image_id: {image_id}")

        # Save the image
        file_path = await image_service.save_image(file, image_id)
        logger.info(f"Image saved successfully: {file_path}")

        return UploadResponse(
            image_id=image_id,
            filename=file.filename or "unknown",
            file_size=file_size
        )

    except HTTPException:
        logger.warning(f"Upload validation failed for file: {file.filename}")
        raise
    except Exception as e:
        logger.error(f"Failed to process image upload: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process image upload: {str(e)}"
        )
