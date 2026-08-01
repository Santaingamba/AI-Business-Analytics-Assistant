import pandas as pd

class OutlierDetector:
    @staticmethod
    def detect_outliers_iqr(df: pd.DataFrame, column_name: str) -> dict:
        col = df[column_name]
        
        if not pd.api.types.is_numeric_dtype(col) or pd.api.types.is_bool_dtype(col):
            return {"outlier_count": 0, "outlier_percentage": 0.0}
            
        q1 = col.quantile(0.25)
        q3 = col.quantile(0.75)
        iqr = q3 - q1
        
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        outliers = col[(col < lower_bound) | (col > upper_bound)]
        outlier_count = int(outliers.count())
        total = int(col.count())
        
        return {
            "outlier_count": outlier_count,
            "outlier_percentage": (outlier_count / total * 100) if total > 0 else 0.0
        }
