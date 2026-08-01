import pandas as pd
from typing import Dict, Any, List

class BenchmarkEngine:
    @staticmethod
    def analyze(df: pd.DataFrame, roles: Dict[str, str]) -> List[Dict[str, Any]]:
        metrics = []
        rev_col = roles.get('revenue')
        
        if not rev_col:
            return metrics
            
        try:
            percentiles = df[rev_col].quantile([0.1, 0.25, 0.5, 0.75, 0.9]).to_dict()
            
            metrics.append({
                "metric_name": "Order Value Percentiles",
                "metric_category": "Benchmark",
                "dimension": "Revenue",
                "value": {str(k): float(v) for k, v in percentiles.items()},
                "aggregation": "percentile"
            })
            
        except Exception:
            pass
            
        return metrics
