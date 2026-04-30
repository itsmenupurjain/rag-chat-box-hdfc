import os
from groq import Groq
from dotenv import load_dotenv
from src.logger import setup_logger

load_dotenv()
logger = setup_logger("llm_generator", "app.log")

class LLMGenerator:
    def __init__(self, model_name="llama-3.3-70b-versatile"):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            logger.error("GROQ_API_KEY not found! Set it as an environment variable.")
        
        # Only create client if key exists — prevents crash on startup
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        self.model_name = model_name
        
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
"""

    def generate_response(self, query, context_chunks):
        """
        Generates a factual response using Groq and Llama 3.
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

        try:
            logger.info(f"Sending request to Groq ({self.model_name})")
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1, # Low temperature for factual consistency
                max_tokens=200
            )
            
            response = completion.choices[0].message.content
            logger.info("Successfully generated LLM response.")
            return response
            
        except Exception as e:
            logger.error(f"Error during LLM generation: {e}")
            return "I encountered an error while generating the response. Please try again later."
