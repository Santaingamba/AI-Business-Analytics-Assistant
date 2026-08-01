import pandas as pd
from typing import Dict, Any, List

class TimeSeriesAnalytics:
    @staticmethod
    def analyze(df: pd.DataFrame, roles: Dict[str, str]) -> List[Dict[str, Any]]:
        metrics = []
        ts_col = roles.get('timestamp')
        rev_col = roles.get('revenue')
        
        if not ts_col or not rev_col:
            return metrics
            
        try:
            temp_df = df.copy()
            temp_df[ts_col] = pd.to_datetime(temp_df[ts_col], errors='coerce')
            temp_df = temp_df.dropna(subset=[ts_col])
            
            if temp_df.empty:
                return metrics
                
            daily = temp_df.set_index(ts_col).resample('D')[rev_col].sum()
            daily.index = daily.index.strftime('%Y-%m-%d')
            
            daily = daily[daily > 0]
            
            metrics.append({
                "metric_name": "Daily Revenue",
                "metric_category": "Time-Series",
                "dimension": "Day",
                "value": {str(k): float(v) for k, v in daily.items()},
                "aggregation": "sum"
            })
            
            ma_7 = daily.rolling(window=7, min_periods=1).mean()
            metrics.append({
                "metric_name": "7-Day Moving Average",
                "metric_category": "Time-Series",
                "dimension": "Day",
                "value": {str(k): float(v) for k, v in ma_7.items()},
                "aggregation": "rolling_mean_7d"
            })
            
        except Exception:
            pass
            
        return metrics
