import random
import os
from typing import Dict, List
from pathlib import Path
from PIL import Image


class AnalysisService:
    """Provides mock image analysis functionality"""

    # Mock data for realistic responses
    SKIN_TYPES = ["Oily", "Dry", "Combination", "Normal", "Sensitive"]
    ISSUES = [
        "Hyperpigmentation",
        "Acne",
        "Dark Circles",
        "Fine Lines",
        "Redness",
        "Uneven Texture",
        "Enlarged Pores"
    ]
    SEVERITIES = ["Low", "Medium", "High"]

    @staticmethod
    def extract_image_metadata(image_path: Path) -> Dict:
        """Extract metadata from image file"""
        with Image.open(image_path) as img:
            file_size_bytes = os.path.getsize(image_path)
            file_size_kb = round(file_size_bytes / 1024, 2)

            return {
                "format": img.format.lower() if img.format else "unknown",
                "width": img.width,
                "height": img.height,
                "file_size_kb": file_size_kb,
                "color_space": img.mode
            }

    @staticmethod
    def analyze_image(image_id: str, image_path: Path) -> Dict:
        """
        Perform mock analysis on an image.

        Returns structured analysis results with image metadata.
        """
        # Generate deterministic results based on image_id for consistency
        random.seed(image_id)

        # Extract image metadata
        image_metadata = AnalysisService.extract_image_metadata(image_path)

        # Select random skin type
        skin_type = random.choice(AnalysisService.SKIN_TYPES)
        skin_type_confidence = round(random.uniform(0.85, 0.98), 2)

        # Select 1-3 random issues with severity
        num_issues = random.randint(1, 3)
        selected_issues = random.sample(AnalysisService.ISSUES, num_issues)

        issues = []
        for issue_name in selected_issues:
            issues.append({
                "name": issue_name,
                "severity": random.choice(AnalysisService.SEVERITIES),
                "confidence": round(random.uniform(0.75, 0.95), 2)
            })

        # Calculate overall confidence (average of skin_type and issues)
        issue_confidences = [issue["confidence"] for issue in issues]
        overall_confidence = round(
            (skin_type_confidence + sum(issue_confidences)) / (len(issue_confidences) + 1),
            2
        )

        # Reset random seed
        random.seed()

        return {
            "image_id": image_id,
            "image_metadata": image_metadata,
            "analysis": {
                "skin_type": {
                    "value": skin_type,
                    "confidence": skin_type_confidence
                },
                "issues": issues,
                "confidence": overall_confidence,
                "analysis_notes": f"Detected {skin_type.lower()} skin with {num_issues} issue(s)."
            }
        }
