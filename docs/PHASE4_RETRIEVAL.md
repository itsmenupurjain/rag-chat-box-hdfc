# Phase 4: Retrieval Engine

## Overview
Phase 4 implements the similarity search mechanism to retrieve relevant document chunks based on user queries.

**Status:** 📋 Planned  
**Implementation Date:** TBD

---

## Objectives

1. Convert user query to embedding
2. Search vector database for similar chunks
3. Retrieve top-K most relevant results
4. Return context with source metadata

---

## Implementation Plan

### 1. Retrieval Engine
**File:** `src/retrieval_engine.py`

**Search Strategy:**
- Cosine similarity
- Top-K retrieval (K=5)
- Optional metadata filtering
- Optional re-ranking with cross-encoder

### 2. Query Processing
- Normalize query text
- Convert to embedding (same model as documents)
- Search vector index
- Return top matches with scores

### 3. Output Format

```json
{
  "query": "What is the expense ratio of HDFC Mid-Cap Fund?",
  "results": [
    {
      "chunk_id": "hdfc_midcap_001",
      "content": "...",
      "similarity_score": 0.92,
      "metadata": {
        "scheme": "HDFC Mid-Cap Fund",
        "source_url": "...",
        "section": "Fund Details"
      }
    }
  ]
}
```

---

## How to Run

```bash
cd src
python retrieval_engine.py
```

---

## Files to Create

- `src/retrieval_engine.py`
- `tests/test_retrieval.py`

---

## Success Criteria

- ✅ Fast query response (<200ms)
- ✅ Relevant results returned
- ✅ Proper similarity scoring
- ✅ Source URLs included
- ✅ Metadata filtering works

---

**Phase 4 Status:** 📋 Not Started  
**Previous Phase:** Phase 3 - Vector Database & Embeddings  
**Next Phase:** Phase 5 - LLM Generation
