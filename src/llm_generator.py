import os
import time
from groq import Groq
from dotenv import load_dotenv
from src.logger import setup_logger

load_dotenv()
logger = setup_logger("llm_generator", "app.log")

# Primary and fallback models (updated Sept 2026 — llama-3.3-70b-versatile was deprecated by Groq)
PRIMARY_MODEL = "qwen/qwen3.8-27b"
FALLBACK_MODEL = "allam-2-7b"

class LLMGenerator:
    def __init__(self, model_name=PRIMARY_MODEL):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            logger.error("GROQ_API_KEY not found! Set it as an environment variable.")
        
        # Only create client if key exists — prevents crash on startup
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        self.model_name = model_name
        self.fallback_model = FALLBACK_MODEL
        self.max_retries = 3
        
        self.system_prompt = """
You are a facts-only mutual fund FAQ assistant. Your role is to provide 
accurate, verifiable information about mutual fund schemes using ONLY 
the provided context from official sources.

RULES:
1. Answer ONLY using information from the provided context.
2. If the information is not in the context, say: "I'm sorry, but I don't have that specific information in my current records."
3. Maximum 3 sentences per response.
4. Include EXACTLY ONE source citation link from the context at the end.
5. NEVER provide investment advice, recommendations, or personal opinions.
6. NEVER say "I recommend", "You should", "This is better", or "I think".
7. Be concise, factual, and precise.
8. Do NOT include any thinking, reasoning, or internal monologue tags in your response.
"""
        
    def _call_groq(self, model, user_prompt):
        """Makes a single API call to Groq with the given model."""
        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,  # Low temperature for factual consistency
            max_tokens=200
        )
        response = completion.choices[0].message.content
        
        # Strip any <think>...</think> tags some models emit
        if response and "<think>" in response:
            import re
            response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()
        
        return response

    def generate_response(self, query, context_chunks):
        """
        Generates a factual response using Groq LLM with retry and fallback logic.
        """
        if not self.client:
            return "Service configuration error: GROQ_API_KEY is not set. Please contact the administrator."
        
        if not context_chunks:
            return "I'm sorry, I couldn't find any relevant factual information to answer your query."

        # Format context for prompt
        context_text = "\n\n".join([c['text'] for c in context_chunks])
        
        user_prompt = f"""
Context from official sources:
{context_text}

User Query: {query}

Provide a factual response following all rules.
"""

        # Try primary model with retries
        models_to_try = [self.model_name, self.fallback_model]
        
        for model in models_to_try:
            for attempt in range(1, self.max_retries + 1):
                try:
                    logger.info(f"Sending request to Groq (model={model}, attempt={attempt}/{self.max_retries})")
                    response = self._call_groq(model, user_prompt)
                    
                    if response and response.strip():
                        logger.info(f"Successfully generated LLM response using {model}.")
                        return response
                    else:
                        logger.warning(f"Empty response from {model} on attempt {attempt}.")
                        
                except Exception as e:
                    logger.error(f"Error during LLM generation (model={model}, attempt={attempt}): {type(e).__name__}: {e}")
                    if attempt < self.max_retries:
                        wait_time = 2 ** attempt  # Exponential backoff: 2s, 4s, 8s
                        logger.info(f"Retrying in {wait_time}s...")
                        time.sleep(wait_time)
            
            logger.warning(f"All {self.max_retries} attempts failed for model '{model}'. Trying fallback...")
        
        logger.error("All models and retries exhausted. Returning error to user.")
        return "I encountered an error while generating the response. Please try again later."
