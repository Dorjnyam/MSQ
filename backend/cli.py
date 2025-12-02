"""Command-line utilities for the MCQ generator backend."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import uuid

from app.services.registry import mcq_generator, pdf_processor


def ingest_pdf(pdf_path: Path, pdf_id: str | None, start_page: int | None, end_page: int | None):
    pdf_path = pdf_path.expanduser().resolve()
    if not pdf_path.exists():
        raise SystemExit(f"PDF not found: {pdf_path}")

    resolved_pdf_id = pdf_id or pdf_path.stem.replace(" ", "_") + f"_{uuid.uuid4().hex[:8]}"
    text, total_pages, (range_start, range_end) = pdf_processor.extract_text(
        pdf_path, page_start=start_page, page_end=end_page
    )
    metadata = {
        "title": pdf_path.name,
        "total_pages": total_pages,
        "ingested_range": f"{range_start}-{range_end}",
    }
    chunks = mcq_generator.process_pdf_to_rag(text, pdf_id=resolved_pdf_id, metadata=metadata)
    result = {
        "pdf_id": resolved_pdf_id,
        "total_pages": total_pages,
        "ingested_pages": f"{range_start}-{range_end}",
        "chunks_created": chunks,
    }
    return result


def process_command(args: argparse.Namespace):
    """Ingest a PDF into the RAG store."""
    result = ingest_pdf(
        pdf_path=Path(args.pdf),
        pdf_id=args.pdf_id,
        start_page=args.start_page,
        end_page=args.end_page,
    )
    print(json.dumps(result, indent=2))


def generate_command(args: argparse.Namespace):
    """Generate MCQs for an already ingested PDF."""
    mcqs = mcq_generator.generate_mcqs(
        pdf_id=args.pdf_id,
        page_start=args.page_start,
        page_end=args.page_end,
        num_questions=args.num_questions,
        difficulty=args.difficulty,
    )
    print(json.dumps({"total_generated": len(mcqs), "mcqs": mcqs}, indent=2, ensure_ascii=False))


def interactive_command(_args: argparse.Namespace):
    """Guided flow: ask for PDF, optional pages, question count, and difficulty."""
    print("=== Interactive MCQ Generator ===")
    pdf_path = Path(input("PDF path: ").strip())
    start_page_raw = input("Start page (leave blank for first page): ").strip()
    end_page_raw = input("End page (leave blank for last page): ").strip()
    num_questions_raw = input("How many questions? [default 10]: ").strip()
    difficulty_raw = input("Difficulty [easy|medium|hard, default medium]: ").strip().lower()

    start_page = int(start_page_raw) if start_page_raw else None
    end_page = int(end_page_raw) if end_page_raw else None
    num_questions = int(num_questions_raw) if num_questions_raw else 10
    difficulty = difficulty_raw if difficulty_raw in {"easy", "hard"} else "medium"

    ingest_result = ingest_pdf(pdf_path, pdf_id=None, start_page=start_page, end_page=end_page)
    print(json.dumps(ingest_result, indent=2))
    generated_pdf_id = ingest_result["pdf_id"]

    gen_args = argparse.Namespace(
        pdf_id=generated_pdf_id,
        page_start=start_page or 1,
        page_end=end_page or ingest_result["total_pages"],
        num_questions=num_questions,
        difficulty=difficulty,
    )
    generate_command(gen_args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="RAG-powered MCQ generator CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    ingest = sub.add_parser("process", help="Extract + chunk a PDF into the vector store")
    ingest.add_argument("--pdf", required=True, help="Path to the PDF file")
    ingest.add_argument("--pdf-id", help="Optional custom identifier for this PDF")
    ingest.add_argument("--start-page", type=int, help="Inclusive start page to ingest")
    ingest.add_argument("--end-page", type=int, help="Inclusive end page to ingest")
    ingest.set_defaults(func=process_command)

    generate = sub.add_parser("generate", help="Generate MCQs for an ingested PDF")
    generate.add_argument("--pdf-id", required=True, help="Identifier returned during processing")
    generate.add_argument("--page-start", type=int, required=True, help="Starting page number")
    generate.add_argument("--page-end", type=int, required=True, help="Ending page number")
    generate.add_argument("--num-questions", type=int, default=10, help="Number of MCQs to create")
    generate.add_argument(
        "--difficulty", choices=["easy", "medium", "hard"], default="medium", help="Question difficulty"
    )
    generate.set_defaults(func=generate_command)

    interactive = sub.add_parser("interactive", help="Prompt-driven flow (enter PDF path, pages, etc.)")
    interactive.set_defaults(func=interactive_command)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

