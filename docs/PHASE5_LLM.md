# Phase 5: LLM Generation & Response Validation

## Overview
Phase 5 integrates Groq API to generate factual responses based on retrieved context, with strict validation constraints.

**Status:** 📋 Planned  
**Implementation Date:** TBD

---

## Objectives

1. Integrate Groq API (Llama 3.3 70B)
2. Design facts-only system prompt
3. Generate responses from retrieved context
4. Validate response constraints (max 3 sentences, 1 citation)
5. Add source links and last updated date

---

## Implementation Plan

### 1. LLM Generator
**File:** `src/llm_generator.py`

**System Prompt:**
```
You are a facts-only mutual fund FAQ assistant.
Rules:
1. Answer ONLY using provided context
2. Maximum 3 sentences
3. Include EXACTLY ONE source citation
4. Add footer: "Last updated from sources: <date>"
5. NEVER provide investment advice
```

### 2. Response Validator
**File:** `src/response_validator.py`

**Validation Checks:**
- Sentence count ≤ 3
- Exactly 1 URL citation
- No advisory language
- Proper footer format

### 3. Output Format

```
The HDFC Mid-Cap Fund has an expense ratio of 0.55% for the Direct Plan 
(as of April 2026).

Source: https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth

Last updated from sources: 2026-04-25
```

---

## How to Run

```bash
cd src
python llm_generator.py
```

---

## Files to Create

- `src/llm_generator.py`
- `src/response_validator.py`
- `tests/test_llm_generation.py`

---

## Success Criteria

- ✅ Responses ≤ 3 sentences
- ✅ Exactly 1 citation link
- ✅ Proper footer included
- ✅ No advisory content
- ✅ Facts-only responses
- ✅ Fast generation (<2s)

---

**Phase 5 Status:** 📋 Not Started  
**Previous Phase:** Phase 4 - Retrieval Engine  
**Next Phase:** Phase 6 - Refusal Handler
