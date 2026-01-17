import json
import random
import os
from datetime import datetime

# PATH SETUP
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

# CONFIGURATION
NUM_ITEMS = 50

# Categories for realsitic generation
categories = {
    "PPE": ["Gloves", "Gown", "Face Shield", "Shoe Covers", "Apron", "Surgical Mask"],
    "Medication": ["Amoxicillin", "Ibuprofen", "Insulin", "Metformin", "Atorvastatin", "Paracetamol"],
    "Equipment": ["Syringe 5ml", "Cannula 18G", "Bandage", "Gauze", "Scalpel", "Thermometer"],
    "Critical": ["N95 Respirator Mask", "Paracetamol IV 10mg"] # Keep originals!
}

# Supplier Data (Templates)
suppliers_list = [
    {"name": "MedSupply Co (Manchester)", "nhs": True, "speed": 24, "markup": 1.0, "carbon": "Medium"},
    {"name": "GreenHealth Logistics (London)", "nhs": True, "speed": 4, "markup": 1.2, "carbon": "Low"},
    {"name": "BudgetMedical Global (Overseas)", "nhs": False, "speed": 72, "markup": 0.6, "carbon": "High"},
    {"name": "RapidResponse York", "nhs": True, "speed": 12, "markup": 1.1, "carbon": "Medium"},
    {"name": "Global Pharma Corp", "nhs": False, "speed": 48, "markup": 0.8, "carbon": "High"}
]

def generate_datasets():
    inventory = []
    supplier_catalog = []

    # GENERATE SUPPLIERS FIRST
    print(f"Generating Suppliers Catalog...")
    
    for sup in suppliers_list:
        clean_name = sup['name'].replace(" ", "").replace("(", "").replace(")", "").lower()
        supplier_catalog.append({
            "supplier_id": f"SUP-{sup['name'][:3].upper()}-{random.randint(10,99)}",
            "name": sup["name"],
            "nhs_approved": sup['nhs'],
            "delivery_time_hours": sup['speed'],  
            "cost_per_unit": {},
            "carbon_footprint": sup['carbon'],
            "contact": {
                "email": f"sales@{clean_name[:15]}.com",
                "phone": f"+44 {random.randint(7000, 7999)} {random.randint(100000, 999999)}" 
            }
        })

    # GENERATE INVENTORY ITEMS 
    print(f"Generating {NUM_ITEMS} inventory items...")

    all_item_names = categories["Critical"][:]

    while len(all_item_names) < NUM_ITEMS:
        cat_key = random.choice(['PPE', 'Medication', 'Equipment'])
        base_name = random.choice(categories[cat_key])
        suffix = random.choice(["(Size S)", "(Size M)", "(Size L)", "Type A", "Type B", "Generic", "Pack"])
        new_name = f"{base_name} {suffix}"
        
        if new_name not in all_item_names:
            all_item_names.append(new_name)

    # Build Inventory List
    for name in all_item_names:
        # Generate ID (e.g., N95 Respirator Mask -> PPE-N95-123)
        # Simple heuristic to guess category prefix
        if "Paracetamol" in name or "Ibuprofen" in name or "Insulin" in name:
            cat_prefix = "MED"
            cat_full = "Medication"
        elif "Syringe" in name or "Scalpel" in name:
            cat_prefix = "EQP"
            cat_full = "Equipment"
        else:
            cat_prefix = "PPE"
            cat_full = "PPE"

        clean_slug = name.split()[0].upper()[:4]
        item_id = f"{cat_prefix}-{clean_slug}-{random.randint(100, 999)}"
        
        # Randomize Stock
        # 30% chance of critical shortage
        if random.random() < 0.3:
            min_thresh = random.randint(50, 100)
            current = random.randint(0, 20)
        else:
            min_thresh = random.randint(20, 50)
            current = random.randint(60, 200)
            
        item_entry = {
            "item_id": item_id,
            "name": name,
            "category": cat_full,
            "location": f"Zone {random.choice(['A', 'B', 'C', 'ICU', 'Pharmacy'])}",
            "current_stock": current,
            "min_threshold": min_thresh,
            "unit": "box" if cat_prefix == "PPE" else "vial" if cat_prefix == "MED" else "pack",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S") # <--- ADDED THIS
        }
        inventory.append(item_entry)

        # --- UPDATE SUPPLIER PRICES FOR THIS ITEM ---
        base_price = round(random.uniform(2.0, 45.0), 2)
        
        for sup_data, sup_obj in zip(suppliers_list, supplier_catalog):
            # Calculate price with variation
            price = round(base_price * sup_data['markup'] * random.uniform(0.95, 1.05), 2)
            
            # 80% chance this supplier stocks this item
            if random.random() < 0.8:
                sup_obj["cost_per_unit"][item_id] = price

    # --- SAVE FILES ---
    # Ensure directory exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    with open(os.path.join(DATA_DIR, "inventory.json"), "w") as f:
        json.dump(inventory, f, indent=4)
        
    with open(os.path.join(DATA_DIR, "suppliers.json"), "w") as f:
        json.dump(supplier_catalog, f, indent=4)

    print("✅ SUCCESS! Generated realistic datasets matching your exact schema.")
    print(f"   - {len(inventory)} items in inventory.json")
    print(f"   - {len(supplier_catalog)} suppliers in suppliers.json")

if __name__ == "__main__":
    generate_datasets()