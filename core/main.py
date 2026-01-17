from openai import OpenAI
from dotenv import load_dotenv
from saved_agents import manager, communication_officer

load_dotenv()

# INITIATE SHARED STATE
state = {
    "shortages": [],
    "options": [],
    "receipt": [],      # New field for the final table
    "total_spent": 0.0, # New field for math
    "human_approval": False,
    "current_agent": manager,
    "order_confirmed": False,
    "email_draft": "",
    "email_sent": False
}

def run_system():
    print("\n" + "="*50)
    print("🚀 NHS-FLOW SYSTEM STARTED")
    print("="*50)

    # 1. INITIAL ANALYSIS LOOP
    user_query = "Are we in stock? If not, find suppliers."
    response = state["current_agent"].run(
        query=user_query,
        state=state,
        openai=OpenAI()
    )

    # 2. HUMAN CHECKPOINT (Financial Approval)
    if state["shortages"] and not state["human_approval"]:
        print("\n" + "-"*50)
        print(f"🚨 AUDIT REPORT: Critical Shortages Detected: {state['shortages']}")
        print("-"*50)
        
        choice = input("\n👤 SUPERVISOR: Do you approve placing the order? (yes/no): ").strip().lower()
        
        if choice == 'yes':
            state["human_approval"] = True
            
            # --- FORCE EXECUTION PROMPT ---
            print("\n⚙️ AUTHORIZING PURCHASE AGENTS...")
            order_query = (
                f"AUTHORIZATION GRANTED. The human has approved the purchase. "
                f"IMMEDIATELY use the 'place_order' tool for these items: {state['shortages']}. "
                f"REQUIREMENTS: "
                f"1. Select the Cheapest NHS-Approved Supplier found in history. "
                f"2. Quantity = (Threshold - Current Stock) + 10 buffer. "
                f"3. DO NOT ask for permission again. EXECUTE the tool now."
            )
            
            order_response = state["current_agent"].run(
                query=order_query,
                state=state,
                openai=OpenAI()
            )
            print(f"\n✅ AGENT REPORT: {order_response}")

        else:
            print("🛑 Order denied by Supervisor.")
            return

    # 3. COMMUNICATION CHECKPOINT
    if state["order_confirmed"]:
        print("\n" + "-"*50)
        print("📨 PREPARING SUPPLIER CONFIRMATION EMAILS...")
        
        email_context = f"Items ordered: {state['receipt']}. Total Value: £{state['total_spent']}"
        draft = communication_officer.run(email_context, state, OpenAI()) # Reuse the run method
        
        state["email_draft"] = draft
        print(f"\n--- DRAFT EMAIL ---\n{draft}\n-------------------")

        confirm = input("\n👤 SUPERVISOR: Send this email? (yes/no): ").strip().lower()
        if confirm == "yes":
            print("\n🚀 Email Sent Successfully!")
            state["email_sent"] = True

    # 4. FINAL MARKDOWN RECEIPT
    print("\n\n")
    print("="*60)
    print(f"{'🏥 NHS-FLOW FINAL SESSION RECEIPT':^60}")
    print("="*60)
    
    if state["order_confirmed"] and state["receipt"]:
        # Header
        print(f"{'ITEM':<25} | {'SUPPLIER':<20} | {'QTY':<5} | {'TOTAL':<10}")
        print("-" * 65)
        
        # Rows
        for row in state["receipt"]:
            # row = [Item, Supplier, Qty, UnitCost, TotalCost]
            item_name = row[0][:23] # Truncate if too long
            supplier = row[1][:18]
            qty = str(row[2])
            total = str(row[4])
            print(f"{item_name:<25} | {supplier:<20} | {qty:<5} | {total:<10}")
            
        print("-" * 65)
        print(f"{'GRAND TOTAL':<53} | £{state['total_spent']:.2f}")
    else:
        print("❌ No orders were finalized in this session.")
        
    print("="*60 + "\n")

if __name__ == "__main__":
    run_system()