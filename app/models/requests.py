from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    """Request model for image analysis endpoint"""
    image_id: str = Field(
        ...,
        description="Unique identifier of the uploaded image",
        example="abc123-def456-ghi789",
        min_length=1
    )

    class Config:
        json_schema_extra = {
            "example": {
                "image_id": "abc123-def456-ghi789"
            }
        }
