from backend.agent import Agency
from backend.llm import load_model, generate_response
from backend.retriever import GroundwaterRetriever

def main():
    print("🤖 Initializing Agent for Debugging...")
    
    # Load Real Components
    llm = load_model()
    print("📚 Loading Knowledge Base...")
    retriever = GroundwaterRetriever()
    try:
        retriever.load()
    except Exception:
        print("⚠️  Vectorstore not found.")
        return

    agent = Agency(llm, retriever)
    
    # query = "What is the detailed cost for a 600ft borewell?"
    query = "can i drill borewells in chennai?"
    
    print(f"\n❓ User Query: {query}\n" + "-"*50)
    
    step_count = 0
    for step in agent.run(query):
        step_count += 1
        status = step["status"]
        content = step["content"]
        
        if status == "thought":
            print(f"[THOUGHT]: {content}")
        elif status == "action":
            print(f"[ACTION]:  {content}")
        elif status == "observation":
            print(f"[OBSERVATION]: {content}")
        elif status == "final":
            print(f"[FINAL ANSWER]: {content}")

    if step_count > 1:
        print("\n" + "="*50)
        print("🎉 Finished.")
    else:
        print("\n❌ Failed: Agent answered directly without thinking.")

if __name__ == "__main__":
    main()
