check_stock_tool_schema ={
        "name": "check_stock",
        "type": "function",
        "description": "Tool to check stock levels in the inventory.",
        "parameters": {
            "file_path": {
                "type": "string",
                "description": "The path to the inventory JSON file."
            }
        },
        "return_type": "JSON string representing inventory status",
        "required": ["file_path"]
    }

get_supplier_tool_schema ={
        "name": "get_supplier",
        "type": "function",
        "description": "Tool to get NHS-approved suppliers for critical items.",
        "parameters": {
            "item_name": {
                "type": "string",
                "description": "The name of the item to find suppliers for."
            },
            "file_path": {
                "type": "string",
                "description": "The path to the suppliers JSON file."
            }
        },
        "return_type": "JSON string representing supplier information",
        "required": ["item_name", "file_path"]
    },

place_order_tool_schema = {
        "name": "place_order",
        "type": "function",
        "description": "Tool to place orders for items from suppliers and update inventory.",
        "parameters": {
            "item_name": {
                "type": "string",
                "description": "The name of the item to order."
            },
            "quantity": {
                "type": "integer",
                "description": "The quantity of the item to order."
            },
            "supplier_info": {
                "type": "set",
                "description": "The name of the supplier to order from."
            },
            "cost_per_unit": {
                "type": "float",
                "description": "Cost per unit of the item."
            }
        },
        "return_type": "string indicating success or failure of the order placement",
        "required": ["item_name", "quantity", "supplier_info", "cost_per_unit"]
    }
