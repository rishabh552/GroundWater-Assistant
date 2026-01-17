from backend.retriever import get_retriever

def debug():
    print("🔍 Loading Retriever...")
    retriever = get_retriever()
    
    # Test queries based on recent context
    queries = [
        "Chennai groundwater status",
        "Can I drill borewells in Chennai?",
        "groundwater regulations in Chennai"
    ]
    
    for q in queries:
        print(f"\n──────────────────────────────────────────────────")
        print(f"🔎 Query: {q}")
        print(f"──────────────────────────────────────────────────")
        
        # Search with higher K to see what we are missing
        results = retriever.search(q, k=10)
        
        for i, (doc, score) in enumerate(results):
            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("estimated_page", "?")
            # score is L2 distance for FAISS usually (lower is better), or similarity (higher is better)
            # FAISS default is L2 distance.
            print(f"\n[{i+1}] Score: {score:.4f} | Source: {source} (Page {page})")
            content_preview = doc.page_content[:200].replace('\n', ' ')
            print(f"Content snippet: {content_preview}...")
            
if __name__ == "__main__":
    debug()
