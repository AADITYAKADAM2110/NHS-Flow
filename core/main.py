import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

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
}
]

openai_client = OpenAI()

messages = [
    {
        "role": "system",
        "content": "You are a Ward Manager. You have a tool called check_stock. Always use it before answering."
    },
    {
        "role": "user",
        "content": "Do we have enough N95 masks?"
    }
]

# first call: AI decides to use the tool
response = openai_client.chat.completions.create(
    model="gpt-4.1-nano",
    messages=messages,
    tools=tools
)

assistant_message = response.choices[0].message

# if-else logic to handle tool usage

if assistant_message.tool_calls:

    #IMPORTANT: Append the assistant message before tool calls
    messages.append(assistant_message)

    # Process each tool call
    for tool_call in assistant_message.tool_calls:
        function_name = tool_call.function.name

        if function_name != "check_stock":
            print(f"Running tool: {function_name}...")

        # step A: run your python function
        result = check_stock(filepath)

        # step B: append the tool response to the messages
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id, #receipt id
            "content": result # actual data from the function
        })

    final_response = openai_client.chat.completions.create(
        model="gpt-4.1-nano",
        messages=messages
    )
    print(f"\nNHS Ward Manager: {final_response.choices[0].message.content}")
else:
    print(f"\nNHS Ward Manager: {assistant_message.content}")

