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
        name = item.get('name')
        quantity = item.get('current_stock', 0)
        min_threshold = item.get('min_threshold', 0)

        # Logic fix: Correctly check stock levels
        if quantity < min_threshold:
            inventory_status[name] = f"CRITICAL: {quantity} (Need {min_threshold})"
        else:
            inventory_status[name] = "In Stock"
    
    return json.dumps(inventory_status) # Return as JSON string for better readability, don't just print 