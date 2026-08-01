import json
from typing import Dict, Any, Optional
from app.services.ai.prompt_engine.templates import PromptTemplateType, get_template

class PromptBuilder:
    """Builds structured prompts by injecting context into versioned templates."""
    
    def __init__(self, version: str = "v1"):
        self.version = version

    def build_prompt(
        self,
        template_type: PromptTemplateType,
        context: Dict[str, Any],
        question: Optional[str] = None,
        target: Optional[str] = None
    ) -> str:
        """
        Constructs the final prompt string by injecting context into the selected template.
        """
        template = get_template(template_type, self.version)
        
        # Serialize context
        try:
            context_str = json.dumps(context, indent=2, default=str)
        except Exception:
            context_str = str(context)
        
        kwargs = {"context": context_str}
        if "{question}" in template:
            kwargs["question"] = question or ""
        if "{target}" in template:
            kwargs["target"] = target or ""
            
        return template.format(**kwargs)
