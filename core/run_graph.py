import json
from datetime import datetime
from graph import graph
import os

initial_state = {
    "ward": json.load(open(r"data\ward_state.json")),
    "supplier_data": json.load(open(r"data\suppliers.json")),
    "rules": json.load(open(r"data\rules.json")),
}

final_state = graph.invoke(initial_state)

print("\nFinal LangGraph State:")
print(final_state)



LOG_FILE = r"data\decision.json"

final_state["timestamp"] = datetime.now().isoformat()

if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
    with open(LOG_FILE, "r") as f:
        decision_log = json.load(f)
else:
    decision_log = []

decision_log.append(final_state)

with open(LOG_FILE, "w") as f:
    json.dump(decision_log, f, indent=2)
