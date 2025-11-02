from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Iterable, List

from dotenv import load_dotenv
from langchain.chains import RetrievalQA
from langchain.retrievers import EnsembleRetriever
from langchain.schema import Document
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.llms.fake import FakeListLLM


def _load_chunks(path: Path) -> List[Document]:
    if not path.exists():
        raise FileNotFoundError(
            f"Chunk cache not found at {path}. Run 'python hybrid_rerank/ingest.py' first."
        )
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [
        Document(page_content=item["page_content"], metadata=item.get("metadata") or {})
        for item in payload
    ]


def _format_sources(docs: Iterable[Document]) -> str:
    lines: List[str] = []
    for idx, doc in enumerate(docs, start=1):
        meta = doc.metadata or {}
        source = Path(meta.get("source", "source")).name
        page = meta.get("page", "?")
        snippet = doc.page_content.replace("\n", " ").strip()
        if len(snippet) > 400:
            snippet = snippet[:397] + "..."
        lines.append(f"[Match {idx} | {source} | page {page}] {snippet}")
    return "\n".join(lines)


def _build_hybrid_retriever(base_dir: Path) -> EnsembleRetriever:
    storage_dir = base_dir / "hybrid_rerank" / "storage"
    chroma_dir = storage_dir / "chroma"
    if not chroma_dir.exists():
        raise FileNotFoundError(
            f"Chroma index not found at {chroma_dir}. Run 'python hybrid_rerank/ingest.py' first."
        )

    force_fake = os.getenv("HYBRID_FORCE_FAKE", "0") == "1"
    use_fake = force_fake or not os.getenv("OPENAI_API_KEY")
    embeddings = FakeEmbeddings(size=1536) if use_fake else OpenAIEmbeddings()
    vectordb = Chroma(
        persist_directory=str(chroma_dir),
        embedding_function=embeddings,
    )
    vector_retriever = vectordb.as_retriever(search_kwargs={"k": 6})

    chunks = _load_chunks(storage_dir / "chunks.json")
    bm25_retriever = BM25Retriever.from_documents(chunks)
    bm25_retriever.k = 6

    hybrid = EnsembleRetriever(
        retrievers=[vector_retriever, bm25_retriever],
        weights=[0.6, 0.4],
    )
    return hybrid


def _build_qa_chain(retriever: EnsembleRetriever) -> RetrievalQA:
    force_fake = os.getenv("HYBRID_FORCE_FAKE", "0") == "1"
    if os.getenv("OPENAI_API_KEY") and not force_fake:
        llm = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0,
        )
    else:
        responses = [
            "Offline mode response: review the provided context snippets for details."
        ] * 100
        llm = FakeListLLM(responses=responses)
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
    )


def main() -> None:
    load_dotenv()
    base_dir = Path(__file__).resolve().parents[1]  # .../Rag 2

    retriever = _build_hybrid_retriever(base_dir)
    qa_chain = _build_qa_chain(retriever)

    print("Hybrid Search + Rerank ready. Ask about the MPP Core documents.")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            query = input("You> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not query:
            continue
        if query.lower() in {"exit", "quit", ":q"}:
            print("Goodbye!")
            break

        try:
            result = qa_chain.invoke({"query": query})
        except Exception as exc:  # pragma: no cover - defensive path
            print(f"[error] {exc}")
            continue

        answer = result.get("result", "").strip()
        sources = result.get("source_documents") or []

        print(f"\nAssistant> {answer or '[no answer returned]'}\n")
        if sources:
            print("Context:")
            print(_format_sources(sources))
            print()


if __name__ == "__main__":
    main()
