from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Iterable, List

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import FakeEmbeddings


def _default_doc_paths(root: Path) -> List[Path]:
    """Return the two expected Core PDFs when they exist."""
    candidates = [
        root / "Core" / "MPP SOP.pdf",
        root / "Core" / "Appendix I.pdf",
    ]
    return [path for path in candidates if path.exists()]


def _load_pdfs(paths: Iterable[Path]) -> List[Document]:
    """Load a list of PDFs into LangChain Documents."""
    docs: List[Document] = []
    for path in paths:
        loader = PyPDFLoader(str(path))
        docs.extend(loader.load())
    return docs


def _chunk_documents(docs: Iterable[Document]) -> List[Document]:
    """Split documents into overlapping chunks to improve recall."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=150,
        separators=["\n\n", "\n", ". ", " "],
    )
    return splitter.split_documents(docs)


def _persist_chunks(chunks: Iterable[Document], output_path: Path) -> None:
    """Persist chunk metadata for later BM25 loading."""
    payload = [
        {"page_content": doc.page_content, "metadata": doc.metadata or {}}
        for doc in chunks
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    load_dotenv()
    base_dir = Path(__file__).resolve().parents[1]  # .../Rag 2

    pdf_paths = _default_doc_paths(base_dir)
    if not pdf_paths:
        raise SystemExit(
            "No source PDFs found. Expected 'Core/MPP SOP.pdf' and 'Core/Appendix I.pdf' under Rag 2."
        )

    print("Building hybrid index from:")
    for path in pdf_paths:
        print(f" - {path}")

    raw_docs = _load_pdfs(pdf_paths)
    print(f"Loaded {len(raw_docs)} PDF pages.")

    chunks = _chunk_documents(raw_docs)
    print(f"Split into {len(chunks)} text chunks.")

    storage_dir = Path(__file__).resolve().parent / "storage"
    chroma_dir = storage_dir / "chroma"
    chroma_dir.mkdir(parents=True, exist_ok=True)

    force_fake = os.getenv("HYBRID_FORCE_FAKE", "0") == "1"
    use_fake = force_fake or not os.getenv("OPENAI_API_KEY")
    embeddings = (
        FakeEmbeddings(size=1536) if use_fake else OpenAIEmbeddings()
    )
    if use_fake:
        print("Warning: Using FakeEmbeddings (non-semantic). Set HYBRID_FORCE_FAKE=0 and OPENAI_API_KEY for real embeddings.")

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(chroma_dir),
    )
    vectordb.persist()
    print(f"Persisted vector index to {chroma_dir}")

    chunk_cache = storage_dir / "chunks.json"
    _persist_chunks(chunks, chunk_cache)
    print(f"Cached chunk metadata for BM25 at {chunk_cache}")


if __name__ == "__main__":
    main()
