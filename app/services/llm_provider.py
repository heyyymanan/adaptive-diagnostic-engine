import os
from openai import OpenAI
import google.generativeai as genai

# Try to load existing OpenAI client if key is present
openai_client = None
if os.getenv("OPENAI_API_KEY"):
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Try to configure Gemini if key is present
if os.getenv("GEMINI_API_KEY"):
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_content(prompt: str, system_message: str = "", max_tokens: int = 800, temperature: float = 0.7) -> str:
    """
    Generates content using the configured LLM provider.
    Expects LLM_PROVIDER env variable to be 'gemini' or 'open-ai'. Defaults to 'gemini'.
    """
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    
    if provider == "open-ai":
        if not openai_client:
            return "Error: OPENAI_API_KEY is not configured."
        try:
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})

            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"OpenAI Provider Error: {str(e)}"
            
    elif provider == "gemini":
        if not os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") == "your_gemini_api_key_here":
            return "Error: GEMINI_API_KEY is not configured correctly."
        try:
            # Gemini models: gemini-2.5-flash is the standard fast & free tier model
            model = genai.GenerativeModel('gemini-2.5-flash',
                system_instruction=system_message if system_message else None
            )
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens,
                    temperature=temperature,
                )
            )
            return response.text.strip()
        except Exception as e:
            return f"Gemini Provider Error: {str(e)}"
    
    else:
        return f"Error: Unknown LLM provider '{provider}'. Please use 'gemini' or 'open-ai'."
