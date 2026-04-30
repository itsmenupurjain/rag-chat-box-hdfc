# RAG Architecture: Mutual Fund FAQ Assistant

## Project Overview

A facts-only Retrieval-Augmented Generation (RAG) based FAQ assistant for mutual fund schemes, using Groww as the reference product context. The system answers objective, verifiable queries by retrieving information exclusively from official public sources (AMC, AMFI, SEBI).

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE                              │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Welcome Message + Disclaimer: "Facts-only. No investment    │  │
│  │  advice." + 3 Example Questions + Chat Input Box             │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    QUERY PROCESSING LAYER                           │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  1. Query Classification                                      │  │
│  │     • Factual Query → Proceed to RAG pipeline                 │  │
│  │     • Advisory Query → Trigger Refusal Handler                │  │
│  │                                                               │  │
│  │  2. Query Preprocessing                                       │  │
│  │     • Intent extraction                                       │  │
│  │     • Entity recognition (scheme name, AMC, metric type)      │  │
│  │     • Query normalization                                     │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
┌──────────────────────────┐    ┌──────────────────────────┐
│   RAG PIPELINE           │    │   REFUSAL HANDLER        │
│   (Factual Queries)      │    │   (Advisory Queries)     │
│                          │    │                          │
│  ┌────────────────────┐  │    │  • Detect: "Should I     │  │
│  │ Document Ingestion │  │    │    invest?", "Which is   │  │
│  │ & Chunking         │  │    │    better?"              │  │
│  └────────────────────┘  │    │  • Return polite refusal │  │
│            │             │    │  • Include educational   │  │
│            ▼             │    │    link (AMFI/SEBI)      │  │
│  ┌────────────────────┐  │    └──────────────────────────┘
│  │ Vector Embeddings  │  │
│  │ & Indexing         │  │
│  └────────────────────┘  │
│            │             │
│            ▼             │
│  ┌────────────────────┐  │
│  │ Similarity Search  │  │
│  │ (Top-K Retrieval)  │  │
│  └────────────────────┘  │
│            │             │
│            ▼             │
│  ┌────────────────────┐  │
│  │ Context Assembly   │  │
│  │ & Source Tracking  │  │
│  └────────────────────┘  │
│            │             │
│            ▼             │
│  ┌────────────────────┐  │
│  │ LLM Generation     │  │
│  │ (Facts-Only Mode)  │  │
│  └────────────────────┘  │
│            │             │
│            ▼             │
│  ┌────────────────────┐  │
│  │ Response Validation│  │
│  │ & Formatting       │  │
│  └────────────────────┘  │
└──────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    RESPONSE DELIVERY                                 │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  • Max 3 sentences                                            │  │
│  │  • Exactly 1 citation link                                    │  │
│  │  • Footer: "Last updated from sources: <date>"                │  │
│  │  • Multi-thread support                                       │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## System Architecture Components

### Phase 1: Data Corpus Definition & Collection

#### 1.1 AMC Selection
**Selected AMC:** HDFC Mutual Fund

**Platform:** Groww (Reference Product Context)

**Selected Schemes (5 with category diversity):**
1. **HDFC Mid-Cap Fund (Direct-Growth)** - Mid Cap
   - URL: https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth
   
2. **HDFC Equity Fund (Direct-Growth)** - Large Cap
   - URL: https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth
   
3. **HDFC Focused Fund (Direct-Growth)** - Focused Fund
   - URL: https://groww.in/mutual-funds/hdfc-focused-fund-direct-growth
   
4. **HDFC ELSS Tax Saver Fund (Direct-Plan-Growth)** - ELSS (Tax Saving)
   - URL: https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth
   
5. **HDFC Large Cap Fund (Direct-Growth)** - Large Cap
   - URL: https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth

#### 1.2 Official Document Sources (Web Pages Only)

**Data Source:** Groww Mutual Fund Pages

**URLs to Scrape (5 Primary URLs):**
1. https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth
2. https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth
3. https://groww.in/mutual-funds/hdfc-focused-fund-direct-growth
4. https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth
5. https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth

**Additional Reference URLs (10-15 from AMFI/SEBI/AMC):**
- AMFI investor education: https://www.amfiindia.com/investor-awareness
- SEBI guidelines: https://www.sebi.gov.in/investor.html
- HDFC AMC official: https://www.hdfcfund.com/
- HDFC AMC factsheets (official source for verification)
- HDFC AMC scheme information documents

**Total Expected URLs:** 15-20 official sources

**Note:** All data will be scraped from web pages (HTML). No PDFs will be used or shared.

---

### Phase 2: Document Processing Pipeline

#### 2.1 Document Ingestion

```python
Document Ingestion Flow (Web Pages Only):
┌──────────────┐
│ Web Scraping │ → Fetch HTML content from Groww URLs
│ (HTML Only)  │ → Use requests + BeautifulSoup
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ HTML Parsing     │ → Extract relevant sections:
│                  │   • Scheme details
│                  │   • Expense ratio
│                  │   • Exit load
│                  │   • Minimum SIP/Lumpsum
│                  │   • Riskometer
│                  │   • Fund manager info
│                  │   • Performance data (factual only)
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Data Cleaning    │ → Remove:
│                  │   • Navigation elements
│                  │   • Ads/promotional content
│                  │   • Irrelevant UI components
│                  │   • Scripts and styles
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│ Metadata Tagging │ → Scheme name, fund category, 
│                  │   AMC, scrape date, source URL
└──────────────────┘
```

**Technologies:**
- **Web Scraping:** requests, BeautifulSoup4, or Playwright (if JavaScript rendering needed)
- **HTML Processing:** BeautifulSoup4, lxml
- **Data Extraction:** Regular expressions for structured data

**Note:** No PDF processing required. All data comes from web pages only.

#### 2.2 Text Chunking Strategy

**Chunking Approach:** Hybrid Semantic + Fixed-size

```
Chunking Parameters:
├── Chunk Size: 500-800 tokens
├── Overlap: 50-100 tokens
├── Strategy: 
│   ├── Respect document structure (headings, sections)
│   ├── Split on logical boundaries (paragraphs, tables)
│   └── Maintain context continuity
└── Metadata per chunk:
    ├── Source URL
    ├── Document type (factsheet/KIM/SID/FAQ)
    ├── Scheme name
    ├── Publication date
    └── Section heading
```

**Example Chunk Structure:**
```json
{
  "chunk_id": "hdfc_top100_factsheet_2024_001",
  "content": "HDFC Top 100 Fund - Expense Ratio: Direct Plan - 0.55%, Regular Plan - 1.75%...",
  "metadata": {
    "source_url": "https://www.hdfcfund.com/factsheet/top100",
    "scheme": "HDFC Top 100 Fund",
    "document_type": "factsheet",
    "amc": "HDFC Mutual Fund",
    "category": "Large Cap",
    "publication_date": "2024-01-15",
    "section": "Fund Details"
  }
}
```

---

### Phase 3: Vector Database & Embeddings

#### 3.1 Embedding Model Selection

**Recommended Model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Dimensions:** 384
- **Speed:** Fast inference
- **Quality:** Good for factual retrieval
- **Size:** ~80MB (lightweight)

**Alternative:** OpenAI `text-embedding-ada-002` (if budget allows)

#### 3.2 Vector Database Options

**Option 1: FAISS (Recommended for MVP)**
```
Pros:
├── Free and open-source
├── Fast similarity search
├── Easy integration with Python
└── Suitable for 15-25 documents (~500-1000 chunks)

Cons:
├── In-memory (no persistence without saving)
└── Limited advanced features
```

**Option 2: ChromaDB**
```
Pros:
├── Built-in persistence
├── Metadata filtering
├── Easy API
└── Good for small-medium datasets
```

**Option 3: Pinecone** (Cloud-based, if scaling needed)

#### 3.3 Indexing Pipeline

```python
Indexing Flow:
┌─────────────────┐
│ Text Chunks     │
│ (from Phase 2)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Embedding Model │ → Convert text to vectors
│ (MiniLM-L6-v2)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Vector Database │ → Store vectors + metadata
│ (FAISS/Chroma)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Index Ready for │ → Optimized for retrieval
│ Retrieval       │
└─────────────────┘
```

---

### Phase 4: Retrieval Engine

#### 4.1 Query Processing

```python
Query Processing Steps:
1. Query Normalization
   ├── Lowercase conversion
   ├── Remove special characters
   └── Handle abbreviations (SIP, ELSS, AMC)

2. Intent Classification
   ├── Factual query types:
   │   ├── Expense ratio query
   │   ├── Exit load query
   │   ├── Minimum investment query
   │   ├── Lock-in period query
   │   ├── Riskometer query
   │   ├── Benchmark query
   │   └── Process/how-to query
   └── Advisory query types:
       ├── Recommendation request
       ├── Comparison request
       └── Performance prediction

3. Entity Extraction
   ├── Scheme name detection
   ├── AMC detection
   └── Metric type identification
```

#### 4.2 Similarity Search

**Search Strategy:** Hybrid Search

```
Retrieval Process:
┌───────────────────────┐
│ User Query            │
│ "What is the expense  │
│  ratio of HDFC        │
│  Top 100 Fund?"       │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Query Embedding       │ → Convert query to vector
│ (same model as docs)  │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Vector Similarity     │ → Cosine similarity search
│ Search (Top-K=5)      │ → Retrieve top 5 chunks
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Metadata Filtering    │ → Optional: filter by scheme,
│                       │   document type, date
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Re-ranking (Optional) │ → Cross-encoder for better
│                       │   relevance scoring
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Top-3 Relevant Chunks │ → Final context for LLM
│ with Source URLs      │
└───────────────────────┘
```

**Similarity Metric:** Cosine Similarity

**Top-K Retrieval:** 
- Retrieve: 5 chunks
- Use top: 3 for context (to stay within token limits)

---

### Phase 5: LLM Generation Layer

#### 5.1 LLM Model Selection

**Option 1: Groq + Llama 3.3 70B (Recommended)**
```
Pros:
├── Fast inference (Groq's LPU)
├── Free tier available
├── Good instruction following
└── Strong factual accuracy
```

**Option 2: OpenAI GPT-4o-mini**
```
Pros:
├── Excellent instruction following
├── Good at formatting
└── Reliable API
Cons:
└── Costs money
```

#### 5.2 Prompt Engineering

**System Prompt:**
```
You are a facts-only mutual fund FAQ assistant. Your role is to provide 
accurate, verifiable information about mutual fund schemes using ONLY 
the provided context from official sources (AMC, AMFI, SEBI).

RULES:
1. Answer ONLY using information from the provided context
2. Maximum 3 sentences per response
3. Include EXACTLY ONE source citation link from the context
4. Add footer: "Last updated from sources: <date from metadata>"
5. NEVER provide investment advice, recommendations, or opinions
6. NEVER compare schemes or predict performance
7. If information is not in context, say so clearly
8. For performance queries, provide link to factsheet only
9. Be concise, factual, and precise
```

**User Prompt Template:**
```
Context from official sources:
{retrieved_chunks_with_metadata}

User Query: {user_query}

Provide a factual response following all rules.
```

**Example Interaction:**
```
Query: "What is the expense ratio of HDFC Top 100 Fund?"

Response: 
The HDFC Top 100 Fund has an expense ratio of 0.55% for the Direct Plan 
and 1.75% for the Regular Plan (as of January 2024). 

Source: https://www.hdfcfund.com/factsheet/top100

Last updated from sources: 2024-01-15
```

#### 5.3 Response Constraints Enforcement

```python
Response Validation Pipeline:
┌─────────────────────┐
│ LLM Raw Output      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Length Check        │ → Max 3 sentences
│                     │ → Split and count
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Citation Check      │ → Exactly 1 URL
│                     │ → Validate URL format
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Advisory Check      │ → No "should", "recommend",
│                     │   "better" language
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Footer Addition     │ → Append last updated date
│                     │   from metadata
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Final Response      │ → Send to user
└─────────────────────┘
```

---

### Phase 6: Refusal Handler

#### 6.1 Advisory Query Detection

**Detection Rules:**
```python
Advisory Query Patterns:
├── "Should I invest in..."
├── "Which fund is better..."
├── "Is this a good fund..."
├── "Recommend me..."
├── "Best fund for..."
├── Performance prediction requests
└── Comparative analysis requests

Keyword Triggers:
├── "should", "better", "best", "recommend"
├── "good investment", "worth investing"
├── "compare", "versus", "vs"
└── "predict", "future returns"
```

#### 6.2 Refusal Response Template

```
Refusal Response Structure:

"I can't provide investment advice or recommendations. My role is to 
share only factual, publicly available information about mutual fund 
schemes. 

For investment guidance, you may consult a SEBI-registered financial 
advisor or visit AMFI's investor education page: 
https://www.amfiindia.com/investor-awareness

Facts-only. No investment advice."
```

---

### Phase 7: User Interface

#### 7.1 UI Components (Streamlit)

```
┌─────────────────────────────────────────────────────┐
│  🏦 Mutual Fund FAQ Assistant                       │
│  ─────────────────────────────────────────────────  │
│  ⚠️ Facts-only. No investment advice.               │
│  ─────────────────────────────────────────────────  │
│                                                     │
│  💡 Try these example questions:                    │
│  • What is the expense ratio of HDFC Top 100 Fund?  │
│  • What is the minimum SIP amount for HDFC ELSS?    │
│  • What is the exit load for HDFC Flexi Cap Fund?   │
│                                                     │
│  ┌───────────────────────────────────────────────┐ │
│  │ Type your question here...                    │ │
│  └───────────────────────────────────────────────┘ │
│                                                     │
│  [ Ask Question ]                                   │
│                                                     │
│  ─────────────────────────────────────────────────  │
│  💬 Chat History (Multi-thread support)             │
│  ─────────────────────────────────────────────────  │
│                                                     │
│  [ New Chat ]  [ Chat 1 ]  [ Chat 2 ]              │
│                                                     │
└─────────────────────────────────────────────────────┘
```

#### 7.2 Multi-Thread Chat Support

```python
Thread Management:
├── Each chat session has unique ID
├── Maintain separate conversation history
├── Store in session state or lightweight DB
└── Allow switching between threads

Session State Structure:
{
  "active_thread_id": "thread_001",
  "threads": {
    "thread_001": {
      "created_at": "2024-01-20 10:00:00",
      "messages": [
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."}
      ]
    },
    "thread_002": {
      ...
    }
  }
}
```

---

## Data Flow Architecture

### End-to-End Query Flow

```
1. User Query Input
       ↓
2. Query Classification (Factual vs Advisory)
       ↓
   ┌───┴───┐
   │       │
Advisory  Factual
   │       │
   ↓       ↓
Refusal  Query Preprocessing
Handler  (normalize, extract entities)
   │       │
   │       ↓
   │    Convert to Embedding
   │       │
   │       ↓
   │    Vector Similarity Search
   │       │
   │       ↓
   │    Retrieve Top-5 Chunks
   │       │
   │       ↓
   │    Assemble Context + Sources
   │       │
   │       ↓
   │    LLM Generation (Facts-Only)
   │       │
   │       ↓
   │    Response Validation
   │       │
   │       ↓
   │    Format Output
   │       │
   └───┬───┘
       │
       ↓
3. Display Response with Citation + Footer
```

---

## Data Freshness & Automation

### 1. Scheduled Scraping
To ensure the assistant provides the most current NAV and fund metrics, the system follows a 9:30 AM IST daily refresh schedule.

**Automation Strategy:**
- **Local:** Windows Task Scheduler triggers `src/scheduler.py` daily.
- **Cloud:** GitHub Actions cron job (`30 4 * * *`) runs the ingestion and indexing pipeline.

### 2. Hybrid Refresh Approach
- **Automated:** Background scheduler runs at 9:30 AM daily.
- **Manual:** Streamlit UI provides a "Refresh Database" button in the sidebar for on-demand updates.

### 3. Pipeline Flow (Refresh)
1. **Scrape**: Fetch fresh HTML from Groww.
2. **Parse**: Extract metrics into structured JSON.
3. **Index**: Regenerate embeddings and update Vector Store.
4. **Notify**: UI reflects "Last Updated" timestamp.

---

## Technology Stack

### Core Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.10+ | Core development |
| **Web Framework** | Streamlit | UI/Chat interface |
| **LLM API** | Groq (Llama 3.3 70B) | Response generation |
| **Embeddings** | sentence-transformers | Text vectorization |
| **Vector DB** | FAISS / ChromaDB | Similarity search |
| **Web Scraping** | BeautifulSoup, PyPDF2 | Document ingestion |
| **Data Processing** | Pandas, NumPy | Data manipulation |
| **Environment** | python-dotenv | API key management |

### Dependencies (requirements.txt)

```txt
streamlit>=1.28.0
groq>=0.4.0
sentence-transformers>=2.2.0
faiss-cpu>=1.7.4  # or chromadb>=0.4.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
requests>=2.31.0
pandas>=2.0.0
numpy>=1.24.0
python-dotenv>=1.0.0
```

**Note:** No PDF libraries (PyPDF2, pdfplumber) needed since we're only processing web pages.

---

## Project Directory Structure

```
mutual-fund-faq-assistant/
│
├── docs/
│   ├── ARCHITECTURE.md              # This file
│   ├── API_REFERENCE.md
│   └── USER_GUIDE.md
│
├── data/
│   ├── raw/                         # Downloaded HTML files from Groww
│   │   ├── hdfc_mid_cap_fund.html
│   │   ├── hdfc_equity_fund.html
│   │   ├── hdfc_focused_fund.html
│   │   ├── hdfc_elss_tax_saver.html
│   │   └── hdfc_large_cap_fund.html
│   ├── processed/                   # Extracted and cleaned text
│   ├── vectors/                     # FAISS/Chroma indexes
│   └── metadata.json                # Document metadata & URLs
│
├── src/
│   ├── __init__.py
│   ├── data_ingestion.py            # Web scraping from Groww URLs
│   ├── html_parser.py               # HTML extraction & cleaning
│   ├── document_processor.py        # Chunking & text processing
│   ├── embedding_engine.py          # Vector embeddings
│   ├── vector_store.py              # FAISS/Chroma management
│   ├── retrieval_engine.py          # Similarity search
│   ├── llm_generator.py             # LLM prompt & generation
│   ├── response_validator.py        # Constraint checking
│   ├── refusal_handler.py           # Advisory query detection
│   └── app.py                       # Streamlit UI
│
├── tests/
│   ├── test_data_ingestion.py
│   ├── test_html_parsing.py
│   ├── test_retrieval.py
│   ├── test_llm_generation.py
│   ├── test_refusal_handling.py
│   └── test_response_validation.py
│
├── configs/
│   ├── groww_urls.json              # Groww mutual fund URLs
│   ├── schemes.json                 # Selected HDFC schemes
│   └── prompts.json                 # LLM prompt templates
│
├── logs/
│   ├── ingestion.log
│   ├── retrieval.log
│   └── app.log
│
├── .env                             # GROQ_API_KEY
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Security & Compliance

### Data Privacy
```
✅ DO NOT collect/store:
   ├── PAN numbers
   ├── Aadhaar numbers
   ├── Account numbers
   ├── OTPs
   ├── Email addresses
   └── Phone numbers

✅ Data stored locally only:
   ├── Public documents (PDFs/HTML)
   ├── Vector embeddings
   └── Chat session metadata (no PII)
```

### Content Restrictions
```
❌ NEVER provide:
   ├── Investment advice
   ├── Recommendations
   ├── Performance comparisons
   ├── Return calculations
   ├── Speculative content

✅ ONLY provide:
   ├── Factual data from official sources
   ├── Single citation link per response
   ├── Last updated date
   ├── Educational links for refusals
```

---

## Performance Optimization

### Caching Strategy
```python
@st.cache_resource
def load_vector_store():
    """Load FAISS index once at startup"""
    pass

@st.cache_data
def get_document_chunks():
    """Cache processed chunks"""
    pass
```

### Latency Targets
- **Query Processing:** < 100ms
- **Vector Search:** < 200ms
- **LLM Generation:** < 2s (Groq)
- **Total Response Time:** < 3s

---

## Known Limitations

1. **Web Scraping Dependencies:**
   - Groww website structure may change, requiring parser updates
   - Mitigation: Regular validation and flexible parsing logic

2. **JavaScript-Rendered Content:**
   - Some data may be loaded dynamically via JavaScript
   - Mitigation: Use Playwright or Selenium if BeautifulSoup fails

3. **Data Freshness:** 
   - NAV and performance data change daily
   - Mitigation: Re-scrape weekly; show last updated date

4. **Rate Limiting:**
   - Groww may have anti-scraping measures
   - Mitigation: Respect robots.txt, add delays, cache locally

5. **Query Understanding:**
   - May struggle with highly specific or multi-part queries
   - Mitigation: Clear example queries and error messages

6. **Source Coverage:**
   - Limited to 5 HDFC schemes from Groww
   - Mitigation: Expandable architecture for more AMCs/schemes

7. **No Real-time Data:**
   - Live NAV requires API calls to AMC
   - Mitigation: Link to official sources for real-time data

---

## Deployment Options

### Option 1: Local Deployment (Recommended for MVP)
```bash
# Run locally
streamlit run src/app.py
```

### Option 2: Streamlit Cloud (Free)
```bash
# Deploy to Streamlit Community Cloud
# Push to GitHub → Connect to Streamlit Cloud
```

### Option 3: Docker Container
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "src/app.py"]
```

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Factual Accuracy | > 95% |
| Response Time | < 3 seconds |
| Citation Inclusion | 100% |
| Advisory Query Refusal | 100% |
| User Satisfaction | > 4/5 rating |
| Response Length Compliance | ≤ 3 sentences |

---

## Future Enhancements

1. **Multi-AMC Support:** Expand to 5-10 AMCs
2. **Automated Re-indexing:** Scheduled updates from official sources
3. **Advanced Query Types:** Support for complex multi-fact queries
4. **Mobile App:** React Native or Flutter wrapper
5. **Analytics Dashboard:** Track query patterns and user behavior
6. **Multilingual Support:** Hindi + English
7. **Voice Interface:** Speech-to-text for queries

---

## Conclusion

This RAG architecture ensures a **trustworthy, transparent, and compliant** mutual fund FAQ assistant that prioritizes **accuracy over intelligence**. The system delivers only verified, source-backed financial information without advisory bias, meeting all regulatory and compliance requirements.

**Key Strengths:**
- ✅ Facts-only responses with citations
- ✅ Strict refusal of advisory queries
- ✅ Multi-thread chat support
- ✅ Lightweight and deployable
- ✅ Scalable architecture for future expansion
