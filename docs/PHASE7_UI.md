# Phase 7: Streamlit UI with Multi-thread Support

## Overview
Phase 7 builds the user interface using Streamlit with multi-thread chat support, example questions, and visible disclaimers.

**Status:** 📋 Planned  
**Implementation Date:** TBD

---

## Objectives

1. Create Streamlit web interface
2. Implement multi-thread chat support
3. Add welcome message and disclaimer
4. Provide 3 example questions
5. Display responses with citations

---

## Implementation Plan

### 1. Main Application
**File:** `src/app.py`

**UI Components:**
- Welcome message
- Disclaimer: "Facts-only. No investment advice."
- 3 example questions
- Chat input box
- Chat history display
- Multi-thread navigation

### 2. Multi-thread Support

**Session State Structure:**
```python
{
  "active_thread_id": "thread_001",
  "threads": {
    "thread_001": {
      "created_at": "2026-04-25 10:00:00",
      "messages": [
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."}
      ]
    }
  }
}
```

### 3. UI Layout

```
┌─────────────────────────────────────────────┐
│  🏦 Mutual Fund FAQ Assistant               │
│  ─────────────────────────────────────────  │
│  ⚠️ Facts-only. No investment advice.       │
│  ─────────────────────────────────────────  │
│                                             │
│  💡 Try these example questions:            │
│  • What is the expense ratio of...?         │
│  • What is the minimum SIP amount...?       │
│  • What is the exit load for...?            │
│                                             │
│  ┌───────────────────────────────────────┐ │
│  │ Type your question here...            │ │
│  └───────────────────────────────────────┘ │
│                                             │
│  [ Ask Question ]                           │
│                                             │
│  ─────────────────────────────────────────  │
│  💬 Chat History                            │
│  ─────────────────────────────────────────  │
│                                             │
│  [ New Chat ]  [ Chat 1 ]  [ Chat 2 ]      │
│                                             │
└─────────────────────────────────────────────┘
```

---

## How to Run

```bash
cd src
streamlit run app.py
```

---

## Files to Create

- `src/app.py`
- `tests/test_ui.py` (optional)

---

## Success Criteria

- ✅ Clean, minimal interface
- ✅ Multi-thread chat working
- ✅ Disclaimer visible
- ✅ Example questions clickable
- ✅ Responses display correctly
- ✅ Citations and footer shown
- ✅ Fast response time (<3s)

---

**Phase 7 Status:** 📋 Not Started  
**Previous Phase:** Phase 6 - Refusal Handler  
**Next Phase:** Testing & Integration
