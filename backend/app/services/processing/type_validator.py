import pandas as pd
import re

class TypeValidator:
    @staticmethod
    def detect_semantic_type(col: pd.Series) -> str:
        if col.isna().all():
            return "Unknown"
        
        sample = col.dropna().head(100).astype(str)
        
        email_pattern = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
        url_pattern = re.compile(r"^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$")
        uuid_pattern = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)
        
        emails = 0
        urls = 0
        uuids = 0
        booleans = 0
        
        for val in sample:
            v = val.strip()
            if email_pattern.match(v):
                emails += 1
            if url_pattern.match(v):
                urls += 1
            if uuid_pattern.match(v):
                uuids += 1
            if v.lower() in ["true", "false", "yes", "no", "1", "0", "y", "n", "t", "f"]:
                booleans += 1
                
        threshold = 0.8 * len(sample)
        
        if emails >= threshold:
            return "Email"
        if urls >= threshold:
            return "URL"
        if uuids >= threshold:
            return "UUID"
        if booleans >= threshold:
            return "Boolean"
            
        if pd.api.types.is_datetime64_any_dtype(col):
            return "Datetime"
        if pd.api.types.is_numeric_dtype(col):
            if pd.api.types.is_integer_dtype(col):
                if col.min() >= 0 and col.max() <= 120 and col.mean() > 0:
                    return "Age"
                return "Integer"
            return "Float"
            
        if col.nunique() < 20 and len(col) > 100:
            return "Categorical"
            
        return "Free Text"
