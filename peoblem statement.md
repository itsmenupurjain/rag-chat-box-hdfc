# Problem Statement

## Mutual Fund FAQ Assistant — RAG-Based Chatbot for HDFC Mutual Fund Schemes

---

## 1. Background

Retail investors in India increasingly rely on digital platforms like **Groww** to research and invest in mutual funds. However, navigating scheme-specific details — such as fund category, risk level, past returns, expense ratio, exit load, and benchmark index — across multiple pages is time-consuming and often confusing for new investors.

At the same time, existing customer support channels (call centres, email) are slow and do not scale. Generic AI chatbots risk providing **investment advice**, which is regulated by SEBI and can expose platforms to legal liability.

There is a clear need for a **facts-only, AI-powered FAQ assistant** that can instantly answer factual questions about mutual fund schemes while strictly refusing to give any form of investment recommendation.

---

## 2. Problem Definition

> **How can we build an intelligent FAQ chatbot that provides accurate, cited, factual answers about HDFC Mutual Fund schemes listed on Groww — without ever crossing the line into investment advice?**

### Key Challenges

| # | Challenge | Description |
|---|-----------|-------------|
| 1 | **Information Scatter** | Scheme details are spread across multiple Groww web pages; users must manually browse each one |
| 2 | **Accuracy & Hallucination Risk** | LLMs can generate plausible but incorrect financial data if not grounded in source documents |
| 3 | **Regulatory Compliance** | SEBI regulations prohibit unregistered entities from giving investment advice; the bot must refuse advisory queries |
| 4 | **Citation & Trust** | Users need to verify answers; every response must include a source link |
| 5 | **Brevity** | Users want quick answers, not lengthy paragraphs — responses must be concise (≤ 3 sentences) |

---

## 3. Objectives

1. **Build a RAG (Retrieval-Augmented Generation) chatbot** that answers factual questions about 5 selected HDFC Mutual Fund schemes using data scraped from Groww.
2. **Ensure factual grounding** — every answer must be derived from the ingested HTML data, not from the LLM's general knowledge.
3. **Enforce strict response rules:**
   - Maximum **3 sentences** per response
   - Exactly **1 citation link** per answer
   - A **"Last Updated"** date footer on every response
4. **Refuse advisory queries** — if a user asks "Should I invest in X?" or similar, the bot must politely decline and explain it only provides factual information.
5. **Deliver a clean, user-friendly Streamlit UI** with multi-thread chat support.

---

## 4. Scope

### In Scope

- **5 HDFC Mutual Fund schemes** (Direct-Growth plans):
  1. HDFC Mid-Cap Fund
  2. HDFC Equity Fund
  3. HDFC Focused Fund
  4. HDFC ELSS Tax Saver Fund
  5. HDFC Large Cap Fund

- **Data source:** Groww website HTML pages only (no PDFs)
- **Reference sources:** AMFI, SEBI, HDFC AMC (for verification)
- **LLM provider:** Groq (Llama 3.3 70B Versatile)
- **Vector store:** FAISS
- **Embeddings:** Sentence Transformers
- **Frontend:** Streamlit

### Out of Scope

- Schemes from other AMCs (e.g., ICICI, SBI, Axis)
- PDF document parsing
- Real-time NAV or live market data
- Portfolio tracking or transaction features
- Investment advice or recommendations of any kind
- Mobile app development

---

## 5. Constraints

| Constraint | Detail |
|------------|--------|
| **No investment advice** | The system must never recommend buying, selling, or holding any scheme |
| **HTML-only data** | Only Groww web pages are used; no PDFs or third-party APIs for fund data |
| **Response length** | Maximum 3 sentences per answer |
| **Citation requirement** | Exactly 1 source link per response |
| **API rate limit** | Groq free tier allows 30 requests/minute |
| **Facts-only** | Responses must be objectively verifiable from the source data |

---

## 6. Proposed Solution — RAG Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   User asks  │────▶│  Retrieval   │────▶│  Generation  │
│   question   │     │  (FAISS +    │     │  (Groq LLM + │
│  (Streamlit) │     │  Embeddings) │     │  Prompt Eng.) │
└──────────────┘     └──────────────┘     └──────────────┘
                            │                     │
                     ┌──────▼──────┐       ┌──────▼──────┐
                     │  Ingested   │       │  Validated  │
                     │  HTML Data  │       │  Response   │
                     │  (Chunked)  │       │  (≤3 lines) │
                     └─────────────┘       └─────────────┘
```

### How It Works

1. **Data Ingestion** — Scrape HTML pages from Groww for the 5 selected schemes
2. **Document Processing** — Parse, clean, and chunk the HTML into meaningful text segments
3. **Vector Embeddings** — Convert chunks into vector representations using Sentence Transformers
4. **Retrieval** — For each user query, retrieve the top-k most relevant chunks via FAISS similarity search
5. **LLM Generation** — Pass retrieved chunks + user query to Groq (Llama 3.3 70B) with a strict prompt template
6. **Validation** — Enforce response rules (≤ 3 sentences, 1 citation, no advice)
7. **Refusal Handling** — Detect and refuse advisory/opinion queries before they reach the LLM

---

## 7. Success Metrics

| Metric | Target |
|--------|--------|
| **Factual Accuracy** | ≥ 95% of answers are verifiable from source data |
| **Response Compliance** | 100% of responses follow the 3-sentence + 1-citation rule |
| **Advisory Refusal Rate** | 100% of advisory queries are correctly refused |
| **Response Latency** | < 5 seconds per query |
| **User Satisfaction** | Positive feedback on clarity and usefulness |

---

## 8. Phased Delivery Plan

| Phase | Deliverable | Status |
|-------|-------------|--------|
| **Phase 1** | Project Setup & Data Corpus Definition | ✅ Complete |
| **Phase 2** | Data Ingestion & HTML Parsing | 🚧 In Progress |
| **Phase 3** | Vector Database & Embeddings | 📋 Planned |
| **Phase 4** | Retrieval Engine | 📋 Planned |
| **Phase 5** | LLM Generation & Validation | 📋 Planned |
| **Phase 6** | Refusal Handler | 📋 Planned |
| **Phase 7** | Streamlit UI & Multi-Thread Chat | 📋 Planned |

---

## 9. Tech Stack

| Component | Technology |
|-----------|------------|
| **Language** | Python 3.10+ |
| **LLM** | Groq — Llama 3.3 70B Versatile |
| **Embeddings** | Sentence Transformers |
| **Vector Store** | FAISS |
| **Web Scraping** | BeautifulSoup4 + lxml |
| **Frontend** | Streamlit |
| **Data Handling** | Pandas, NumPy |
| **Config** | python-dotenv, JSON configs |

---

## 10. Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Groww blocks scraping | Data ingestion fails | Use cached HTML, respect robots.txt, add retries |
| LLM hallucination | Incorrect financial data shown to users | RAG grounding + strict prompt constraints + validation layer |
| API rate limiting | Slow or failed responses | Queue requests, cache frequent answers, respect 30 req/min limit |
| Regulatory non-compliance | Legal exposure | Hard-coded refusal handler for advisory queries; no advice under any prompt |
| Stale data | Outdated scheme details | Display "Last Updated" date; plan periodic re-ingestion |

---

**Author:** Nupur Jain  
**Last Updated:** September 2, 2026  
**Project Repository:** [rag-chat-box-hdfc](https://github.com/itsmenupurjain/rag-chat-box-hdfc)
