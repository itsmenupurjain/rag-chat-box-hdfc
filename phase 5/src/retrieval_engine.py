"""
Phase 5: Retrieval Engine
Searches vector database for relevant chunks based on user query
"""

import os
import sys
import json
import pickle
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.logger import setup_logger

logger = setup_logger("phase5_retrieval", "phase5_retrieval.log")


class RetrievalEngine:
    """Retrieves relevant documents from vector database"""
    
    def __init__(self, vectors_dir=None, model_name='all-MiniLM-L6-v2'):
        self.model_name = model_name
        
        if vectors_dir is None:
            self.data_dir = os.path.dirname(os.path.dirname(__file__))
            self.vectors_dir = os.path.join(self.data_dir, "data", "vectors")
        else:
            self.vectors_dir = vectors_dir
        
        logger.info("Loading vector database...")
        self._load_database()
        
        logger.info("Loading embedding model...")
        self.model = SentenceTransformer(model_name)
        logger.info("RetrievalEngine ready")
    
    def _load_database(self):
        """Load FAISS index and metadata"""
        # Load FAISS index
        index_path = os.path.join(self.vectors_dir, 'faiss_index.bin')
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"FAISS index not found: {index_path}")
        
        self.index = faiss.read_index(index_path)
        logger.info(f"Loaded FAISS index: {self.index.ntotal} vectors")
        
        # Load metadata
        metadata_path = os.path.join(self.vectors_dir, 'metadata.pkl')
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Metadata not found: {metadata_path}")
        
        with open(metadata_path, 'rb') as f:
            self.metadata = pickle.load(f)
        logger.info(f"Loaded metadata: {len(self.metadata)} entries")
        
        # Load config
        config_path = os.path.join(self.vectors_dir, 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f)
    
    def search(self, query, top_k=5):
        """Search for relevant chunks"""
        # Create query embedding
        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding).astype('float32')
        
        # Search FAISS index
        distances, indices = self.index.search(query_embedding, top_k)
        
        # Retrieve metadata for matched chunks
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.metadata):
                chunk_data = self.metadata.iloc[idx].to_dict()
                chunk_data['distance'] = float(dist)
                chunk_data['similarity_score'] = float(1 / (1 + dist))  # Convert to similarity
                results.append(chunk_data)
        
        logger.info(f"Query: '{query[:50]}...'")
        logger.info(f"Retrieved {len(results)} chunks")
        
        return results
    
    def get_context(self, query, top_k=5, max_context_length=2000):
        """Get formatted context for LLM"""
        results = self.search(query, top_k)
        
        context_parts = []
        total_length = 0
        
        for chunk in results:
            text = chunk.get('text', '')
            scheme = chunk.get('scheme_name', '')
            chunk_type = chunk.get('chunk_type', '')
            
            # Format chunk
            formatted = f"[Scheme: {scheme}] [Type: {chunk_type}]\n{text}"
            
            # Check if adding this chunk exceeds max length
            if total_length + len(formatted) > max_context_length:
                break
            
            context_parts.append(formatted)
            total_length += len(formatted)
        
        context = "\n\n".join(context_parts)
        
        return context, results


def main():
    """Test Phase 5 retrieval"""
    logger.info("=" * 70)
    logger.info("PHASE 5: Testing Retrieval Engine")
    logger.info("=" * 70)
    
    try:
        engine = RetrievalEngine()
        
        # Test queries
        test_queries = [
            "What is the minimum SIP amount?",
            "Explain exit load for HDFC Mid-Cap Fund",
            "What are the returns of HDFC Equity Fund?"
        ]
        
        for query in test_queries:
            logger.info(f"\n{'='*50}")
            logger.info(f"Query: {query}")
            logger.info("=" * 50)
            
            results = engine.search(query, top_k=3)
            
            for i, chunk in enumerate(results, 1):
                logger.info(f"\nResult {i}:")
                logger.info(f"  Scheme: {chunk.get('scheme_name', 'N/A')}")
                logger.info(f"  Type: {chunk.get('chunk_type', 'N/A')}")
                logger.info(f"  Similarity: {chunk.get('similarity_score', 0):.4f}")
                logger.info(f"  Text: {chunk.get('text', '')[:100]}...")
        
        logger.info("\n" + "=" * 70)
        logger.info("PHASE 5 RETRIEVAL ENGINE READY")
        logger.info("=" * 70)
        
    except FileNotFoundError as e:
        logger.error(f"Database not found: {e}")
        logger.error("Run Phase 4 first to build vector database")
        sys.exit(1)


if __name__ == "__main__":
    main()
