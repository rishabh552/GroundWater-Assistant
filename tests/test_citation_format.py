"""
Test if the agent properly includes both natural language AND cited data
"""
from backend.agent import Agency
from backend.llm import load_model
from backend.retriever import GroundwaterRetriever

def test_citation_format():
    print("🧪 Testing Agent Response Format (Natural + Citations)...")
    print("="*70)
    
    # Load components
    print("Loading model and retriever...")
    llm = load_model()
    retriever = GroundwaterRetriever()
    
    try:
        retriever.load()
    except FileNotFoundError:
        print("❌ Vectorstore not found. Run 'python ingest.py' first.")
        return
    
    agent = Agency(llm, retriever)
    
    # Test query
    query = "What is the groundwater status in Chennai?"
    
    print(f"\n{'='*70}")
    print(f"📝 Testing Query: {query}")
    print('='*70)
    
    has_natural_response = False
    has_data_section = False
    has_source_citation = False
    final_answer = ""
    
    for step in agent.run(query):
        status = step["status"]
        content = step["content"]
        
        if status == "thought":
            print(f"💭 THOUGHT: {content[:100]}...")
        elif status == "action":
            print(f"🔧 ACTION: {content}")
        elif status == "observation":
            print(f"👁️  OBSERVATION (preview): {content[:150]}...")
        elif status == "final":
            final_answer = content
            print(f"\n✅ FINAL ANSWER:")
            print("="*70)
            print(content)
            print("="*70)
            
            # Check response format
            if len(content) > 50 and not content.startswith("==="):
                has_natural_response = True
            
            if "📊" in content or "Retrieved Data" in content:
                has_data_section = True
            
            if ("Source:" in content or ".pdf" in content) and "Page" in content:
                has_source_citation = True
    
    print(f"\n{'='*70}")
    print(f"📊 Format Check Results:")
    print(f"  ✅ Natural Language Response: {'YES' if has_natural_response else '❌ NO'}")
    print(f"  ✅ Data Section (📊): {'YES' if has_data_section else '❌ NO'}")
    print(f"  ✅ Source Citations: {'YES' if has_source_citation else '❌ NO'}")
    
    if has_natural_response and has_data_section and has_source_citation:
        print(f"\n🎉 SUCCESS: Response includes both natural language AND cited data!")
    else:
        print(f"\n⚠️  WARNING: Response format incomplete")
        if not has_natural_response:
            print("  - Missing natural conversational response")
        if not has_data_section:
            print("  - Missing '📊 Retrieved Data from Reports' section")
        if not has_source_citation:
            print("  - Missing source citations (document name, page number)")
    
    print('='*70)

if __name__ == "__main__":
    test_citation_format()
