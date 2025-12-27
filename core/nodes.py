from ward_manager import predict_shortage
from logistics_agent import plan_delivery
from compliance_agent import check_compliance


def analyze_ward_state(state):

    ward = state["ward"]
    state["shortage_detected"] = predict_shortage(ward)
    return state


def plan_logistics(state):

    supplier = state["supplier_data"][0]
    delivery = plan_delivery(supplier)

    state["supplier"] = supplier["name"]
    state["eta_hours"] = delivery["eta_hours"]
    state["cost"] = delivery["estimated_cost"]
    state["supplier_compliant"] = check_compliance(supplier, state["rules"])
    return state


def human_review(state):

    if not state["supplier_compliant"]:
        state["final_status"] = "BLOCKED_NON_COMPLIANT"
        state["approved_by_human"] = False
        return state
    
    approval = input("Approve delivery? (yes/no): ").strip().lower()

    if approval == "yes":
        state["approved_by_human"] = True
        state["final_status"] = "SCHEDULED"
    else:
        state["approved_by_human"] = False
        state["final_status"] = "REJECTED"

    return state

    