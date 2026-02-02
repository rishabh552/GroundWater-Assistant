
import os
import sys

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.agent import Agency
from backend.llm import load_model
from backend.retriever import get_retriever

def test_agent(query, role="farmer"):
    print(f"\n--- Testing Query ({role}): {query} ---")
    
    # Load model and retriever
    llm = load_model()
    retriever = get_retriever()
    
    agency = Agency(llm, retriever)
    
    for update in agency.run(query, user_role=role):
        status = update["status"]
        content = update["content"]
        
        if status == "thought":
            print(f"THOUGHT: {content}")
        elif status == "action":
            print(f"ACTION: {content}")
        elif status == "observation":
            print(f"OBSERVATION: {content[:200]}...")
        elif status == "final":
            print(f"FINAL ANSWER:\n{content}")

if __name__ == "__main__":
    # Test cases
    queries = [
        ("What is the minimum distance I must maintain between my well and my neighbor's well in Salem?", "farmer"),
        ("I am a small farmer in Kallakurichi. Are there any government schemes for my new borewell?", "farmer"),
        ("How much HP motor do I need for a 500ft borewell?", "officer")
    ]
    
    for q, r in queries:
        test_agent(q, r)
