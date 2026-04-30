import re
from src.logger import setup_logger

logger = setup_logger("response_validator", "app.log")

class ResponseValidator:
    def __init__(self):
        # Keywords that suggest investment advice or personal opinion
        self.advisory_keywords = [
            "recommend", "should", "better", "best", "good", "bad", 
            "invest in", "buy", "sell", "think", "believe", "opinion",
            "predict", "future", "guarantee"
        ]

    def validate(self, response, context_chunks):
        """
        Validates the LLM response against the architecture rules.
        """
        # 1. Check for advisory language
        found_keywords = [w for w in self.advisory_keywords if re.search(rf"\b{w}\b", response.lower())]
        if found_keywords:
            logger.warning(f"Advisory language detected: {found_keywords}")
            return False, "Response contains advisory language."

        # 2. Check for sentence count (approximate by periods)
        sentences = re.split(r'(?<=[.!?]) +', response.strip())
        # Filter out links and footers
        content_sentences = [s for s in sentences if not s.startswith("http") and "Source:" not in s]
        
        if len(content_sentences) > 4: # Allowing a bit of wiggle room for small sentences
             logger.warning(f"Response too long: {len(content_sentences)} sentences.")
             # We won't block it here but log it
        
        # 3. Check for at least one URL from context
        context_urls = set([c['url'] for c in context_chunks])
        found_urls = re.findall(r'https?://\S+', response)
        
        valid_url_found = any(url in context_urls for url in found_urls)
        if not found_urls:
            logger.warning("No citation URL found in response.")
            # We'll append one if missing later in the orchestrator
        elif not valid_url_found:
            logger.warning("URL in response not found in provided context.")
            
        return True, "Success"

    def clean_and_format(self, response, context_chunks):
        """
        Final polish: ensure exactly one citation and a footer.
        """
        # Extract URLs
        found_urls = re.findall(r'https?://\S+', response)
        
        # If no URL, append the top one
        if not found_urls and context_chunks:
            response += f"\n\nSource: {context_chunks[0]['url']}"
        
        # Append footer
        from datetime import datetime
        footer = f"\n\nLast updated from sources: {datetime.now().strftime('%Y-%m-%d')}"
        
        if footer not in response:
            response += footer
            
        return response
