import json
import os
# Import your real functions
from check_stock_function import check_stock
from get_supplier_function import get_supplier
from place_order import place_order

# --- ABSOLUTE PATH SETUP ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR) if "core" in BASE_DIR else BASE_DIR
INVENTORY_PATH = os.path.join(PROJECT_ROOT, "data", "inventory.json")
SUPPLIER_PATH = os.path.join(PROJECT_ROOT, "data", "suppliers.json")

class Agent:
    def __init__(self, name, instructions, model="gpt-4o-mini", tools=None):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.tools = tools if isinstance(tools, list) else [tools] if tools else []

    def run(self, query, state, openai):
        print(f"\n🧠 {self.name} STARTING RUN...")
        
        messages = [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": query}
        ]

        while True:
            # 1. Call OpenAI
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools if self.tools else None,
            )
            
            msg = response.choices[0].message

            # 2. If AI just talks (no tools), return the text
            if not msg.tool_calls:
                return msg.content

            # 3. If AI calls tools, we MUST process ALL of them
            messages.append(msg)
            
            for tool in msg.tool_calls:
                func_name = tool.function.name
                args = json.loads(tool.function.arguments)
                print(f"   🛠️ {self.name} CALLING TOOL: {func_name}")

                result = "Error: Tool not found."

                # --- TOOL A: STOCK AUDITOR ---
                if "stock_auditor" in func_name or func_name == "check_stock":
                    raw_result = check_stock(INVENTORY_PATH)
                    print(f"      🔙 STOCK RESULT: {str(raw_result)[:50]}...")
                    
                    result = f"Stock Check Result: {raw_result}"
                    
                    if "CRITICAL" in str(raw_result):
                        print("      🚨 CRITICAL SHORTAGE DETECTED")
                        try:
                            data = json.loads(raw_result)
                            shortages = []
                            for k, v in data.items():
                                # Robust check for nested dicts or strings
                                if (isinstance(v, str) and "CRITICAL" in v) or \
                                   (isinstance(v, dict) and "CRITICAL" in str(v)):
                                    shortages.append(k)
                            
                            print(f"      📋 PARSED SHORTAGES: {shortages}")
                            if state is not None:
                                state["shortages"] = shortages
                        except Exception as e:
                            print(f"      ❌ PARSING ERROR: {e}")

                # --- TOOL B: PROCUREMENT SPECIALIST ---
                elif "procurement" in func_name or func_name == "get_supplier":
                    # Smart Item Detection
                    current_shortages = state.get("shortages", [])
                    item_to_find = None
                    query_text = args.get('query', '').lower()
                    
                    # check if the query mentions a specific shortage
                    for short_item in current_shortages:
                        if short_item.lower() in query_text:
                            item_to_find = short_item
                            break
                    if not item_to_find:
                        item_to_find = current_shortages[0] if current_shortages else "N95 Respirator Mask"

                    print(f"      🔎 LOOKING FOR SUPPLIER FOR: {item_to_find}")
                    
                    # Call function safely
                    try:
                        raw_result = get_supplier(item_to_find, SUPPLIER_PATH)
                    except TypeError:
                        raw_result = get_supplier(SUPPLIER_PATH, item_to_find)
                    
                    print(f"      🔙 SUPPLIER FOUND: {str(raw_result)[:50]}...")
                    result = f"Supplier Options for {item_to_find}: {raw_result}"
                    
                    # Save options
                    if state is not None:
                        if "options" not in state or not isinstance(state["options"], list):
                            state["options"] = []
                        state["options"].append(f"{item_to_find}: {raw_result}")

                # --- TOOL C: PLACE ORDER ---
                elif func_name == "place_order":
                    item = args.get("item_name")
                    qty = args.get("quantity")
                    supplier = args.get("supplier_info")
                    cost = args.get("cost_per_unit")
                    
                    # Calculate Receipt
                    try:
                        total = float(qty) * float(cost)
                        if state.get("total_spent") is None: state["total_spent"] = 0
                        state["total_spent"] += total
                        
                        # Add to receipt list for final display
                        if "receipt" not in state: state["receipt"] = []
                        state["receipt"].append([item, supplier, qty, f"£{cost}", f"£{total}"])
                        
                        print(f"      💳 ORDERING: {qty}x {item} (Total: £{total})")
                    except:
                        print("      ⚠️ Cost calculation error")

                    result = place_order(item, qty, supplier, cost)
                    if "SUCCESS" in result and state is not None:
                        state["order_confirmed"] = True

                else:
                    result = f"Tool {func_name} executed (Simulation)"

                # IMPORTANT: Append the result to history
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool.id,
                    "content": str(result)
                })
    
    # Required for the Manager to treat this agent as a tool
    def as_tool(self, tool_name, tool_description):
        return {
            "type": "function",
            "function": {
                "name": tool_name,
                "description": tool_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The task or question."
                        }
                    },
                    "required": ["query"]
                }
            }
        }