⚠️ Note: This project uses simulated NHS-style data only and does not access, store, or process real patient or hospital data.

## How to Run

1. Clone the repository
2. Install Python 3.10+
3. Run:
   python core/run_cycle.py
4. Follow the prompt for human approval

## Architecture Overview

NHS-Flow is implemented as an explicit state machine using LangGraph.
Each node represents a single responsibility: ward analysis, logistics planning, compliance validation, and human approval.

The system prioritizes correctness, governance, and auditability over automation, reflecting the constraints of real healthcare environments.

All decisions are persisted in an append-only audit log to support traceability and post-hoc analysis.

## Limitations

- Uses simulated NHS-style data only
- Rule-based prediction logic (no ML yet)
- Single supplier selection strategy
- Console-based human approval

These limitations are intentional to validate system correctness
before scaling complexity.
