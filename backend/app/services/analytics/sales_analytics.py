import pandas as pd
from typing import Dict, Any, List

class SalesAnalytics:
    @staticmethod
    def analyze(df: pd.DataFrame, roles: Dict[str, str]) -> List[Dict[str, Any]]:
        metrics = []
        rev_col = roles.get('revenue')
        ts_col = roles.get('timestamp')
        
        if not rev_col or not ts_col:
            return metrics
            
        try:
            temp_df = df.copy()
            temp_df[ts_col] = pd.to_datetime(temp_df[ts_col], errors='coerce')
            temp_df = temp_df.dropna(subset=[ts_col])
            
            if temp_df.empty:
                return metrics
                
            temp_df['DayOfWeek'] = temp_df[ts_col].dt.day_name()
            temp_df['HourOfDay'] = temp_df[ts_col].dt.hour
            
            dow_sales = temp_df.groupby('DayOfWeek')[rev_col].sum()
            metrics.append({
                "metric_name": "Sales by Day of Week",
                "metric_category": "Sales",
                "dimension": "Day of Week",
                "value": {str(k): float(v) for k, v in dow_sales.items()},
                "aggregation": "sum"
            })
            
            hod_sales = temp_df.groupby('HourOfDay')[rev_col].sum()
            metrics.append({
                "metric_name": "Sales by Hour of Day",
                "metric_category": "Sales",
                "dimension": "Hour of Day",
                "value": {str(k): float(v) for k, v in hod_sales.items()},
                "aggregation": "sum"
            })
            
        except Exception:
            pass
            
        return metrics
