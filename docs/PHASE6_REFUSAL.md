# Phase 6: Refusal Handler

## Overview
Phase 6 implements detection and handling of advisory/non-factual queries that violate the facts-only constraint.

**Status:** 📋 Planned  
**Implementation Date:** TBD

---

## Objectives

1. Detect advisory queries (e.g., "Should I invest?")
2. Return polite refusal messages
3. Provide educational resource links
4. Reinforce facts-only limitation

---

## Implementation Plan

### 1. Refusal Handler
**File:** `src/refusal_handler.py`

**Advisory Query Patterns:**
- "Should I invest in..."
- "Which fund is better..."
- "Is this a good fund..."
- "Recommend me..."
- "Best fund for..."

**Refusal Response Template:**
```
I can't provide investment advice or recommendations. My role is to 
share only factual, publicly available information about mutual fund 
schemes.

For investment guidance, you may consult a SEBI-registered financial 
advisor or visit AMFI's investor education page: 
https://www.amfiindia.com/investor-awareness

Facts-only. No investment advice.
```

### 2. Detection Methods
- Keyword matching
- Pattern recognition
- Intent classification
- LLM-based classification (optional)

---

## How to Run

```bash
cd src
python refusal_handler.py
```

---

## Files to Create

- `src/refusal_handler.py`
- `tests/test_refusal_handling.py`

---

## Success Criteria

- ✅ 100% advisory query detection
- ✅ Polite refusal messages
- ✅ Educational links provided
- ✅ Clear facts-only reinforcement
- ✅ No false positives on factual queries

---

**Phase 6 Status:** 📋 Not Started  
**Previous Phase:** Phase 5 - LLM Generation  
**Next Phase:** Phase 7 - Streamlit UI
