import pandas as pd
import numpy as np

class StatisticsService:
    @staticmethod
    def calculate_dataset_statistics(df: pd.DataFrame) -> dict:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        bool_cols = df.select_dtypes(include=[bool]).columns.tolist()
        datetime_cols = df.select_dtypes(include=['datetime', 'datetimetz']).columns.tolist()
        
        # Categorical/object columns usually overlap with text, we roughly separate by uniqueness in the profiler, 
        # but here we just count simple dtypes.
        obj_cols = df.select_dtypes(include=['object', 'string', 'category']).columns.tolist()
        
        return {
            "row_count": len(df),
            "column_count": len(df.columns),
            "numeric_columns": len(numeric_cols),
            "categorical_columns": len(obj_cols),
            "boolean_columns": len(bool_cols),
            "datetime_columns": len(datetime_cols),
            "text_columns": len(obj_cols),
            "memory_usage_bytes": int(df.memory_usage(deep=True).sum())
        }

    @staticmethod
    def calculate_column_statistics(df: pd.DataFrame, column_name: str) -> dict:
        col = df[column_name]
        is_numeric = pd.api.types.is_numeric_dtype(col) and not pd.api.types.is_bool_dtype(col)
        
        # Mode could be multiple values, take the first one or None
        mode_series = col.mode()
        mode_val = str(mode_series.iloc[0]) if not mode_series.empty else None
        
        stats = {
            "mean": float(col.mean()) if is_numeric else None,
            "median": float(col.median()) if is_numeric else None,
            "mode": mode_val,
            "variance": float(col.var()) if is_numeric else None,
            "std_dev": float(col.std()) if is_numeric else None,
            "min_val": float(col.min()) if is_numeric else None,
            "max_val": float(col.max()) if is_numeric else None,
            "range_val": float(col.max() - col.min()) if is_numeric and not pd.isna(col.max()) and not pd.isna(col.min()) else None,
            "q1": float(col.quantile(0.25)) if is_numeric else None,
            "q3": float(col.quantile(0.75)) if is_numeric else None,
            "iqr": float(col.quantile(0.75) - col.quantile(0.25)) if is_numeric else None,
            "skewness": float(col.skew()) if is_numeric else None,
            "kurtosis": float(col.kurtosis()) if is_numeric else None,
        }
        
        # Clean NaNs
        for k, v in stats.items():
            if pd.isna(v) or v in [np.inf, -np.inf]:
                stats[k] = None
                
        return stats
