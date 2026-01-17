"""
PDF Ingestion using IBM Docling for table-aware parsing
"""
import argparse
from pathlib import Path
from tqdm import tqdm

from docling.document_converter import DocumentConverter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import torch

from backend.config import (
    PDF_DIR,
    VECTORSTORE_DIR,
    EMBEDDING_MODEL,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)


def parse_pdf_with_docling(pdf_path: Path) -> str:
    """
    Parse a PDF using Docling, preserving table structure.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Markdown text with preserved table formatting
    """
    print(f"Parsing PDF: {pdf_path.name}")
    
    converter = DocumentConverter()
    result = converter.convert(str(pdf_path))
    
    # Export to Markdown (preserves tables)
    markdown_content = result.document.export_to_markdown()
    
    print(f"Extracted {len(markdown_content)} characters")
    return markdown_content


def create_chunks(text: str, source_name: str) -> list:
    """
    Split text into chunks while preserving context.
    
    Args:
        text: Full markdown text
        source_name: Name of source PDF for metadata
        
    Returns:
        List of document chunks with metadata
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "]
    )
    
    chunks = splitter.create_documents(
        texts=[text],
        metadatas=[{"source": source_name}]
    )
    
    # Add page estimation to metadata (rough approximation)
    chars_per_page = 3000
    for i, chunk in enumerate(chunks):
        estimated_page = (chunk.metadata.get("start", i * CHUNK_SIZE)) // chars_per_page + 1
        chunk.metadata["estimated_page"] = estimated_page
    
    print(f"Created {len(chunks)} chunks")
    return chunks


def build_vectorstore(chunks: list, persist_dir: Path = VECTORSTORE_DIR, merge_existing: bool = True):
    """
    Build FAISS vectorstore from document chunks.
    
    Args:
        chunks: List of document chunks
        persist_dir: Directory to save the index
        merge_existing: If True, merge with existing index instead of overwriting
    """
    print(f"Building vector store with {EMBEDDING_MODEL}...")
    
    # Use GPU if available for faster embedding
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": device}
    )
    
    # Check if existing vectorstore exists and merge_existing is True
    if merge_existing and persist_dir.exists() and any(persist_dir.iterdir()):
        print("Loading existing vector store for merging...")
        existing_store = FAISS.load_local(
            str(persist_dir),
            embeddings,
            allow_dangerous_deserialization=True
        )
        # Create new vectorstore from new chunks
        new_store = FAISS.from_documents(chunks, embeddings)
        # Merge new into existing
        existing_store.merge_from(new_store)
        vectorstore = existing_store
        print(f"Merged {len(chunks)} new chunks into existing index")
    else:
        vectorstore = FAISS.from_documents(chunks, embeddings)
    
    # Save to disk
    vectorstore.save_local(str(persist_dir))
    print(f"Vector store saved to {persist_dir}")
    
    return vectorstore


def ingest_pdf(pdf_path: Path):
    """
    Full ingestion pipeline: PDF -> Markdown -> Chunks -> Vectorstore
    """
    # Parse PDF
    markdown = parse_pdf_with_docling(pdf_path)
    
    # Create chunks
    chunks = create_chunks(markdown, pdf_path.name)
    
    # Build and save vectorstore
    vectorstore = build_vectorstore(chunks)
    
    print(f"\n✅ Successfully ingested: {pdf_path.name}")
    print(f"   Chunks created: {len(chunks)}")
    print(f"   Vector store: {VECTORSTORE_DIR}")
    
    return vectorstore


def ingest_all_pdfs():
    """Ingest all PDFs in the data/pdfs directory."""
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {PDF_DIR}")
        print("Please add CGWB/State groundwater reports to this directory.")
        return None
    
    all_chunks = []
    
    for pdf_path in tqdm(pdf_files, desc="Processing PDFs"):
        markdown = parse_pdf_with_docling(pdf_path)
        chunks = create_chunks(markdown, pdf_path.name)
        all_chunks.extend(chunks)
    
    # Build combined vectorstore
    vectorstore = build_vectorstore(all_chunks)
    
    print(f"\n✅ Ingested {len(pdf_files)} PDF files")
    print(f"   Total chunks: {len(all_chunks)}")
    
    return vectorstore


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CGWB PDF reports")
    parser.add_argument(
        "--pdf", 
        type=str, 
        help="Path to specific PDF file to ingest"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Ingest all PDFs in data/pdfs directory"
    )
    
    args = parser.parse_args()
    
    if args.pdf:
        ingest_pdf(Path(args.pdf))
    elif args.all:
        ingest_all_pdfs()
    else:
        print("Usage:")
        print("  python ingest.py --pdf <path_to_pdf>")
        print("  python ingest.py --all")
