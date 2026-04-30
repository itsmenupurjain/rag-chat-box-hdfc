# Phase 3: Vectorization & Indexing

## Overview
This phase involves converting the processed mutual fund data into vector embeddings and storing them in a vector database for efficient similarity search.

## Technology Stack
- **Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions)
- **Vector Database:** ChromaDB (Persistent)
- **Storage Path:** `data/vectors/`

## Components

### 1. Document Processor (`src/document_processor.py`)
- Converts structured JSON data into self-contained factual chunks.
- Chunks are organized by section: Overview, Costs & Value, Investment, Risk, and Analysis (Pros/Cons).
- Metadata includes scheme name, source URL, and section type.

### 2. Embedding Engine (`src/embedding_engine.py`)
- Wrapper for SentenceTransformer.
- Generates 384-dimensional vectors for text chunks.

### 3. Vector Store (`src/vector_store.py`)
- Manages ChromaDB collection.
- Handles persistent storage and similarity search.

### 4. Indexing Orchestrator (`src/index_data.py`)
- Coordinates the flow from processed files to the vector store.

## Current Progress
- [x] Dependency Installation (sentence-transformers, chromadb)
- [x] Document Processor Implementation
- [x] Embedding Engine Implementation
- [x] Vector Store Implementation (Numpy Fallback)
- [x] Indexing Orchestrator Implementation
- [x] Run Indexing and Verify Results
