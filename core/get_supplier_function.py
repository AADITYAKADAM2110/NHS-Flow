from agents import function_tool
import json

   

@function_tool
def get_supplier(item_name: str, file_path_supplier: str) -> str:
    
    """The function to get supplier info."""

    try:
        with open(file_path_supplier, 'r') as file:
            suppliers = json.load(file)
    except FileNotFoundError:
        return "Error: Supplier file not found."

    supplier_info = {}

    for supplier in suppliers:

        name = supplier.get('name')
        nhs_approved = supplier.get('nhs_approved', False)
        supplier_info[name] = "NHS Approved" if nhs_approved else "Not NHS Approved"
        cost_per_unit = supplier.get('cost_per_unit', 'N/A')
        supplier_info[name] += f", Cost per unit: {cost_per_unit}"
        delivery_time = supplier.get('delivery_time_hours', 'N/A')
        supplier_info[name] += f", Delivery time (hours): {delivery_time}"
        

    
    return json.dumps(supplier_info) # Return as JSON string for better readability
