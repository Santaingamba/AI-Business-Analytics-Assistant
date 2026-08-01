class TokenManager:
    """Manages token counting and context compression."""
    
    @staticmethod
    def count_tokens(text: str) -> int:
        """Approximate token count (1 token ~= 4 chars)."""
        if not text:
            return 0
        return len(text) // 4
        
    @staticmethod
    def prune_context(context: dict, max_tokens: int = 6000) -> dict:
        """Prunes the context to fit within the max_tokens limit."""
        import json
        context_str = json.dumps(context)
        if TokenManager.count_tokens(context_str) <= max_tokens:
            return context
            
        # Basic pruning strategy: trim large string lists or metrics if needed
        # In an enterprise setting, this would intelligently summarize older metrics
        pruned = context.copy()
        if "analytics" in pruned:
            if "segments" in pruned["analytics"]:
                pruned["analytics"]["segments"] = pruned["analytics"]["segments"][:5] # Keep top 5
        return pruned
