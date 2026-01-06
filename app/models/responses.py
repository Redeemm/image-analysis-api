from typing import List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class BaseResponse(BaseModel):
    """Base response model with common fields"""
    success: bool = Field(default=True, description="Indicates if the request was successful")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + 'Z', description="Response timestamp in ISO format")


class HealthCheckResponse(BaseResponse):
    """Health check endpoint response"""
    status: str = Field(..., description="Service status", example="running")
    service: str = Field(..., description="Service name", example="Image Analysis API")
    version: str = Field(..., description="API version", example="1.0.0")


class UploadResponse(BaseResponse):
    """Image upload success response"""
    image_id: str = Field(..., description="Unique identifier for the uploaded image", example="abc123-def456-ghi789")
    message: str = Field(default="Image uploaded successfully", description="Success message")
    filename: str = Field(..., description="Original filename", example="image.jpg")
    file_size: int = Field(..., description="File size in bytes", example=102400)


class AnalysisResponse(BaseResponse):
    """Image analysis result response"""
    image_id: str = Field(..., description="Image identifier", example="abc123-def456-ghi789")
    skin_type: str = Field(..., description="Detected skin type", example="Oily")
    issues: List[str] = Field(..., description="Detected skin issues", example=["Hyperpigmentation", "Acne"])
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)", example=0.87)
    analysis_notes: str = Field(..., description="Additional analysis notes", example="Detected oily skin with 2 concern(s)")


class ErrorDetail(BaseModel):
    """Error detail structure"""
    code: str = Field(..., description="Error code", example="INVALID_FILE_TYPE")
    message: str = Field(..., description="Error message", example="Invalid file type. Allowed types: JPEG, PNG")
    field: Optional[str] = Field(None, description="Field that caused the error", example="file")


class ErrorResponse(BaseModel):
    """Error response model"""
    success: bool = Field(default=False, description="Always false for errors")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + 'Z', description="Error timestamp")
    error: ErrorDetail = Field(..., description="Error details")
    correlation_id: Optional[str] = Field(None, description="Request correlation ID for tracking")

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "timestamp": "2024-01-06T12:00:00Z",
                "error": {
                    "code": "INVALID_FILE_TYPE",
                    "message": "Invalid file type. Allowed types: JPEG, PNG",
                    "field": "file"
                },
                "correlation_id": "abc123-def456"
            }
        }
