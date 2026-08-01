import pandas as pd
from typing import Dict, Any, List

class FunnelAnalytics:
    @staticmethod
    def analyze(df: pd.DataFrame, roles: Dict[str, str]) -> List[Dict[str, Any]]:
        metrics = []
        
        columns = [c.lower() for c in df.columns]
        state_col = None
        for col in df.columns:
            if col.lower() in ['status', 'state', 'stage', 'event']:
                state_col = col
                break
                
        if not state_col:
            return metrics
            
        try:
            funnel_counts = df[state_col].value_counts()
            sorted_funnel = funnel_counts.sort_values(ascending=False)
            
            metrics.append({
                "metric_name": "State/Stage Funnel Distribution",
                "metric_category": "Funnel",
                "dimension": state_col,
                "value": {str(k): int(v) for k, v in sorted_funnel.items()},
                "aggregation": "funnel_counts"
            })
            
            if len(sorted_funnel) > 1:
                max_state_vol = sorted_funnel.iloc[0]
                min_state_vol = sorted_funnel.iloc[-1]
                overall_conv = (min_state_vol / max_state_vol * 100) if max_state_vol > 0 else 0
                
                metrics.append({
                    "metric_name": "Overall Estimated Conversion %",
                    "metric_category": "Funnel",
                    "dimension": state_col,
                    "value": float(overall_conv),
                    "aggregation": "conversion_rate"
                })
        except Exception:
            pass
            
        return metrics
