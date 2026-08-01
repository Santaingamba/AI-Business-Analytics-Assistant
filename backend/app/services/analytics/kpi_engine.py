import pandas as pd
from typing import Dict, Any, List

class KPIEngine:
    @staticmethod
    def calculate_kpis(df: pd.DataFrame, roles: Dict[str, str]) -> List[Dict[str, Any]]:
        kpis = []
        
        # Revenue KPIs
        revenue_col = roles.get('revenue')
        if revenue_col:
            total_rev = df[revenue_col].sum()
            kpis.append({
                "kpi_name": "Total Revenue",
                "kpi_category": "Financial",
                "value": float(total_rev)
            })
            
            aov = df[revenue_col].mean()
            kpis.append({
                "kpi_name": "Average Order Value",
                "kpi_category": "Financial",
                "value": float(aov) if not pd.isna(aov) else 0.0
            })
            
        # Cost & Profit KPIs
        cost_col = roles.get('cost')
        if revenue_col and cost_col:
            total_cost = df[cost_col].sum()
            profit = total_rev - total_cost
            gross_margin = (profit / total_rev * 100) if total_rev > 0 else 0
            
            kpis.extend([
                {"kpi_name": "Total Cost", "kpi_category": "Financial", "value": float(total_cost)},
                {"kpi_name": "Gross Profit", "kpi_category": "Financial", "value": float(profit)},
                {"kpi_name": "Gross Margin %", "kpi_category": "Financial", "value": float(gross_margin)}
            ])
            
        # Customer KPIs
        customer_col = roles.get('customer_id')
        if customer_col:
            unique_customers = df[customer_col].nunique()
            kpis.append({
                "kpi_name": "Total Customers",
                "kpi_category": "Customer",
                "value": float(unique_customers)
            })
            
            if revenue_col and unique_customers > 0:
                arpu = total_rev / unique_customers
                kpis.append({
                    "kpi_name": "ARPU",
                    "kpi_category": "Customer",
                    "value": float(arpu)
                })
                
        # Product KPIs
        product_col = roles.get('product_id')
        if product_col:
            unique_products = df[product_col].nunique()
            kpis.append({
                "kpi_name": "Unique Products Sold",
                "kpi_category": "Product",
                "value": float(unique_products)
            })
                
        return kpis
