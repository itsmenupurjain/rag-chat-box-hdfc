import os
from src.document_processor import DocumentProcessor
from src.embedding_engine import EmbeddingEngine
from src.vector_store import SimpleVectorStore
from src.logger import setup_logger

logger = setup_logger("indexing_orchestrator", "indexing.log")

PROCESSED_DIR = os.path.join("data", "processed")
VECTORS_DIR = os.path.join("data", "vectors")

def run_indexing():
    logger.info("Starting Phase 3: Vectorization & Indexing")
    
    # 1. Initialize components
    processor = DocumentProcessor()
    embedding_engine = EmbeddingEngine()
    
    # 2. Process documents to chunks
    if not os.path.exists(PROCESSED_DIR):
        logger.error(f"Processed directory {PROCESSED_DIR} does not exist. Run Phase 2 first.")
        return
        
    chunks = processor.process_directory(PROCESSED_DIR)
    if not chunks:
        logger.warning("No chunks found to index.")
        return
        
    # 3. Generate embeddings
    texts = [chunk["content"] for chunk in chunks]
    metadata = [chunk["metadata"] for chunk in chunks]
    
    # Add content itself to metadata for easier retrieval later
    for i, m in enumerate(metadata):
        m["content"] = texts[i]
        
    embeddings = embedding_engine.get_embeddings(texts, fit=True)
    
    # Save vectorizer if in fallback mode
    if embedding_engine.use_fallback:
        embedding_engine.save_vectorizer(os.path.join(VECTORS_DIR, "vectorizer.pkl"))
    
    # 4. Create and save vector store
    vector_store = SimpleVectorStore(VECTORS_DIR)
    vector_store.add_documents(embeddings, metadata)
    vector_store.save()
    
    logger.info("Phase 3 Implementation Complete")

if __name__ == "__main__":
    run_indexing()
