import pandas as pd

class MissingValueAnalyzer:
    @staticmethod
    def analyze_dataset(df: pd.DataFrame) -> dict:
        null_cells = int(df.isna().sum().sum())
        total_cells = df.size
        
        return {
            "null_cells": null_cells,
            "null_percentage": (null_cells / total_cells * 100) if total_cells > 0 else 0.0
        }

    @staticmethod
    def analyze_column(df: pd.DataFrame, column_name: str) -> dict:
        col = df[column_name]
        missing_count = int(col.isna().sum())
        total = len(col)
        
        return {
            "missing_count": missing_count,
            "missing_percentage": (missing_count / total * 100) if total > 0 else 0.0
        }
