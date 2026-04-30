"""
Phase 4: Vector Database & Embeddings
Creates embeddings and stores in FAISS vector database
"""

import os
import sys
import json
import pickle
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.logger import setup_logger

logger = setup_logger("phase4_vectors", "phase4_vectors.log")


class VectorDatabase:
    """Creates and manages vector embeddings"""
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model_name = model_name
        self.data_dir = os.path.dirname(os.path.dirname(__file__))
        self.processed_dir = os.path.join(self.data_dir, "data", "processed")
        self.vectors_dir = os.path.join(self.data_dir, "data", "vectors")
        
        os.makedirs(self.vectors_dir, exist_ok=True)
        
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        logger.info("Model loaded successfully")
    
    def load_chunks(self):
        """Load document chunks from parquet"""
        chunks_path = os.path.join(self.processed_dir, 'chunks.parquet')
        
        if not os.path.exists(chunks_path):
            logger.error(f"Chunks file not found: {chunks_path}")
            logger.error("Run Phase 3 first to process documents")
            return None
        
        df = pd.read_parquet(chunks_path)
        logger.info(f"Loaded {len(df)} chunks")
        return df
    
    def create_embeddings(self, texts):
        """Create embeddings for a list of texts"""
        logger.info(f"Creating embeddings for {len(texts)} texts...")
        embeddings = self.model.encode(texts, show_progress_bar=True)
        logger.info(f"Embeddings shape: {embeddings.shape}")
        return embeddings
    
    def build_faiss_index(self, embeddings):
        """Build FAISS index from embeddings"""
        dimension = embeddings.shape[1]
        
        # Create L2 index
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        
        logger.info(f"FAISS index built: {index.ntotal} vectors, dimension: {dimension}")
        return index
    
    def save_vector_db(self, index, metadata_df):
        """Save vector database and metadata"""
        # Save FAISS index
        index_path = os.path.join(self.vectors_dir, 'faiss_index.bin')
        faiss.write_index(index, index_path)
        logger.info(f"Saved FAISS index: {index_path}")
        
        # Save metadata
        metadata_path = os.path.join(self.vectors_dir, 'metadata.pkl')
        with open(metadata_path, 'wb') as f:
            pickle.dump(metadata_df, f)
        logger.info(f"Saved metadata: {metadata_path}")
        
        # Save model name
        config = {
            'model_name': self.model_name,
            'num_vectors': index.ntotal,
            'dimension': index.d
        }
        config_path = os.path.join(self.vectors_dir, 'config.json')
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        logger.info(f"Saved config: {config_path}")
    
    def build_database(self):
        """Main method to build vector database"""
        logger.info("=" * 70)
        logger.info("PHASE 4: Building Vector Database")
        logger.info("=" * 70)
        
        # Load chunks
        chunks_df = self.load_chunks()
        if chunks_df is None:
            return None
        
        # Extract texts
        texts = chunks_df['text'].tolist()
        
        # Create embeddings
        embeddings = self.create_embeddings(texts)
        embeddings = np.array(embeddings).astype('float32')
        
        # Build FAISS index
        index = self.build_faiss_index(embeddings)
        
        # Save everything
        self.save_vector_db(index, chunks_df)
        
        # Summary
        logger.info("\n" + "=" * 70)
        logger.info("PHASE 4 VECTOR DATABASE COMPLETE")
        logger.info("=" * 70)
        logger.info(f"Total vectors: {index.ntotal}")
        logger.info(f"Vector dimension: {index.d}")
        logger.info(f"Model: {self.model_name}")
        logger.info(f"Saved to: {self.vectors_dir}")
        
        return index, chunks_df


def main():
    """Run Phase 4 vector database creation"""
    vector_db = VectorDatabase(model_name='all-MiniLM-L6-v2')
    result = vector_db.build_database()
    
    if result:
        index, metadata = result
        logger.info("\n✅ Phase 4 completed successfully!")
        logger.info(f"   - {index.ntotal} vectors created")
        logger.info(f"   - Saved to data/vectors/")
    else:
        logger.error("\n❌ Phase 4 failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
