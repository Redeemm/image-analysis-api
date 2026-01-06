import random
from typing import Dict, List
from pathlib import Path


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

    @staticmethod
    def analyze_image(image_id: str, image_path: Path) -> Dict:
        # Generate deterministic results based on image_id for consistency
        random.seed(image_id)

        # Select random skin type
        skin_type = random.choice(AnalysisService.SKIN_TYPES)

        # Select 1-3 random issues
        num_issues = random.randint(1, 3)
        issues = random.sample(AnalysisService.ISSUES, num_issues)

        # Generate confidence score (between 0.75 and 0.95)
        confidence = round(random.uniform(0.75, 0.95), 2)

        # Reset random seed
        random.seed()

        return {
            "image_id": image_id,
            "skin_type": skin_type,
            "issues": issues,
            "confidence": confidence,
            "analysis_notes": f"Detected {skin_type.lower()} skin with {num_issues} concern(s)"
        }
