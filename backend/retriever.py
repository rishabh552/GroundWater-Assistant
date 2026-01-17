"""
Retriever module for semantic search over groundwater documents
"""
from pathlib import Path
import torch
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from backend.config import VECTORSTORE_DIR, EMBEDDING_MODEL, TOP_K_RESULTS


class GroundwaterRetriever:
    """Retriever for searching block-level groundwater data."""
    
    def __init__(self, vectorstore_path: Path = VECTORSTORE_DIR):
        """
        Initialize the retriever with a pre-built vectorstore.
        
        Args:
            vectorstore_path: Path to the FAISS index directory
        """
        self.vectorstore_path = vectorstore_path
        # Use CPU for embeddings to avoid VRAM conflicts with LLM
        # The embedding model is small (~90MB) and fast on CPU
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"}
        )
        self.vectorstore = None
        
    def load(self):
        """Load the vectorstore from disk."""
        if not self.vectorstore_path.exists():
            raise FileNotFoundError(
                f"Vector store not found at {self.vectorstore_path}. "
                "Please run 'python ingest.py' first."
            )
        
        self.vectorstore = FAISS.load_local(
            str(self.vectorstore_path),
            self.embeddings,
            allow_dangerous_deserialization=True
        )
        print(f"Loaded vector store from {self.vectorstore_path}")
        
    def search(self, query: str, k: int = TOP_K_RESULTS) -> list:
        """
        Search for relevant documents based on query.
        
        Args:
            query: User's question (e.g., "Status of Sankarapuram block")
            k: Number of results to return
            
        Returns:
            List of (document, score) tuples
        """
        if self.vectorstore is None:
            self.load()
            
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        return results
    
    def format_context(self, results: list) -> str:
        """
        Format search results into a context string for the LLM.
        
        Args:
            results: List of (document, score) tuples
            
        Returns:
            Formatted context string with sources
        """
        if not results:
            return "No relevant data found in documents."
        
        context_parts = []
        
        for idx, (doc, score) in enumerate(results, 1):
            source = doc.metadata.get("source", "Unknown")
            page = doc.metadata.get("estimated_page", "?")
            
            # Add relevance indicator for very good matches
            relevance_note = " (High Relevance)" if score < 0.5 else ""
            
            # Format the document content with clear structure
            content = doc.page_content.strip()
            
            context_parts.append(
                f"=== DOCUMENT {idx}{relevance_note} ===\n"
                f"📄 Source: {source}\n"
                f"📍 Page: ~{page}\n"
                f"🎯 Relevance Score: {score:.3f}\n"
                f"\nCONTENT:\n{content}\n"
            )
        
        header = (
            f"RETRIEVED DATA FROM KNOWLEDGE BASE ({len(results)} documents found):\n" 
            + "="*70 + "\n\n"
        )
        
        footer = (
            "\n" + "="*70 + 
            "\n\n⚠️ IMPORTANT: In your Final Answer, you MUST:\n"
            "1. Provide a natural, conversational response first\n"
            "2. Then add a '📊 Retrieved Data from Reports' section\n"
            "3. Include specific water levels, percentages, classifications found above\n"
            "4. Cite the source document and page number for each piece of data\n"
        )
        
        return header + "\n".join(context_parts) + footer


def get_retriever() -> GroundwaterRetriever:
    """Factory function to get a loaded retriever instance."""
    retriever = GroundwaterRetriever()
    retriever.load()
    return retriever


# Test retrieval when run directly
if __name__ == "__main__":
    print("Testing retriever...")
    
    try:
        retriever = get_retriever()
        
        test_query = "What is the groundwater status of Sankarapuram block?"
        print(f"\nTest query: {test_query}")
        
        results = retriever.search(test_query)
        
        if results:
            print(f"\nFound {len(results)} results:")
            for doc, score in results:
                print(f"\n[Score: {score:.3f}]")
                print(f"Source: {doc.metadata.get('source', 'Unknown')}")
                print(f"Content: {doc.page_content[:200]}...")
        else:
            print("No results found.")
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
