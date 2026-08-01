from enum import Enum
from typing import Dict

class PromptTemplateType(str, Enum):
    EXECUTIVE_SUMMARY = "EXECUTIVE_SUMMARY"
    BUSINESS_QUESTION = "BUSINESS_QUESTION"
    KPI_EXPLANATION = "KPI_EXPLANATION"
    REVENUE_ANALYSIS = "REVENUE_ANALYSIS"
    CUSTOMER_ANALYSIS = "CUSTOMER_ANALYSIS"
    PRODUCT_ANALYSIS = "PRODUCT_ANALYSIS"
    TREND_ANALYSIS = "TREND_ANALYSIS"
    ANOMALY_EXPLANATION = "ANOMALY_EXPLANATION"
    DATA_QUALITY = "DATA_QUALITY"
    RECOMMENDATION = "RECOMMENDATION"
    ROOT_CAUSE = "ROOT_CAUSE"
    COMPARISON = "COMPARISON"
    GENERAL = "GENERAL"

# Versioned Templates
PROMPT_TEMPLATES: Dict[str, Dict[PromptTemplateType, str]] = {
    "v1": {
        PromptTemplateType.EXECUTIVE_SUMMARY: (
            "You are a Principal AI Business Analyst. "
            "Generate an executive summary for the provided dashboard and analytics context. "
            "Focus on high-level KPIs, significant trends, and actionable insights. "
            "Context: {context}"
        ),
        PromptTemplateType.BUSINESS_QUESTION: (
            "You are a Principal AI Business Analyst. "
            "Answer the user's business question using ONLY the provided analytics context. "
            "Do not hallucinate data that is not present in the context. "
            "Context: {context}\n"
            "Question: {question}"
        ),
        PromptTemplateType.KPI_EXPLANATION: (
            "Explain the following KPI to an executive audience. Provide its current value, trend, and business impact based on the context. "
            "Context: {context}\n"
            "KPI: {target}"
        ),
        PromptTemplateType.REVENUE_ANALYSIS: (
            "Analyze the revenue metrics provided in the context. Highlight growth areas, declining segments, and potential reasons for the changes. "
            "Context: {context}"
        ),
        PromptTemplateType.CUSTOMER_ANALYSIS: (
            "Analyze the customer segments provided in the context. Describe the characteristics of the most valuable segments and any churn risks. "
            "Context: {context}"
        ),
        PromptTemplateType.PRODUCT_ANALYSIS: (
            "Review the product performance from the context. Identify top performers, underperformers, and inventory/sales correlations. "
            "Context: {context}"
        ),
        PromptTemplateType.TREND_ANALYSIS: (
            "Explain the major trends observed in the provided analytics context over time. "
            "Context: {context}"
        ),
        PromptTemplateType.ANOMALY_EXPLANATION: (
            "Identify and explain any outliers or anomalies present in the context data. Discuss potential causes. "
            "Context: {context}"
        ),
        PromptTemplateType.DATA_QUALITY: (
            "Explain the data quality score and any profiling issues found in the dataset context. Suggest remediation steps. "
            "Context: {context}"
        ),
        PromptTemplateType.RECOMMENDATION: (
            "Based on the provided analytics context, generate 3-5 strategic business recommendations. "
            "Prioritize them by Business Impact and Confidence. "
            "Context: {context}"
        ),
        PromptTemplateType.ROOT_CAUSE: (
            "Perform a root cause analysis for the requested metric or event, using only the provided context. "
            "Context: {context}\n"
            "Target: {target}"
        ),
        PromptTemplateType.COMPARISON: (
            "Compare the requested segments, time periods, or products based on the context provided. "
            "Context: {context}\n"
            "Comparison targets: {target}"
        ),
        PromptTemplateType.GENERAL: (
            "You are an AI Business Analyst. Answer the user's question conversationally. Use the provided context if relevant. "
            "Context: {context}\n"
            "Question: {question}"
        )
    }
}

def get_template(template_type: PromptTemplateType, version: str = "v1") -> str:
    """Retrieve a versioned prompt template."""
    if version not in PROMPT_TEMPLATES:
        raise ValueError(f"Template version {version} not found.")
    if template_type not in PROMPT_TEMPLATES[version]:
        raise ValueError(f"Template type {template_type} not found in version {version}.")
    return PROMPT_TEMPLATES[version][template_type]
