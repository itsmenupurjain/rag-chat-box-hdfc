"""
Phase 3: Document Processing & Chunking
Processes raw HTML data into chunks suitable for vector embedding
"""

import os
import sys
import json
import pandas as pd
import re

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.logger import setup_logger

logger = setup_logger("phase3_processing", "phase3_processing.log")


class DocumentProcessor:
    """Processes documents and creates chunks for embedding"""
    
    def __init__(self, chunk_size=500, chunk_overlap=50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        
        self.data_dir = os.path.dirname(os.path.dirname(__file__))
        self.processed_dir = os.path.join(self.data_dir, "data", "processed")
        
        logger.info("DocumentProcessor initialized")
        logger.info(f"Chunk size: {chunk_size}, overlap: {chunk_overlap}")
    
    def load_processed_data(self):
        """Load processed scheme data from parquet"""
        data_path = os.path.join(self.processed_dir, 'schemes_data.parquet')
        
        if not os.path.exists(data_path):
            logger.error(f"Data file not found: {data_path}")
            logger.error("Run Phase 2 first to ingest data")
            return None
        
        df = pd.read_parquet(data_path)
        logger.info(f"Loaded {len(df)} schemes from processed data")
        return df
    
    def clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s.,;:!?\-()%/]', '', text)
        # Normalize
        text = text.strip()
        
        return text
    
    def create_chunks(self, text, metadata=None):
        """Split text into overlapping chunks"""
        if not text:
            return []
        
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            if len(chunk_words) < 50:  # Skip very small chunks
                continue
            
            chunk = {
                'text': chunk_text,
                'chunk_id': len(chunks),
                'word_count': len(chunk_words)
            }
            
            if metadata:
                chunk.update(metadata)
            
            chunks.append(chunk)
        
        return chunks
    
    def process_scheme(self, row):
        """Process a single scheme and create chunks"""
        chunks = []
        
        # Combine all relevant text
        full_text = row.get('full_text', '')
        description = row.get('description', '')
        key_features = ' '.join(row.get('key_features', []))
        
        # Create metadata
        metadata = {
            'scheme_name': row.get('scheme_name', ''),
            'category': row.get('category', ''),
            'plan': row.get('plan', ''),
            'risk_level': row.get('risk_level', ''),
            'source_url': row.get('source_url', '')
        }
        
        # Chunk full text
        if full_text:
            full_chunks = self.create_chunks(full_text, metadata.copy())
            full_chunks_metadata = [{'chunk_type': 'full_text', **c} for c in full_chunks]
            chunks.extend(full_chunks_metadata)
            logger.info(f"Created {len(full_chunks)} chunks from full text")
        
        # Chunk description separately
        if description:
            desc_chunks = self.create_chunks(description, metadata.copy())
            desc_chunks_metadata = [{'chunk_type': 'description', **c} for c in desc_chunks]
            chunks.extend(desc_chunks_metadata)
            logger.info(f"Created {len(desc_chunks)} chunks from description")
        
        # Chunk key features
        if key_features:
            feature_chunks = self.create_chunks(key_features, metadata.copy())
            feature_chunks_metadata = [{'chunk_type': 'key_features', **c} for c in feature_chunks]
            chunks.extend(feature_chunks_metadata)
            logger.info(f"Created {len(feature_chunks)} chunks from features")
        
        return chunks
    
    def process_all(self):
        """Process all schemes and create chunks"""
        logger.info("=" * 70)
        logger.info("PHASE 3: Starting Document Processing")
        logger.info("=" * 70)
        
        # Load data
        df = self.load_processed_data()
        if df is None:
            return None
        
        all_chunks = []
        
        # Process each scheme
        for idx, row in df.iterrows():
            logger.info(f"\nProcessing: {row['scheme_name']}")
            chunks = self.process_scheme(row)
            all_chunks.extend(chunks)
        
        # Save chunks
        if all_chunks:
            chunks_df = pd.DataFrame(all_chunks)
            chunks_path = os.path.join(self.processed_dir, 'chunks.parquet')
            chunks_df.to_parquet(chunks_path, index=False)
            logger.info(f"\nSaved {len(all_chunks)} chunks to: {chunks_path}")
            
            # Summary
            logger.info("\n" + "=" * 70)
            logger.info("PHASE 3 PROCESSING COMPLETE")
            logger.info("=" * 70)
            logger.info(f"Total chunks created: {len(all_chunks)}")
            logger.info(f"Chunk size: {self.chunk_size} words")
            logger.info(f"Chunk overlap: {self.chunk_overlap} words")
            logger.info(f"Average chunks per scheme: {len(all_chunks) / len(df):.1f}")
        
        return all_chunks


def main():
    """Run Phase 3 processing"""
    processor = DocumentProcessor(chunk_size=500, chunk_overlap=50)
    chunks = processor.process_all()
    
    if chunks:
        logger.info("\n✅ Phase 3 completed successfully!")
        logger.info(f"   - {len(chunks)} document chunks created")
        logger.info(f"   - Saved to data/processed/chunks.parquet")
    else:
        logger.error("\n❌ Phase 3 failed - no chunks created")
        sys.exit(1)


if __name__ == "__main__":
    main()
