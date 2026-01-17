"""CLI wrapper to run the ingestion pipeline from the project root."""
import argparse
from pathlib import Path

from backend.ingest import ingest_pdf, ingest_all_pdfs


def main():
    parser = argparse.ArgumentParser(description="Ingest CGWB PDF reports")
    parser.add_argument(
        "--pdf",
        type=str,
        help="Path to specific PDF file to ingest",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Ingest all PDFs in data/pdfs directory",
    )

    args = parser.parse_args()

    if args.pdf:
        ingest_pdf(Path(args.pdf))
    elif args.all:
        ingest_all_pdfs()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
