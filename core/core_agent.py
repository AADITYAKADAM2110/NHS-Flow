import json
# Import your real functions
from check_stock_function import check_stock
from get_supplier_function import get_supplier
from place_order import place_order_and_calculate

# Define file paths
INVENTORY_PATH = r"data/inventory.json"
SUPPLIER_PATH = r"data/suppliers.json"

class Agent:
    def __init__(self, name, instructions, model="gpt-4o-mini", tools=None):
        self.name = name
        self.instructions = instructions
        self.model = model
        self.tools = tools if isinstance(tools, list) else [tools] if tools else []

    def run(self, query, state, openai):
        print(f"\n🧠 {self.name} STARTING RUN...")
        print(f"   📝 INPUT QUERY: {query}")
        
        messages = [
            {"role": "system", "content": self.instructions},
            {"role": "user", "content": query}
        ]

        # --- DEBUG: See what the Agent sees ---
        # print(f"   📜 SYSTEM PROMPT: {self.instructions[:100]}...") 

        while True:
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools if self.tools else None,
            )
            
            msg = response.choices[0].message
            
            # --- DEBUG: See what the Agent thinks ---
            if msg.content:
                print(f"   💭 {self.name} THOUGHT: {msg.content}")

            # If AI talks (no tools), return the text
            if not msg.tool_calls:
                print(f"   🛑 {self.name} STOPPING (No tool calls)")
                return msg.content

            # If AI calls tools, execute them!
            messages.append(msg)
            
            for tool in msg.tool_calls:
                func_name = tool.function.name
                args = json.loads(tool.function.arguments)
                print(f"   🛠️ {self.name} CALLING TOOL: {func_name}")
                print(f"      👉 ARGS: {args}")

                result = "Error: Tool not found."

                # --- REAL TOOL MAPPING ---
                
                # A. STOCK AUDITOR LOGIC
                # A. STOCK AUDITOR LOGIC
                if "stock_auditor" in func_name or func_name == "check_stock":
                    raw_result = check_stock(INVENTORY_PATH)
                    print(f"      🔙 TOOL RESULT (Truncated): {str(raw_result)[:100]}...")
                    
                    result = f"Stock Check Result: {raw_result}"
                    
                    # --- ROBUST PARSING FIX ---
                    # We check if the text "CRITICAL" appears anywhere in the raw result string.
                    # This covers simple strings AND complex JSON structures.
                    if "CRITICAL" in str(raw_result):
                        print("      🚨 CRITICAL SHORTAGE FOUND IN JSON")
                        try:
                            data = json.loads(raw_result)
                            shortages = []
                            
                            # Handle different data structures
                            for k, v in data.items():
                                # Check if 'v' is a string like "CRITICAL: 5"
                                if isinstance(v, str) and "CRITICAL" in v:
                                    shortages.append(k)
                                # Check if 'v' is a dictionary like {"status": "CRITICAL"}
                                elif isinstance(v, dict):
                                    # Convert the whole inner dictionary to string to search for "CRITICAL"
                                    if "CRITICAL" in str(v):
                                        shortages.append(k)
                                        
                            print(f"      📋 PARSED SHORTAGES: {shortages}")
                            if state is not None:
                                state["shortages"] = shortages
                        except Exception as e:
                            print(f"      ❌ PARSING ERROR: {e}")

                # B. PROCUREMENT LOGIC
                elif "procurement" in func_name or func_name == "get_supplier":
                    # Debug: What item are we looking for?
                    current_shortages = state.get("shortages", [])
                    item_to_find = current_shortages[0] if current_shortages else "N95 Respirator Mask"
                    print(f"      🔎 LOOKING FOR SUPPLIER FOR: {item_to_find}")
                    
                    # Try calling with (Item, Path)
                    try:
                        raw_result = get_supplier(item_to_find, SUPPLIER_PATH)
                    except TypeError:
                        # Try calling with (Path, Item)
                        print("      ⚠️ Argument mismatch retry...")
                        raw_result = get_supplier(SUPPLIER_PATH, item_to_find)
                    except Exception as e:
                        print(f"      ❌ SUPPLIER ERROR: {e}")
                        raw_result = "Error finding supplier."

                    print(f"      🔙 SUPPLIER FOUND: {raw_result}")
                    result = f"Supplier Options: {raw_result}"
                    if state is not None:
                        state["options"] = raw_result

                # C. PLACE ORDER LOGIC
                elif func_name == "place_order_and_calculate":
                    item = args.get("item_name")
                    qty = args.get("quantity")
                    supplier = args.get("supplier_info")
                    cost = args.get("cost_per_unit")
                    
                    print(f"      💳 PLACING ORDER: {qty}x {item} from {supplier}")
                    result = place_order_and_calculate(item, qty, supplier, cost)
                    print(f"      🔙 ORDER RESULT: {result}")
                    
                    if "SUCCESS" in result and state is not None:
                        state["order_confirmed"] = True

                else:
                    result = f"Tool {func_name} executed (Simulation)"

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool.id,
                    "content": str(result)
                })
        
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
                            "description": "The task or question for the specialist agent."
                        }
                    },
                    "required": ["query"]
                }
            }
        }