# Lab 2.9: Multi-Agent Architecture

**Duration:** 60 minutes
**Level:** 2

## Objectives

Complete this lab to demonstrate your understanding of the concepts covered.

## Prerequisites

- Completed previous labs
- Python 3.10+ with signalwire-agents installed
- Virtual environment activated

## Instructions

### 1. Set Up Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Implement Your Solution

Edit `solution/agent.py` according to the lab requirements.

### 3. Test Locally

```bash
# List available functions
swaig-test solution/agent.py --list-tools

# Check SWML output
swaig-test solution/agent.py --dump-swml
```

### 4. Submit

```bash
git add solution/agent.py
git commit -m "Complete Lab 2.9: Multi-Agent Architecture"
git push
```

## Grading

| Check | Points |
|-------|--------|
| GeneralAgent Loads | 15 |
| GeneralAgent SWML | 10 |
| GeneralAgent has routing | 10 |
| SalesAgent Loads | 15 |
| SalesAgent SWML | 10 |
| SalesAgent has pricing | 10 |
| SupportAgent Loads | 15 |
| SupportAgent SWML | 10 |
| SupportAgent has tickets | 5 |
| **Total** | **100** |

**Passing Score:** 70%

## Reference

See `reference/starter.py` for a boilerplate template.

---

## Next Assignment

Ready to continue? [**Start Lab 2.10: Production Deployment**](https://classroom.github.com/a/t0Aqma1B)

---

*SignalWire AI Agents Certification*
