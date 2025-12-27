from typing import TypedDict, Dict, Any

class NHSFlowState(TypedDict):
    
    ward: Dict[str, any]
    supplier_data: Dict[str, Any]
    rules: Dict[str, Any]
    
    shortage_detected: bool
    item: str
    supplier: str
    eta_hours: int
    cost: float
    supplier_compliant: bool

    approved_by_human: bool
    final_status: str