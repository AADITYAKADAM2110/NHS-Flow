from openai import OpenAI
from dotenv import load_dotenv
from saved_agents import manager, communication_officer
from session_variables import TOTAL_SPENT

load_dotenv()



# INITIATE SHARED  STATE
state = {
    "shortages": [],
    "options": [],
    "contact": {},
    "human_approval": False,
    "current_agent": manager,
    "order_confirmed": False,
    "email_draft": "",
    "email_sent": False
}

def run_system():
    """Main function to run the NHS-Flow system."""

    print("NHS-Flow System Started...")

    user_query = "Are we in stock? If not, find suppliers."

    response = state["current_agent"].run(
        query=user_query,
        state=state,
        openai=OpenAI()
    )

    if state["shortages"] and not state["human_approval"]:
        print(f"\n AUDIT: Shortages detected: {state['shortages']}. \nEstimated costs: £{state['options']}")
        choice = input("Do you approve placing the order? (yes/no): ").strip().lower()
        if choice == 'yes':
            state["human_approval"] = True
            order_query = f"Place orders for the following items: {state['shortages']} with estimated costs: £{state['options']}."
            order_response = state["current_agent"].run(
                query=order_query,
                state=state,
                openai=OpenAI()
            )
            print(f"\nORDER RESPONSE: {order_response}")

        else:
            print("Order not approved by human supervisor.")
            return
        
    if state["order_confirmed"] == True:
        print("\n ORDER IS CONFIRMED. Activating Communication Officer...")

        email_context = f"Items ordered: {state['options']}. Total: £{TOTAL_SPENT}. Contact details: {state['contact']}"

        draft = communication_officer.run(email_context)
        state["email_draft"] = draft

        print(f"\n EMAIL DRAFT \n   \n {email_context} \n")

        confirm = input("Would you like to send this email to the supplier? (yes/no):").strip().lower()

        if confirm == "yes":
            print("\n Email Sent!")
            state["email_sent"] = True

    print(f"\nFINAL RESPONSE: {response}")
    print(f"\nSession Completed Verified Total Spent: £{state['options']}")



    
run_system()