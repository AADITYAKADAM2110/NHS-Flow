import json

filepath = r"data/inventory.json"

def place_order(item_name: str, quantity: int, supplier_info):
    """
    Simulates placing an order for a given item from a supplier.
    Updates inventory records accordingly.

    Args:
        item_name (str): The name of the item to order.
        quantity (int): The quantity of the item to order.
        supplier_info (dict): Information about the supplier.
    """

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

        return f"SUCCESS: Stock updated. New level: {item['current_stock']}. Ordered {quantity} from {supplier_info['name']}."
    
    except Exception as e:
        return f"ERROR: {str(e)}"