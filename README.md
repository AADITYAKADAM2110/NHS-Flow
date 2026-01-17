# 🏥 NHS-Flow: Autonomous Supply Chain Agent

**NHS-Flow** is an agentic AI system designed to automate the detection and procurement of critical medical supplies. By leveraging a multi-agent architecture, it creates a robust, self-correcting workflow that bridges the gap between inventory databases and supplier logic.



## 🌟 Key Features

* **🕵️‍♂️ Intelligent Stock Auditing:** The `Stock Auditor` agent autonomously scans `inventory.json`, detects items below critical thresholds, and flags them for immediate action.
* **🛒 Strategic Procurement:** The `Procurement Specialist` agent analyzes `suppliers.json` to find the best vendors based on cost, delivery speed, and NHS approval status.
* **🔗 Smart Data Mapping:** Includes a robust translation layer that maps natural language queries (e.g., "Paracetamol") to specific Database IDs (`MED-PARA-500`) to ensure accurate ordering.
* **🛡️ Human-in-the-Loop (HITL):** A safety layer that pauses execution for human supervisor approval before finalizing any financial transaction.
* **📝 Automated Administration:** Automatically updates the inventory database (preventing re-order loops), generates a financial receipt, and drafts confirmation emails to suppliers.

## ⚙️ Architecture

The system operates on a **Shared State** model where three agents collaborate:

1.  **Manager (Supervisor):** The brain that directs traffic. It receives the user intent ("Check stock") and delegates tasks.
2.  **Stock Auditor Tool:** Has read/write access to the Inventory Database.
3.  **Procurement Tool:** Has read access to the Supplier Database and logic to calculate costs.

### The Workflow
1.  **Audit:** System scans for shortages (`Current < Threshold`).
2.  **Sourcing:** System finds valid suppliers for identified items.
3.  **Proposal:** System presents options to the Human Supervisor.
4.  **Execution:** Upon approval, the system:
    * Places the order.
    * **Updates `inventory.json` immediately** (Real-time consistency).
    * Calculates total spend.
5.  **Reporting:** Generates a Markdown receipt and drafts a supplier email.

## 📂 Project Structure

```text
NHS-Flow/
├── core/
│   ├── main.py                 # The entry point (State Machine & Supervisor Logic)
│   ├── core_agent.py           # The Agent Class (LLM Integration & Tool Handling)
│   ├── saved_agents.py         # Agent Personas (Prompts & Roles)
│   ├── check_stock_function.py # Logic to read/parse inventory
│   ├── get_supplier_function.py# Logic to map IDs and find prices
│   └── place_order.py          # Logic to update DB and execute trade
├── data/
|   |__ generate_data.py        # Generate Realistic database
|   |
│   ├── inventory_copy.json     # Copy of the old databse
|   |__ inventory.json          # The Ground Truth database
|   |
|   |__ suppliers_copy.json     # Copy of old database
|   |
│   └── suppliers.json          # Vendor price lists
|             
├── .env                        # API Keys (Not shared)
└── requirements.txt            # Dependencies

🚀 How to Run

1. Clone the repository:
git clone [https://github.com/AADITYAKADAM2110/NHS-Flow](https://github.com/AADITYAKADAM2110/NHS-Flow)
cd NHS-Flow

2. Install Dependencies:
pip install openai python-dotenv

3. Set up Environment: Create a .env file and add your OpenAI Key:
OPENAI_API_KEY=sk-your-key-here

4. Run the System:
python core/main.py

🧠 Technical Challenges Solved
-The "Zombie Loop" Bug: Initially, the agent would place orders but fail to update the database, causing it to panic and re-order infinitely. This was solved by implementing a deterministic place_order function that writes to the JSON file immediately upon execution.

-ID Mismatching: Suppliers use SKUs (PPE-001) while users use names (Masks). A lookup function was engineered to bridge this gap dynamically.

🔜 Future Roadmap
[ ] Add a Frontend UI for the Supervisor Dashboard.

[ ] Possible integration with Gmail API to actually send the drafted emails.

[ ] Migrate JSON database to SQL/PostgreSQL for scalability.

[ ] Build same system using LangGraph and CrewAI to compare the architecture.
