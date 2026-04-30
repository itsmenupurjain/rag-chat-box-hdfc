"""
Phase 6: LLM Integration & Response Generation
Generates facts-only responses using Groq API with strict constraints
"""

import os
import sys
import json
from groq import Groq
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.logger import setup_logger

logger = setup_logger("phase6_llm", "phase6_llm.log")


class LLMEngine:
    """Handles LLM integration with facts-only constraints"""
    
    def __init__(self, api_key=None, model="llama-3.3-70b-versatile"):
        # Load API key
        load_dotenv()
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found. Please set it in .env file")
        
        self.model = model
        self.client = Groq(api_key=self.api_key)
        
        self.system_prompt = """You are a factual mutual fund information assistant specializing in HDFC Mutual Funds.

CRITICAL RULES - YOU MUST FOLLOW THESE STRICTLY:

1. ONLY use information from the provided context
2. MAXIMUM 3 SENTENCES in your response
3. Include EXACTLY 1 citation from the context at the end
4. NEVER give investment advice or recommendations
5. NEVER make up information not in the context
6. If information is not in context, say "I don't have that information in my current data"
7. Keep responses factual, concise, and helpful
8. Format citation as: [Source: Scheme Name, chunk_type]

RESPONSE FORMAT:
[Your factual answer - maximum 3 sentences]

[Source: Scheme Name, chunk_type]"""
        
        logger.info(f"LLMEngine initialized with model: {model}")
    
    def generate_response(self, query, context):
        """Generate response with context"""
        
        prompt = f"""Context:
{context}

User Question: {query}

Remember: Maximum 3 sentences, exactly 1 citation, facts only."""
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.1,  # Low temperature for factual responses
                max_tokens=300,
                top_p=0.9
            )
            
            answer = response.choices[0].message.content.strip()
            
            logger.info(f"Generated response: {answer[:100]}...")
            return answer
            
        except Exception as e:
            logger.error(f"LLM API error: {str(e)}")
            return f"Error generating response: {str(e)}"
    
    def ask(self, query, retrieval_engine, top_k=5):
        """Complete RAG pipeline: retrieve + generate"""
        
        # Get relevant context
        context, results = retrieval_engine.get_context(query, top_k=top_k)
        
        if not context:
            return "I don't have sufficient information to answer that question based on my current data."
        
        # Generate response
        response = self.generate_response(query, context)
        
        return response, results


def main():
    """Test Phase 6 LLM integration"""
    logger.info("=" * 70)
    logger.info("PHASE 6: Testing LLM Integration")
    logger.info("=" * 70)
    
    try:
        from phase5.src.retrieval_engine import RetrievalEngine
        
        # Initialize components
        retrieval = RetrievalEngine()
        llm = LLMEngine()
        
        # Test queries
        test_queries = [
            "What is the minimum SIP amount for HDFC funds?",
            "What is the exit load for HDFC Mid-Cap Fund?",
            "What are the risk factors for these funds?"
        ]
        
        for query in test_queries:
            logger.info(f"\n{'='*60}")
            logger.info(f"Q: {query}")
            logger.info("=" * 60)
            
            response, results = llm.ask(query, retrieval, top_k=3)
            
            logger.info(f"\nA: {response}")
            logger.info(f"\nRetrieved {len(results)} chunks")
        
        logger.info("\n" + "=" * 70)
        logger.info("PHASE 6 LLM INTEGRATION READY")
        logger.info("=" * 70)
        
    except FileNotFoundError:
        logger.error("Vector database not found. Run Phase 4 first.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
