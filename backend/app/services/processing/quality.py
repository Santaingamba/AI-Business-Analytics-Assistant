import pandas as pd

class DataQualityService:
    @staticmethod
    def calculate_quality_score(null_percentage: float, duplicate_percentage: float) -> float:
        missing_penalty = min(50.0, null_percentage)
        duplicate_penalty = min(30.0, duplicate_percentage)
        
        score = 100.0 - missing_penalty - duplicate_penalty
        return max(0.0, float(score))

    @staticmethod
    def calculate_completeness_score(null_percentage: float) -> float:
        return max(0.0, float(100.0 - null_percentage))
