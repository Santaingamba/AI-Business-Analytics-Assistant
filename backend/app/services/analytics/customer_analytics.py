import pandas as pd
from typing import Dict, Any, List

class CustomerAnalytics:
    @staticmethod
    def analyze(df: pd.DataFrame, roles: Dict[str, str]) -> List[Dict[str, Any]]:
        metrics = []
        cust_col = roles.get('customer_id')
        rev_col = roles.get('revenue')
        
        if not cust_col:
            return metrics
            
        freq = df[cust_col].value_counts()
        metrics.append({
            "metric_name": "Purchase Frequency Summary",
            "metric_category": "Customer",
            "dimension": "Orders per Customer",
            "value": freq.describe().to_dict(),
            "aggregation": "distribution"
        })
        
        if rev_col:
            cust_val = df.groupby(cust_col)[rev_col].sum().sort_values(ascending=False)
            
            # Format top 10 as dict with string keys (for JSON serialization)
            top_10 = {str(k): float(v) for k, v in cust_val.head(10).items()}
            metrics.append({
                "metric_name": "Top Customers by Revenue",
                "metric_category": "Customer",
                "dimension": cust_col,
                "value": top_10,
                "aggregation": "sum_top_10"
            })
            
        return metrics
