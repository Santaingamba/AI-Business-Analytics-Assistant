import pandas as pd
import numpy as np
from typing import Dict, Any, List

class TrendAnalyzer:
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
                
            monthly = temp_df.set_index(ts_col).resample('ME')[rev_col].sum()
            monthly = monthly[monthly > 0]
            
            if len(monthly) >= 2:
                mom = monthly.pct_change() * 100
                mom.index = mom.index.strftime('%Y-%m')
                mom = mom.replace([np.inf, -np.inf], np.nan).dropna()
                
                metrics.append({
                    "metric_name": "Month-over-Month Growth %",
                    "metric_category": "Trend",
                    "dimension": "Month",
                    "value": {str(k): float(v) for k, v in mom.items()},
                    "aggregation": "pct_change"
                })
                
                if not mom.empty:
                    latest_growth = mom.iloc[-1]
                    metrics.append({
                        "metric_name": "Latest MoM Growth",
                        "metric_category": "Trend",
                        "dimension": "Month",
                        "value": float(latest_growth),
                        "aggregation": "latest"
                    })
                    
        except Exception:
            pass
            
        return metrics
