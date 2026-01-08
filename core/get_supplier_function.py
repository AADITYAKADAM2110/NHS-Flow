from agents import function_tool
import json

ordered_items = set()


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
        items = supplier.get('items_supplied', [])

        if item_name in items:
            supplier_info[supplier['supplier_name']] = {
                "contact": supplier.get('contact', 'N/A'),
                "items_supplied": items
            } # this if condition checks if the item is supplied by the supplier
        else:
            continue

        supplier_info["note"] = "Ensure to place the order only once per item."
        supplier_info["ordered_items"] = list(ordered_items)
        
        if item_name not in ordered_items:
            ordered_items.add(item_name) # Track ordered items to avoid duplicates

        supplier_info["cost_per_unit"] = supplier.get('cost_per_unit', 'N/A')
        supplier_info["name"] = supplier.get('name', 'N/A')
        supplier_info["nhs_approved"] = supplier.get('nhs_approved', False)
        supplier_info["delivery_time_hours"] = supplier.get('delivery_time_hours', 'N/A')
        supplier_info["carbon_footprint"] = supplier.get('carbon_footprint', 'N/A')

    
    return json.dumps(supplier_info) # Return as JSON string for better readability
