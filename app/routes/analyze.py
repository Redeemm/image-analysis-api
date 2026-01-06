from fastapi import APIRouter, HTTPException
from app.services.image_service import ImageService
from app.services.analysis_service import AnalysisService
from app.models.requests import AnalysisRequest
from app.models.responses import AnalysisResponse
from app.utils.logger import get_logger

router = APIRouter()
image_service = ImageService()
analysis_service = AnalysisService()
logger = get_logger(__name__)


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_image(request: AnalysisRequest):
    try:
        logger.info(f"Processing analysis request for image_id: {request.image_id}")

        # Check if image exists
        image_path = image_service.get_image_path(request.image_id)

        if not image_path:
            logger.warning(f"Image not found for ID: {request.image_id}")
            raise HTTPException(
                status_code=404,
                detail=f"Image not found for ID: {request.image_id}"
            )

        logger.info(f"Found image at path: {image_path}")

        # Perform analysis
        results = analysis_service.analyze_image(request.image_id, image_path)
        logger.info(f"Analysis completed for image_id: {request.image_id}")

        return AnalysisResponse(**results)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to analyze image: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to analyze image: {str(e)}")
