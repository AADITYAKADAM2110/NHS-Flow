import json
from openai import OpenAI, Agent
from dotenv import load_dotenv

load_dotenv(load_dotenv=True)

# datasource
filepath = r"data/inventory.json"


def check_stock(file_path):
    """The actual python function that reads the file."""
    # Logic fix: Only read the file once
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


# Define the tool for openai

tools_schema = {
    "type": "function",
    "function": {
        "name": "check_stock",
        "description": "Check the inventory stock levels from a JSON file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the inventory JSON file."
                }
            },
            "required": ["file_path"]
        }
    }
}