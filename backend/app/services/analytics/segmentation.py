import pandas as pd
from typing import Dict, Any, List

class SegmentationEngine:
    @staticmethod
    def analyze(df: pd.DataFrame, roles: Dict[str, str]) -> List[Dict[str, Any]]:
        segments = []
        cust_col = roles.get('customer_id')
        rev_col = roles.get('revenue')
        ts_col = roles.get('timestamp')
        
        if not cust_col or not rev_col or not ts_col:
            return segments
            
        try:
            temp_df = df.copy()
            temp_df[ts_col] = pd.to_datetime(temp_df[ts_col], errors='coerce')
            temp_df = temp_df.dropna(subset=[ts_col])
            
            if temp_df.empty:
                return segments
                
            current_date = temp_df[ts_col].max() + pd.Timedelta(days=1)
            
            rfm = temp_df.groupby(cust_col).agg({
                ts_col: lambda x: (current_date - x.max()).days,
                rev_col: ['count', 'sum']
            }).reset_index()
            
            rfm.columns = [cust_col, 'Recency', 'Frequency', 'Monetary']
            
            r_labels = range(4, 0, -1)
            f_labels = range(1, 5)
            m_labels = range(1, 5)
            
            rfm['R'] = pd.qcut(rfm['Recency'], q=4, labels=r_labels, duplicates='drop')
            rfm['F'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=4, labels=f_labels)
            rfm['M'] = pd.qcut(rfm['Monetary'], q=4, labels=m_labels, duplicates='drop')
            
            def join_rfm(x): return str(x['R']) + str(x['F'])
            rfm['RF_Segment'] = rfm.apply(join_rfm, axis=1)
            
            def map_segment(rf):
                if rf in ['44', '43', '34']: return 'Champions'
                if rf in ['42', '33', '32']: return 'Loyal'
                if rf in ['41', '31']: return 'Recent'
                if rf in ['24', '23', '14', '13']: return 'At Risk'
                return 'Hibernating'
                
            rfm['SegmentName'] = rfm['RF_Segment'].apply(map_segment)
            
            segment_counts = rfm['SegmentName'].value_counts()
            segment_revs = rfm.groupby('SegmentName')['Monetary'].sum()
            total_cust = len(rfm)
            
            for seg_name in segment_counts.index:
                count = int(segment_counts[seg_name])
                rev = float(segment_revs.get(seg_name, 0))
                segments.append({
                    "segment_name": seg_name,
                    "description": f"RFM Customer Segment",
                    "customer_count": count,
                    "revenue": rev,
                    "percentage": float((count / total_cust) * 100) if total_cust > 0 else 0
                })
                
        except Exception:
            pass
            
        return segments
