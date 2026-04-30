import numpy as np
import os
import pickle
from src.logger import setup_logger

logger = setup_logger("vector_store", "indexing.log")

class SimpleVectorStore:
    """
    A pure-Python, Numpy-based vector store. 
    No external C++ dependencies (like Chroma or FAISS).
    Perfect for small to medium datasets.
    """
    def __init__(self, directory):
        self.directory = directory
        self.embeddings = []
        self.metadata = []

    def add_documents(self, embeddings, metadata):
        """
        Adds embeddings and their corresponding metadata.
        """
        if len(embeddings) != len(metadata):
            raise ValueError("Embeddings and metadata must have the same length")
        
        if len(self.embeddings) == 0:
            self.embeddings = np.array(embeddings)
        else:
            self.embeddings = np.vstack([self.embeddings, np.array(embeddings)])
            
        self.metadata.extend(metadata)
        logger.info(f"Added {len(embeddings)} documents to SimpleVectorStore")

    def search(self, query_embedding, k=5):
        """
        Searches for top k similar documents using Cosine Similarity.
        """
        if len(self.embeddings) == 0:
            return []
            
        # Normalize embeddings for cosine similarity
        norm_embeddings = self.embeddings / np.linalg.norm(self.embeddings, axis=1, keepdims=True)
        norm_query = query_embedding / np.linalg.norm(query_embedding)
        
        # Calculate similarities
        similarities = np.dot(norm_embeddings, norm_query)
        
        # Get top k indices
        top_k_indices = np.argsort(similarities)[::-1][:k]
        
        results = []
        for idx in top_k_indices:
            results.append({
                "metadata": self.metadata[idx],
                "score": float(similarities[idx])
            })
        return results

    def save(self):
        """
        Saves the embeddings and metadata to disk.
        """
        os.makedirs(self.directory, exist_ok=True)
        np.save(os.path.join(self.directory, "embeddings.npy"), self.embeddings)
        with open(os.path.join(self.directory, "metadata.pkl"), "wb") as f:
            pickle.dump(self.metadata, f)
        logger.info(f"Saved SimpleVectorStore to {self.directory}")

    @classmethod
    def load(cls, directory):
        """
        Loads the store from disk.
        """
        instance = cls(directory)
        emp_path = os.path.join(directory, "embeddings.npy")
        meta_path = os.path.join(directory, "metadata.pkl")
        
        if os.path.exists(emp_path) and os.path.exists(meta_path):
            instance.embeddings = np.load(emp_path)
            with open(meta_path, "rb") as f:
                instance.metadata = pickle.load(f)
            logger.info(f"Loaded SimpleVectorStore from {directory}")
            return instance
        return None
