import re
from src.logger import setup_logger

logger = setup_logger("refusal_handler", "app.log")

class RefusalHandler:
    def __init__(self):
        self.advisory_patterns = [
            r"should i invest",
            r"is it good to invest",
            r"which (fund|scheme) is better",
            r"best (fund|scheme)",
            r"recommend",
            r"suggest a (fund|scheme)",
            r"where to invest",
            r"is this a good (fund|scheme)",
            r"predict",
            r"future returns",
            r"how much return will i get"
        ]
        
        # Using strict word boundaries and full matches for greetings
        self.greeting_patterns = [
            r"hi", r"hello", r"hey", r"h", r"hola", r"greetings",
            r"hi there", r"hello there", r"hey there"
        ]
        
        self.refusal_message = (
            "I can't provide investment advice or recommendations. My role is to "
            "share only factual, publicly available information about mutual fund schemes.\n\n"
            "For investment guidance, you may consult a SEBI-registered financial advisor "
            "or visit AMFI's investor education page: https://www.amfiindia.com/investor-awareness\n\n"
            "Facts-only. No investment advice."
        )
        
        self.greeting_message = (
            "Hello! I am your HDFC Mutual Fund FAQ Assistant. I can provide you with "
            "factual details like NAV, Expense Ratio, and Fund Manager information for HDFC schemes. "
            "How can I help you today?"
        )

    def is_advisory_query(self, query):
        query = query.lower().strip()
        for pattern in self.advisory_patterns:
            if re.search(pattern, query):
                return True
        return False

    def is_greeting(self, query):
        """
        Detects if a query is just a simple greeting.
        """
        # Clean query: lowercase, strip, and remove all non-alphanumeric at ends
        query = query.lower().strip()
        clean_query = re.sub(r'[^a-z0-9 ]', '', query)
        
        # Check for exact matches in the list
        if clean_query in self.greeting_patterns:
            logger.info(f"Greeting detected: '{clean_query}'")
            return True
            
        # Also handle "how are you" etc.
        if "how are you" in clean_query or "how are u" in clean_query:
            return True
            
        return False

    def get_refusal_response(self):
        return self.refusal_message
        
    def get_greeting_response(self):
        return self.greeting_message
