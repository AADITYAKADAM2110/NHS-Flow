import json
from session_variables import SESSION_BUDGET, TOTAL_SPENT

filepath = r"data/inventory.json"


def place_order_and_calculate(item_name: str, quantity: int, supplier_info, cost_per_unit: float = 0.0) -> str:
    
    tool_description = """
    Simulates placing an order for a given item from a supplier.
    Updates inventory records accordingly.

    Args:
        item_name (str): The name of the item to order.
        quantity (int): The quantity of the item to order.
        supplier_info (dict): Information about the supplier.
        cost_per_unit (float): Cost per unit of the item.
    """

    global TOTAL_SPENT, SESSION_BUDGET

    estimated_cost = float(cost_per_unit) * int(quantity)

    if (TOTAL_SPENT + estimated_cost) > SESSION_BUDGET:
        remaining_budget = SESSION_BUDGET - TOTAL_SPENT
        return f"ERROR: Cannot place order. Budget exceeded by {estimated_cost - remaining_budget:.2f} GBP. Remaining budget: {remaining_budget:.2f} GBP. Request Manual approval."
    

    try: 
        with open(filepath, 'r') as file:
            inventory = json.load(file)

        item_found = False

        for item in inventory:
            if item['name'].lower() == item_name.lower():
                item["current_stock"] += quantity
                item["last_updated"] = "Just Now"
                item_found = True
                break

        if not item_found:
            return f"Item '{item_name}' not found in inventory."
        
        with open(filepath, 'w') as file:
            json.dump(inventory, file, indent=4)

        TOTAL_SPENT += estimated_cost
        return f"SUCCESS: Order placed for {quantity} of '{item_name}' from {supplier_info['name']}. Estimated cost: {estimated_cost:.2f} GBP. Total spent this session: {TOTAL_SPENT:.2f} GBP."
        
    
    except Exception as e:
        return f"ERROR: {str(e)}"