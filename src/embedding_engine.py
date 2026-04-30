import requests
import time
import os
import numpy as np
import pickle
from dotenv import load_dotenv
from src.logger import setup_logger
from sklearn.feature_extraction.text import TfidfVectorizer

load_dotenv()
logger = setup_logger("embedding_engine", "indexing.log")

class EmbeddingEngine:
    def __init__(self, model_id="sentence-transformers/all-MiniLM-L6-v2"):
        self.api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
        self.hf_token = os.getenv("HF_TOKEN")
        self.use_fallback = False
        self.vectorizer = None
        
        if not self.hf_token or "your_huggingface_token" in self.hf_token:
            logger.warning("HF_TOKEN not found or placeholder used. Using TF-IDF (local).")
            self.use_fallback = True
            self.vectorizer = TfidfVectorizer(stop_words='english')
        
        self.headers = {"Authorization": f"Bearer {self.hf_token}"}

    def get_embeddings(self, texts, fit=False):
        """
        Generates embeddings. fit=True is used during indexing for TF-IDF.
        """
        if isinstance(texts, str):
            texts = [texts]

        if self.use_fallback:
            if fit:
                logger.info(f"Fitting TF-IDF on {len(texts)} chunks")
                return self.vectorizer.fit_transform(texts).toarray()
            else:
                try:
                    return self.vectorizer.transform(texts).toarray()
                except Exception as e:
                    logger.error(f"TF-IDF transform failed: {e}. Was vectorizer fit?")
                    return None

        # HF API path
        logger.info(f"Requesting embeddings for {len(texts)} chunks via HF API")
        try:
            response = requests.post(
                self.api_url, 
                headers=self.headers, 
                json={"inputs": texts, "options": {"wait_for_model": True}},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"HF API Error {response.status_code}: {response.text}")
                if response.status_code == 503:
                    logger.info("Model is loading, retrying in 10s...")
                    time.sleep(10)
                    return self.get_embeddings(texts)
                return None
        except Exception as e:
            logger.error(f"Exception during HF API call: {e}")
            return None

    def save_vectorizer(self, path):
        if self.use_fallback and self.vectorizer:
            with open(path, 'wb') as f:
                pickle.dump(self.vectorizer, f)
            logger.info(f"Saved TF-IDF vectorizer to {path}")

    def load_vectorizer(self, path):
        if os.path.exists(path):
            with open(path, 'rb') as f:
                self.vectorizer = pickle.load(f)
            self.use_fallback = True
            logger.info(f"Loaded TF-IDF vectorizer from {path}")
            return True
        return False
