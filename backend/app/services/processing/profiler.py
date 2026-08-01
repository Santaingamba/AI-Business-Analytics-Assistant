import pandas as pd
from typing import Dict, Any

from .statistics import StatisticsService
from .missing import MissingValueAnalyzer
from .duplicate import DuplicateAnalyzer
from .outlier import OutlierDetector
from .type_validator import TypeValidator
from .quality import DataQualityService

class ProfilingService:
    @staticmethod
    def profile_dataset(df: pd.DataFrame) -> Dict[str, Any]:
        """Profiles the dataset and its columns, returning a structured summary dict."""
        
        # Dataset level
        dataset_stats = StatisticsService.calculate_dataset_statistics(df)
        missing_stats = MissingValueAnalyzer.analyze_dataset(df)
        dup_stats = DuplicateAnalyzer.analyze_dataset(df)
        
        dataset_stats.update(missing_stats)
        dataset_stats.update(dup_stats)
        
        # Calculate quality
        null_pct = dataset_stats["null_percentage"]
        dup_row_pct = (dataset_stats["duplicate_rows"] / dataset_stats["row_count"] * 100) if dataset_stats["row_count"] > 0 else 0
        
        dataset_stats["completeness_score"] = DataQualityService.calculate_completeness_score(null_pct)
        dataset_stats["quality_score"] = DataQualityService.calculate_quality_score(null_pct, dup_row_pct)
        
        # Column level
        columns_profile = {}
        for col_name in df.columns:
            c_stats = StatisticsService.calculate_column_statistics(df, col_name)
            c_miss = MissingValueAnalyzer.analyze_column(df, col_name)
            c_dup = DuplicateAnalyzer.analyze_column(df, col_name)
            c_out = OutlierDetector.detect_outliers_iqr(df, col_name)
            semantic = TypeValidator.detect_semantic_type(df[col_name])
            
            c_stats.update(c_miss)
            c_stats.update(c_dup)
            c_stats.update(c_out)
            c_stats["semantic_type"] = semantic
            
            columns_profile[col_name] = c_stats
            
        return {
            "dataset": dataset_stats,
            "columns": columns_profile
        }
