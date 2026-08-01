import pandas as pd
from typing import Dict, Any, List

class ProductAnalytics:
    @staticmethod
    def analyze(df: pd.DataFrame, roles: Dict[str, str]) -> List[Dict[str, Any]]:
        metrics = []
        prod_col = roles.get('product_id')
        rev_col = roles.get('revenue')
        
        if not prod_col:
            return metrics
            
        vol = df[prod_col].value_counts()
        
        top_10_vol = {str(k): int(v) for k, v in vol.head(10).items()}
        metrics.append({
            "metric_name": "Top Products by Volume",
            "metric_category": "Product",
            "dimension": prod_col,
            "value": top_10_vol,
            "aggregation": "count_top_10"
        })
        
        bottom_10_vol = {str(k): int(v) for k, v in vol.tail(10).items()}
        metrics.append({
            "metric_name": "Worst Products by Volume",
            "metric_category": "Product",
            "dimension": prod_col,
            "value": bottom_10_vol,
            "aggregation": "count_bottom_10"
        })
        
        if rev_col:
            rev_val = df.groupby(prod_col)[rev_col].sum().sort_values(ascending=False)
            top_10_rev = {str(k): float(v) for k, v in rev_val.head(10).items()}
            
            metrics.append({
                "metric_name": "Top Products by Revenue",
                "metric_category": "Product",
                "dimension": prod_col,
                "value": top_10_rev,
                "aggregation": "sum_top_10"
            })
            
        return metrics
