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





    