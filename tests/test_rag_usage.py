"""
Test script to verify the agent properly uses RAG contents
"""
from backend.agent import Agency
from backend.llm import load_model
from backend.retriever import GroundwaterRetriever

def test_rag_usage():
    print("🧪 Testing RAG Usage in Agent...")
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
    
    # Test queries that should require RAG
    test_queries = [
        "What is the groundwater status in Chennai?",
        "Can I drill a borewell in Kallakurichi?",
        "Is Salem safe for groundwater extraction?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*70}")
        print(f"📝 Testing Query: {query}")
        print('='*70)
        
        rag_used = False
        source_cited = False
        final_answer = ""
        
        for step in agent.run(query):
            status = step["status"]
            content = step["content"]
            
            if status == "thought":
                print(f"💭 THOUGHT: {content[:150]}...")
            elif status == "action":
                print(f"🔧 ACTION: {content}")
                if "search_knowledge_base" in content:
                    rag_used = True
            elif status == "observation":
                print(f"👁️  OBSERVATION: {content[:200]}...")
            elif status == "final":
                final_answer = content
                print(f"\n✅ FINAL ANSWER:")
                print(content)
                
                # Check if sources are cited
                if "Source:" in content or ".pdf" in content or "Page" in content:
                    source_cited = True
        
        print(f"\n{'='*70}")
        print(f"📊 Test Results:")
        print(f"  - RAG Search Used: {'✅ YES' if rag_used else '❌ NO'}")
        print(f"  - Sources Cited: {'✅ YES' if source_cited else '❌ NO'}")
        print(f"  - Answer Length: {len(final_answer)} characters")
        
        if not rag_used:
            print("  ⚠️  WARNING: Agent did not use RAG search!")
        if not source_cited:
            print("  ⚠️  WARNING: Agent did not cite sources!")
        
        print('='*70)

if __name__ == "__main__":
    test_rag_usage()
