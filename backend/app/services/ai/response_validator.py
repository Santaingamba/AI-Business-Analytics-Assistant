import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class ResponseValidator:
    """Validates responses from the LLM, handles fallbacks and hallucinations."""
    
    @staticmethod
    def validate_json(response: str) -> Optional[Dict[str, Any]]:
        """Ensures the response is valid JSON."""
        try:
            # Sometimes LLMs wrap JSON in markdown blocks
            clean_response = response.strip()
            if clean_response.startswith("```json"):
                clean_response = clean_response[7:]
            if clean_response.endswith("```"):
                clean_response = clean_response[:-3]
                
            return json.loads(clean_response)
        except json.JSONDecodeError:
            logger.error("LLM returned malformed JSON")
            return None
            
    @staticmethod
    def check_empty(response: str) -> bool:
        """Checks if the response is empty."""
        return not response or len(response.strip()) == 0
        
    @staticmethod
    def fallback_explanation(context: Dict[str, Any], target: str) -> str:
        """Deterministic fallback explanation if LLM fails."""
        # Simple string-based extraction from context
        metrics = context.get("analytics", {}).get("metrics", [])
        for m in metrics:
            if m["name"].lower() == target.lower():
                return f"Fallback Analysis: {m['name']} is currently at {m['value']} ({m['category']})."
                
        kpis = context.get("analytics", {}).get("kpis", [])
        for k in kpis:
            if k["name"].lower() == target.lower():
                return f"Fallback Analysis: {k['name']} is {k['value']} (Trend: {k['trend']}, Target: {k['target']})."
                
        return "Our AI service is temporarily unavailable, and we could not find deterministic analytics for this specific query."
