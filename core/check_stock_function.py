from agents import function_tool
import json

@function_tool
def check_stock(file_path: str) -> str:

    """Tool to check stock levels in the inventory."""
    
    try:
        with open(file_path, 'r') as file:
            inventory = json.load(file)
    except FileNotFoundError:
        return "Error: Inventory file not found."
    
    inventory_status = {}
    
    for item in inventory:
        item_name = item.get('item_name', 'Unknown Item')
        quantity = item.get('quantity', 0)
        critical_threshold = item.get('critical_threshold', 0)
        
        if quantity <= critical_threshold:
            status = "CRITICAL"
        else:
            status = "Sufficient"
        
        inventory_status[item_name] = {
            "name": item_name,
            "quantity": quantity,
            "critical_threshold": critical_threshold,
            "status": status
        }
    
    return json.dumps(inventory_status) # Return as JSON string for better readability, don't just print 