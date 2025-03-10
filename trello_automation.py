import requests
import yaml
from dotenv import load_dotenv
import os

# ✅ Load extracted insights from `output.yaml`
with open("output.yaml", "r") as file:
    tasks = yaml.safe_load(file)  # Load YAML as a list of tasks

# Load environment variables from .env file
load_dotenv()

# Accessing variables
API_KEY = os.getenv("TRELLO_API_KEY")
TOKEN = os.getenv("TRELLO_TOKEN")
BOARD_ID = os.getenv("TRELLO_BOARD_ID")
LIST_ID_TODO = os.getenv("TRELLO_LIST_ID")

# ✅ Trello API URL for Creating a Card
TRELLO_URL = "https://api.trello.com/1/cards"

# ✅ Loop through all extracted tasks in YAML
for task_data in tasks:
    task_name = f"{task_data['Feature']} - {task_data['Priority']} Priority"
    task_description = f"**Deadline:** {task_data['Deadline']}\n**Assigned to:** {', '.join(task_data['Assigned to'])}"

    # ✅ Trello API Request Parameters
    params = {
        "key": API_KEY,
        "token": TOKEN,
        "idList": LIST_ID_TODO,  # Add task to "To Do" list
        "name": task_name,
        "desc": task_description
    }

    # ✅ Send the request to Trello
    response = requests.post(TRELLO_URL, params=params)

    # ✅ Handle API Response
    if response.status_code == 200:
        print(f"✅ Task '{task_name}' successfully created in Trello!")
    else:
        print(f"❌ Failed to create task '{task_name}':", response.json())
