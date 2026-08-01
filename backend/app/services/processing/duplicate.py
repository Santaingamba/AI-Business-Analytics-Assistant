import pandas as pd

class DuplicateAnalyzer:
    @staticmethod
    def analyze_dataset(df: pd.DataFrame) -> dict:
        duplicate_rows = int(df.duplicated().sum())
        
        # Be careful with columns duplication on very wide/large datasets
        duplicate_columns = 0
        if len(df.columns) <= 100 and len(df) <= 100000:
            try:
                duplicate_columns = int(df.T.duplicated().sum())
            except Exception:
                pass
            
        return {
            "duplicate_rows": duplicate_rows,
            "duplicate_columns": duplicate_columns
        }

    @staticmethod
    def analyze_column(df: pd.DataFrame, column_name: str) -> dict:
        col = df[column_name]
        unique_count = int(col.nunique(dropna=False))
        total = len(col)
        
        return {
            "unique_count": unique_count,
            "unique_percentage": (unique_count / total * 100) if total > 0 else 0.0,
            "duplicate_percentage": (100.0 - (unique_count / total * 100)) if total > 0 else 0.0
        }
