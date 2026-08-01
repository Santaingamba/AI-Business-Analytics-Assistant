import pandas as pd
from typing import Dict, Any, List

class RevenueAnalytics:
    @staticmethod
    def analyze(df: pd.DataFrame, roles: Dict[str, str]) -> List[Dict[str, Any]]:
        metrics = []
        rev_col = roles.get('revenue')
        
        if not rev_col:
            return metrics
            
        cat_col = roles.get('category')
        if cat_col:
            rev_by_cat = df.groupby(cat_col)[rev_col].sum().sort_values(ascending=False)
            metrics.append({
                "metric_name": "Revenue by Category",
                "metric_category": "Revenue",
                "dimension": cat_col,
                "value": rev_by_cat.to_dict(),
                "aggregation": "sum"
            })
            
            if not rev_by_cat.empty:
                metrics.append({
                    "metric_name": "Top Revenue Category",
                    "metric_category": "Revenue",
                    "dimension": cat_col,
                    "value": str(rev_by_cat.index[0]),
                    "aggregation": "top_1"
                })
                
        ts_col = roles.get('timestamp')
        if ts_col:
            try:
                temp_df = df.copy()
                temp_df[ts_col] = pd.to_datetime(temp_df[ts_col])
                
                # Monthly Revenue
                monthly = temp_df.set_index(ts_col).resample('ME')[rev_col].sum()
                monthly.index = monthly.index.astype(str)
                metrics.append({
                    "metric_name": "Monthly Revenue",
                    "metric_category": "Revenue",
                    "dimension": "Month",
                    "value": monthly.to_dict(),
                    "aggregation": "sum"
                })
            except Exception:
                pass
                
        return metrics
