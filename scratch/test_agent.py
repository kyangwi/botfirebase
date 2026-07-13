import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sqlchat_project.settings")
django.setup()

from chat.utils import init_database
from chat.agent_graph import run_agent_graph

def test_agent():
    db = init_database(None, None, None)
    print("Database loaded.")
    
    query = "What is the revenue?"
    print(f"\nRunning agent graph for query: '{query}'")
    
    result = run_agent_graph(query, db, chat_history=[])
    
    print("\n--- AGENT RESULT ---")
    print(f"Intent classified: {result.intent}")
    print(f"SQL Query generated: {result.sql_query}")
    print(f"SQL Result: {result.sql_result}")
    print(f"Chart Payload: {result.chart_payload}")
    print(f"Retries used: {result.retries_used}")
    print(f"Error (if any): {result.error}")
    print(f"Response Text:\n{result.response_text}")

if __name__ == "__main__":
    test_agent()
