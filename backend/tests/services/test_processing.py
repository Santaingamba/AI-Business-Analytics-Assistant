import pandas as pd
import numpy as np
from app.services.processing.statistics import StatisticsService
from app.services.processing.type_validator import TypeValidator
from app.services.processing.quality import DataQualityService
from app.services.processing.outlier import OutlierDetector

def test_type_validator():
    emails = pd.Series(["test@test.com", "admin@admin.org", "invalid", "user@domain.co", "hello@world.io"])
    assert TypeValidator.detect_semantic_type(emails) == "Email"

def test_statistics():
    df = pd.DataFrame({
        "A": [1, 2, 3, 4],
        "B": [1.5, 2.5, 3.5, 4.5]
    })
    
    stats = StatisticsService.calculate_dataset_statistics(df)
    assert stats["row_count"] == 4
    assert stats["column_count"] == 2
    assert stats["numeric_columns"] == 2
    
def test_data_quality():
    score = DataQualityService.calculate_quality_score(10.0, 5.0)
    assert score == 85.0
    
def test_outlier_detector():
    df = pd.DataFrame({
        "A": [1, 2, 3, 4, 100]
    })
    res = OutlierDetector.detect_outliers_iqr(df, "A")
    assert res["outlier_count"] == 1
