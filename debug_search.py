
from duckduckgo_search import DDGS
import json

def test_search():
    queries = ["Tamil Nadu news", "groundwater Dindigul Tamil Nadu"]
    for q in queries:
        print(f"\n--- Testing Query: {q} ---")
        try:
            with DDGS() as ddgs:
                results = [r for r in ddgs.news(q, region='in-en', max_results=5)]
                print(f"Results found: {len(results)}")
                for r in results:
                    print(f"- {json.dumps(r)}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_search()
