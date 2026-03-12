import os
from dotenv import load_dotenv

# Import our new modules
from app.utils.token_optimizer import optimize_prompt
from app.services.llm_provider import generate_content

load_dotenv()

def generate_study_plan(session_data):
    ability_score = session_data.get("ability_score", 0.5)
    questions_answered = session_data.get("questions_answered", [])
    
    missed_topics = set()
    for q in questions_answered:
        if not q.get("correct", False):
            missed_topics.add(q.get("topic", "General"))
            
    difficulty_reached = round(ability_score, 2)
    missed_topics_str = ", ".join(missed_topics) if missed_topics else "None"
    
    # 1. Base prompt with placeholders instead of formatted strings
    base_prompt = """
    The student has just completed an adaptive diagnostic test. 
    Their final estimated ability score (difficulty reached) is {difficulty_reached} on a scale of 0.1 to 1.0.
    Based on their incorrect answers, they struggled with the following topics: {missed_topics_str}.
    
    Please generate a concise, personalized 3-step study plan tailored to their specific weaknesses and current ability level.
    """
    
    variables = {
        "difficulty_reached": difficulty_reached,
        "missed_topics_str": missed_topics_str
    }
    
    # 2. Optimize prompt for token usage
    # We'll use a conservative max prompt tokens (e.g., 1000) to allow room for the generated response
    final_prompt = optimize_prompt(base_prompt, variables, max_prompt_tokens=1000)
    
    system_message = "You are an expert tutor providing focused, actionable study advice."
    
    # 3. Generate response using our unified provider
    try:
        response_text = generate_content(
            prompt=final_prompt,
            system_message=system_message,
            max_tokens=800,
            temperature=0.7
        )
        return response_text
    except Exception as e:
        return f"Could not generate study plan at this time. Error: {str(e)}"