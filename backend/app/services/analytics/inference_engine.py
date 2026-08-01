import pandas as pd
from typing import Dict, List, Optional

class InferenceEngine:
    @staticmethod
    def infer_roles(df: pd.DataFrame, semantic_types: Dict[str, str] = None) -> Dict[str, str]:
        """
        Infers the business role of columns.
        Returns a mapping of Role -> Column Name
        Roles: 'timestamp', 'revenue', 'customer_id', 'product_id', 'category', 'cost'
        """
        roles = {}
        columns = df.columns.tolist()
        columns_lower = [c.lower() for c in columns]
        
        # 1. Infer Timestamp
        for col, col_l in zip(columns, columns_lower):
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                roles['timestamp'] = col
                break
            if 'date' in col_l or 'time' in col_l or 'created' in col_l:
                if semantic_types and semantic_types.get(col) == 'Datetime':
                    roles['timestamp'] = col
                    break
                # If no semantic types available, fallback to trying to parse head
                try:
                    pd.to_datetime(df[col].dropna().head(10))
                    roles['timestamp'] = col
                    break
                except:
                    pass
                    
        # 2. Infer Revenue/Price
        for col, col_l in zip(columns, columns_lower):
            if any(k in col_l for k in ['revenue', 'price', 'total', 'amount', 'sales', 'value']):
                if pd.api.types.is_numeric_dtype(df[col]):
                    roles['revenue'] = col
                    break
                    
        # 3. Infer Cost
        for col, col_l in zip(columns, columns_lower):
            if any(k in col_l for k in ['cost', 'expense', 'cogs']):
                if pd.api.types.is_numeric_dtype(df[col]):
                    roles['cost'] = col
                    break

        # 4. Infer Customer ID
        for col, col_l in zip(columns, columns_lower):
            if any(k in col_l for k in ['customer', 'user', 'client', 'buyer']):
                if 'id' in col_l or 'email' in col_l or 'name' in col_l:
                    roles['customer_id'] = col
                    break
            if semantic_types and semantic_types.get(col) == 'Email' and 'customer_id' not in roles:
                roles['customer_id'] = col
                
        # 5. Infer Product ID/Category
        for col, col_l in zip(columns, columns_lower):
            if 'product' in col_l or 'item' in col_l or 'sku' in col_l:
                roles['product_id'] = col
                break
                
        for col, col_l in zip(columns, columns_lower):
            if 'category' in col_l or 'type' in col_l or 'segment' in col_l or 'department' in col_l:
                roles['category'] = col
                break
                
        return roles
