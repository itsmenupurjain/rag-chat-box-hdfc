import os
import re
import sys
from src.embedding_engine import EmbeddingEngine
from src.vector_store import SimpleVectorStore
from src.logger import setup_logger

# Fix Windows console encoding — safe for Linux
try:
    if sys.stdout and hasattr(sys.stdout, 'reconfigure') and sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

logger = setup_logger("retrieval_engine", "retrieval.log")

class RetrievalEngine:
    def __init__(self, vectors_dir=os.path.join("data", "vectors")):
        self.vectors_dir = vectors_dir
        
        # 1. Initialize and load embedding engine (with vectorizer fallback)
        self.embedding_engine = EmbeddingEngine()
        vectorizer_path = os.path.join(vectors_dir, "vectorizer.pkl")
        if os.path.exists(vectorizer_path):
            self.embedding_engine.load_vectorizer(vectorizer_path)
            
        # 2. Load vector store
        self.vector_store = SimpleVectorStore.load(vectors_dir)
        if not self.vector_store:
            logger.error(f"Failed to load vector store from {vectors_dir}")

    def preprocess_query(self, query):
        """
        Normalizes the user query for better matching.
        Keeps common financial terms intact.
        """
        # Lowercase
        query = query.lower().strip()
        # Remove special characters except common MF terms
        query = re.sub(r'[^a-zA-Z0-9\s\-₹%]', '', query)
        
        # NOTE: Aggressive abbreviation replacement removed as it conflicts with TF-IDF 
        # when the source text uses abbreviations (e.g. "ELSS").
            
        logger.info(f"Cleaned query: {query}")
        return query

    def retrieve_context(self, query, k=5):
        """
        Full retrieval pipeline: preprocess -> embed -> search -> assemble.
        Increased default k to 5 for better recall.
        """
        if not self.vector_store:
            return []

        # 1. Preprocess
        clean_query = self.preprocess_query(query)
        
        # 2. Generate Embedding
        query_vector = self.embedding_engine.get_embeddings(clean_query)
        
        if query_vector is None:
            logger.error("Failed to generate query embedding.")
            return []

        # 3. Search
        results = self.vector_store.search(query_vector[0], k=k)
        
        # 4. Assemble context
        context_chunks = []
        for res in results:
            metadata = res['metadata']
            score = res.get('score', 0)
            
            chunk_text = metadata.get('content', '')
            source_url = metadata.get('url', 'N/A')
            scheme_name = metadata.get('scheme', 'Unknown')
            
            formatted_chunk = f"[Source: {source_url} | Scheme: {scheme_name}]\n{chunk_text}"
            context_chunks.append({
                "text": formatted_chunk,
                "url": source_url,
                "score": score,
                "scheme": scheme_name
            })
            
        logger.info(f"Retrieved {len(context_chunks)} chunks for query: {query}")
        return context_chunks
