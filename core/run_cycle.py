"""
NHS-Flow v1
Purpose: Validate a complete end-to-end decision cycle
using simulated NHS-style data with human-in-the-loop approval.
"""



import json
from ward_manager import predict_shortage
from logistics_agent import plan_delivery
from compliance_agent import check_compliance
from datetime import datetime

ward = json.load(open(r"data\ward_state.json"))
suppliers = json.load(open(r"data\suppliers.json"))
rules = json.load(open(r"data\rules.json"))

decision = {}

if predict_shortage(ward):
    supplier = suppliers[0]
    delivery = plan_delivery(supplier)
    compliant = check_compliance(supplier, rules)
    human_approval = ""
    
    print("Shortage predicted")

    if compliant:
        print(f"Delivery from {supplier['name']}")
        print(f"ETA: {delivery['eta_hours']} hours")
        print(f"Estimated Cost: £{delivery['estimated_cost']}")

        human_approval = input("Approve delivery? (yes/no): ").strip().lower()

        if human_approval == "yes":
            print("Delivery approved and scheduled.")
            final_status = "SCHEDULED"
            approved = True
        else: 
            print("Delivery rejected by human.")
            final_status = "REJECTED"
            approved = False

    else:
        print("Supplier does not comply with regulations.")
        human_approval = "no"
        final_status = "BLOCKED_NON_COMPLIANT"
        approved = False

    decision = {
        "shortage_detected": True,
        "item": ward["item"],
        "supplier": supplier["name"],
        "eta_hours": delivery["eta_hours"],
        "cost": delivery["estimated_cost"],
        "approved_by_human": approved,
        "final_status": final_status
    }
else:
    print("Stock levels sufficient.")
    decision = {
        "shortage_detected": False,
        "final_status": "NO_ACTION_REQUIRED"
    }


LOG_FILE = r"data\decision.json"
   
decision["timestamp"] = datetime.now().isoformat()

try:
    with open(LOG_FILE, "r") as f:
        decision_log = json.load(f)
except FileNotFoundError:
    decision_log = []

decision_log.append(decision)

with open(LOG_FILE, "w") as f:
    json.dump(decision_log, f, indent=2)

print("\nFinal Decision:")
print(decision)