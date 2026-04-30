from src.retrieval_engine import RetrievalEngine
from src.llm_generator import LLMGenerator
from src.response_validator import ResponseValidator
from src.refusal_handler import RefusalHandler
from src.logger import setup_logger
import sys

# Fix Windows console encoding — safe for Linux
try:
    if sys.stdout and hasattr(sys.stdout, 'reconfigure') and sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

logger = setup_logger("rag_assistant", "app.log")

class MutualFundAssistant:
    def __init__(self):
        self.retrieval_engine = RetrievalEngine()
        self.llm_generator = LLMGenerator()
        self.validator = ResponseValidator()
        self.refusal_handler = RefusalHandler()

    def ask(self, query):
        logger.info(f"Received query: {query}")
        
        # 0. Check for Greeting
        if self.refusal_handler.is_greeting(query):
            return self.refusal_handler.get_greeting_response()
            
        # 0.5 Check for Advisory Query (Refusal Handler)
        if self.refusal_handler.is_advisory_query(query):
            return self.refusal_handler.get_refusal_response()
        
        # 1. Retrieve relevant context
        context_chunks = self.retrieval_engine.retrieve_context(query, k=8)
        
        if not context_chunks:
            return "I'm sorry, I couldn't find any factual information about that specific query in the HDFC Mutual Fund records I have."

        # 2. Generate response
        raw_response = self.llm_generator.generate_response(query, context_chunks)
        
        # 3. Validate and Clean
        is_valid, reason = self.validator.validate(raw_response, context_chunks)
        final_response = self.validator.clean_and_format(raw_response, context_chunks)
        
        return final_response

if __name__ == "__main__":
    assistant = MutualFundAssistant()
    test_queries = ["hi", "h", "NAV of HDFC Mid Cap?"]
    for q in test_queries:
        print(f"\nUser: {q}")
        print(f"Assistant: {assistant.ask(q)}")
