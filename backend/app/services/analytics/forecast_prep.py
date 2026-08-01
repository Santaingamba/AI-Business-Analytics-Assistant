import pandas as pd
from typing import Dict, Any, List

class ForecastPreparation:
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
            
            if len(daily) > 14:
                lag_1 = daily.shift(1)
                lag_7 = daily.shift(7)
                
                corr_1 = daily.corr(lag_1)
                corr_7 = daily.corr(lag_7)
                
                metrics.append({
                    "metric_name": "Autocorrelation (Lag 1)",
                    "metric_category": "Forecast Readiness",
                    "dimension": "Day",
                    "value": float(corr_1) if not pd.isna(corr_1) else 0.0,
                    "aggregation": "corr"
                })
                
                metrics.append({
                    "metric_name": "Autocorrelation (Lag 7)",
                    "metric_category": "Forecast Readiness",
                    "dimension": "Day",
                    "value": float(corr_7) if not pd.isna(corr_7) else 0.0,
                    "aggregation": "corr"
                })
                
        except Exception:
            pass
            
        return metrics
