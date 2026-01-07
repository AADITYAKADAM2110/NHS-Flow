import json
from openai import OpenAI, Agent
from dotenv import load_dotenv

load_dotenv(load_dotenv=True)

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
        if quantity < min_threshold:
            inventory_status[name] = f"Low Stock - {min_threshold} required"
        else:
            inventory_status[name] = "In Stock"
            print("Inventory Status:")
            print(inventory_status)
    return inventory_status

