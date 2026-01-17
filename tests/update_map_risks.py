import json
import os
from tqdm import tqdm

from backend.map_utils import LOCATIONS, RISK_COLORS
from backend.retriever import GroundwaterRetriever
from backend.llm import load_model, generate_response

# Output file
OUTPUT_FILE = "generated_map_data.json"

def get_risk_level(district, retriever, model_tuple):
    """
    Queries the RAG system to find the risk level for a district.
    """
    # Try multiple query variations for better retrieval
    queries = [
        f"{district} groundwater category",
        f"{district} District groundwater status",
        f"groundwater extraction {district}"
    ]
    
    all_docs = []
    for query in queries:
        docs = retriever.search(query, k=3)
        all_docs.extend(docs)
    
    if not all_docs:
        return "Unknown"
    
    # Deduplicate and get top content
    seen_content = set()
    unique_docs = []
    for doc, score in all_docs:
        content_hash = hash(doc.page_content[:100])
        if content_hash not in seen_content:
            seen_content.add(content_hash)
            unique_docs.append(doc.page_content)
    
    context = "\n---\n".join(unique_docs[:5])
    
    # More specific prompt with examples
    prompt = f"""Analyze the groundwater data below and classify {district} District into ONE category.

Categories:
- Safe (extraction < 70%)
- Semi-Critical (extraction 70-90%)  
- Critical (extraction 90-100%)
- Over-Exploited (extraction > 100%)
- Saline (high salinity)

Context:
{context[:3000]}

Answer with ONLY the category name (Safe, Semi-Critical, Critical, Over-Exploited, or Saline).
If {district} is not mentioned or data is unclear, answer: Unknown

Category for {district}:"""
    
    response = generate_response(model_tuple, prompt)
    answer = response.strip().split('\n')[0].strip()  # Get first line only
    
    # Extended matching with common variations
    answer_lower = answer.lower()
    
    # Check for each category with multiple keywords
    if any(kw in answer_lower for kw in ['over-exploited', 'overexploited', 'over exploited', '>100', 'exceeds']):
        return "Over-Exploited"
    elif any(kw in answer_lower for kw in ['critical', 'high risk', '90-100', '90%']):
        if 'semi' not in answer_lower:
            return "Critical"
    if any(kw in answer_lower for kw in ['semi-critical', 'semicritical', 'semi critical', 'moderate', '70-90']):
        return "Semi-Critical"
    elif any(kw in answer_lower for kw in ['safe', 'low risk', '<70', 'sustainable']):
        return "Safe"
    elif any(kw in answer_lower for kw in ['saline', 'salinity', 'brackish']):
        return "Saline"
    
    # Fallback: check for percentage in answer to infer category
    import re
    percentage_match = re.search(r'(\d+)%', answer)
    if percentage_match:
        pct = int(percentage_match.group(1))
        if pct > 100:
            return "Over-Exploited"
        elif pct >= 90:
            return "Critical"
        elif pct >= 70:
            return "Semi-Critical"
        else:
            return "Safe"
            
    return "Unknown"

def main():
    print("🗺️  Starting RAG-based Map Update...")
    print("    This will query the Vector Database for every district.")
    
    # Load Components
    print("Loading Retriever...")
    retriever = GroundwaterRetriever()
    try:
        retriever.load()
    except Exception as e:
        print(f"Error loading retriever: {e}")
        return

    print("Loading LLM...")
    model_tuple = load_model()
    
    updated_locations = LOCATIONS.copy()
    
    # Iterate
    print(f"Processing {len(LOCATIONS)} districts...")
    for district in LOCATIONS.keys():
        print(f"  > Checking {district}...", end="", flush=True)
        risk = get_risk_level(district, retriever, model_tuple)
        print(f" [{risk}]")
        
        updated_locations[district]["risk"] = risk
        
    # Save
    with open(OUTPUT_FILE, "w") as f:
        json.dump(updated_locations, f, indent=4)
        
    print(f"\n✅ Map Data Updated! Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
