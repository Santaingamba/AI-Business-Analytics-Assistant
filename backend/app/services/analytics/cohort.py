import pandas as pd
from typing import Dict, Any, List

class CohortAnalytics:
    @staticmethod
    def analyze(df: pd.DataFrame, roles: Dict[str, str]) -> List[Dict[str, Any]]:
        metrics = []
        ts_col = roles.get('timestamp')
        cust_col = roles.get('customer_id')
        
        if not ts_col or not cust_col:
            return metrics
            
        try:
            temp_df = df.copy()
            temp_df[ts_col] = pd.to_datetime(temp_df[ts_col], errors='coerce')
            temp_df = temp_df.dropna(subset=[ts_col])
            
            if temp_df.empty:
                return metrics
                
            temp_df['InvoiceMonth'] = temp_df[ts_col].dt.to_period('M')
            temp_df['CohortMonth'] = temp_df.groupby(cust_col)['InvoiceMonth'].transform('min')
            
            def get_date_int(d, column):
                year = d[column].dt.year
                month = d[column].dt.month
                return year, month

            invoice_year, invoice_month = get_date_int(temp_df, 'InvoiceMonth')
            cohort_year, cohort_month = get_date_int(temp_df, 'CohortMonth')
            
            years_diff = invoice_year - cohort_year
            months_diff = invoice_month - cohort_month
            temp_df['CohortIndex'] = years_diff * 12 + months_diff + 1
            
            cohort_data = temp_df.groupby(['CohortMonth', 'CohortIndex'])[cust_col].nunique().reset_index()
            cohort_pivot = cohort_data.pivot(index='CohortMonth', columns='CohortIndex', values=cust_col)
            
            cohort_pivot.index = cohort_pivot.index.astype(str)
            cohort_pivot.columns = cohort_pivot.columns.astype(str)
            
            cohort_size = cohort_pivot.iloc[:, 0]
            retention = cohort_pivot.divide(cohort_size, axis=0)
            
            ret_dict = retention.fillna(0).to_dict(orient='index')
            # Ensure float types for JSON
            cleaned_dict = {
                k: {inner_k: float(inner_v) for inner_k, inner_v in v.items()}
                for k, v in ret_dict.items()
            }
            
            metrics.append({
                "metric_name": "Monthly Customer Retention Matrix",
                "metric_category": "Cohort",
                "dimension": "CohortMonth vs CohortIndex",
                "value": cleaned_dict,
                "aggregation": "retention_percentage"
            })
            
        except Exception:
            pass
            
        return metrics
