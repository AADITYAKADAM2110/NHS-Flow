tools = [
    {
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
},
    {
    "type": "function",
    "function": {
        "name": "get_supplier",
        "description": "Find NHS-approved suppliers for medical items and check delivery times.",
        "parameters": {
            "type": "object",
            "properties": {
                    "item_name": {
                        "type": "string",
                        "description": "The name of the item needed (e.g., 'N95 Respirator Mask')"
                },
                "file_path_supplier": {
                    "type": "string",
                    "description": "The path to the supplier JSON file."
                }
            },
            "required": ["item_name", "file_path_supplier"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "place_order",
        "description": "Place an order with a supplier for a specific medical item and updates the inventory.",
        "parameters": {
            "type": "object",
            "properties": {
                "supplier_name": {
                    "type": "string",
                    "description": "The name of the supplier to place the order with."
                },
                "item_name": {
                    "type": "string",
                    "description": "The name of the item to order."
                },
                "quantity": {
                    "type": "integer",
                    "description": "The quantity of the item to order."
                }
            },
            "required": ["supplier_name", "item_name", "quantity"]
        }
    }
}
]