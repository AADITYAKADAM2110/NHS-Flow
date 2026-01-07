import json
from openai import OpenAI
from dotenv import load_dotenv
from check_stock_function import check_stock
from get_supplier_function import get_supplier
from place_order import place_order
from tools import tools

load_dotenv()

# datasource
filepath = r"data/inventory.json"
filepath_supplier = r"data/suppliers.json"



openai_client = OpenAI()

messages = [
    {
        "role": "system",
        "content": "You are an NHS Global Inventory Auditor. Your primary goal is clinical safety. Whenever you run a stock check, you MUST analyze the entire result. If you detect ANY critical shortages—even if the user didn't ask about them—you must flag them, find suppliers for them, and include them in your final report. Never ignore a shortage. After you propose a solution for a shortage, you MUST call check_stock one last time to verify the inventory status of the entire ward. Only when check_stock shows 'All In Stock' are you permitted to end the conversation. You are NOT allowed to finish the conversation until you have resolved ALL critical shortages. EXIT RULE: You can only end the conversation by outputting the exact phrase: 'ALL_ISSUES_RESOLVED'. If there are still items with 'CRITICAL' status in the inventory that you haven't ordered supplies for, you CANNOT say this phrase. You must fix them first."
    },
    {
        "role": "user",
        "content": "Are we in stock? and if not, who can supply them to us quickly?"
    }
]

# The infinite loop to keep the conversation going
while True:
    response = openai_client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=messages,
        tools=tools,
    )

    assistant_message = response.choices[0].message
    messages.append(assistant_message)

    # If the AI is done talking and does not want to use a tool, break the loop
    if assistant_message.tool_calls:
        print("\n Agent is acting...\n")

        for tool_call in assistant_message.tool_calls:
            name = tool_call.function.name
            print(f"Calling tool: {name} (ID: {tool_call.id})")

            if name == "check_stock":
                result = check_stock(filepath)
            elif name == "get_supplier":
                result = get_supplier(filepath_supplier)
            elif name == "place_order":
                args = json.loads(tool_call.function.arguments)
                result = place_order(args["item_name"], args["quantity"], args["supplier_name"])

            else:
                print(f"\nError: AI tried to call unknown tool '{name}'")
                result = f"Error: The tool '{name}' does not exist. Please use 'check_stock' or 'get_supplier'."

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                }
            ) 
    else:
        final_message = assistant_message.content

        if "ALL_ISSUES_RESOLVED" in final_message:
            print("\n✅ NHS Final Report (Authorized):", final_message.replace("ALL_ISSUES_RESOLVED", ""))
            break

        else:
            print("Agent tried to quit early! Kicking it back...")
            messages.append(
                {"role": "user", "content": "You did NOT output the confirmation phrase 'ALL_ISSUES_RESOLVED'. This means you might have missed an item. Check the inventory again and fix ANY remaining shortages."}
            )
            continue