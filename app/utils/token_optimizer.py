def estimate_tokens(text: str) -> int:
    """
    Estimates the number of tokens in a standard text assuming roughly 4 characters per token.
    For more accuracy, libraries like tiktoken could be used for OpenAI, 
    but 4 chars per token is a safe, free, and standard estimate for both LLMs.
    """
    return len(text) // 4

def optimize_prompt(base_prompt: str, variables: dict, max_prompt_tokens: int = 150) -> str:
    """
    Optimizes the context variables so that the final prompt fits well within the max token limit.
    In this application, the largest variable is likely the 'missed_topics_str' or 'questions_answered'.
    We will truncate the missed topics if it's too long to save token cost.
    """
    # Helper to calculate available tokens
    def get_prompt_with_vars(vars_dict: dict) -> str:
        try:
            return base_prompt.format(**vars_dict)
        except KeyError:
            # If base prompt does not use literal formatting, just append
            return base_prompt + " " + str(vars_dict)
            
    # Initial estimate
    current_prompt = get_prompt_with_vars(variables)
    current_tokens = estimate_tokens(current_prompt)
    
    if current_tokens <= max_prompt_tokens:
        return current_prompt
        
    # If over limit, we need to apply truncation strategy
    optimized_variables = variables.copy()
    
    # Example optimization: truncate 'missed_topics_str'
    if "missed_topics_str" in optimized_variables:
        topics_str = optimized_variables["missed_topics_str"]
        topics_list = topics_str.split(", ")
        
        while topics_list and estimate_tokens(get_prompt_with_vars(optimized_variables)) > max_prompt_tokens:
            topics_list.pop() # Remove the last topic to save tokens
            optimized_variables["missed_topics_str"] = ", ".join(topics_list) + ", [truncated for optimization]"

    return get_prompt_with_vars(optimized_variables)
