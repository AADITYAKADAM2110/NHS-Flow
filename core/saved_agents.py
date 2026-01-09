from core_agent import Agent
from instructions import stock_auditor_instructions, procurement_agent_instructions, manager_instructions, communications_officer_instructions
from tools import check_stock_tool_schema, get_supplier_tool_schema, place_order_tool_schema


stock_auditor = Agent(
    name="Stock Auditor",
    instructions=stock_auditor_instructions,
    tools=check_stock_tool_schema,
    model="gpt-4.1-nano"
)

stock_auditor_tool = stock_auditor.as_tool(tool_name="stock_auditor_tool", tool_description="Use this tool to check stock levels and identify critical shortages.")

procurement_specialist = Agent(
    name="Procurement Specialist",
    instructions=procurement_agent_instructions,
    tools=get_supplier_tool_schema,
    model="gpt-4.1-nano"
)

communication_officer = Agent(
    name="Communication Officer",
    instructions=communications_officer_instructions,
    model="gpt-4.1-nano"
)

procurement_specialist_tool = procurement_specialist.as_tool(tool_name="procurement_specialist_tool", tool_description="Use this tool to find NHS-approved suppliers for critical items.")

manager_tools = [stock_auditor_tool, procurement_specialist_tool, place_order_tool_schema]

manager = Agent(
    name="NHS-Flow Supervisor",
    instructions=manager_instructions,
    tools = manager_tools
)