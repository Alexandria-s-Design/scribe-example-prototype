# MPP 2 – Hybrid Search + Rerank

This folder provides a lightweight retrieval workflow focused on the two core MPP PDFs found under `Rag 2/Core`. It combines dense vector search with classical keyword search and applies reciprocal-rank fusion to re-rank the merged results before answering with an OpenAI model.

## What it does
- Indexes `MPP SOP.pdf` and `Appendix I.pdf` from `Rag 2/Core`.
- Builds a Chroma vector store (OpenAI embeddings).
- Stores chunk metadata so a BM25 retriever can be rebuilt quickly.
- Answers questions via an interactive console app using a hybrid (vector + BM25) retriever with reciprocal-rank reranking.
- Falls back to local fake embeddings and responses when `OPENAI_API_KEY` is unset (or `HYBRID_FORCE_FAKE=1`) so you can smoke-test without external calls.

## Prerequisites
- Python 3.10+ available as `python`.
- An OpenAI-compatible API key (`OPENAI_API_KEY`).
- (Optional) set `OPENAI_MODEL` if you want something other than `gpt-4o-mini`.

## Setup
1. (Optional) create and activate a virtual environment.
2. Install dependencies:
   ```pwsh
   python -m pip install -r Rag 2/hybrid_rerank/requirements.txt
   ```
3. Copy `.env.example` to `.env` (or export the variables another way) and set `OPENAI_API_KEY` (and optionally `OPENAI_MODEL`).
4. Run the ingestion step once to build the stores (set `HYBRID_FORCE_FAKE=1` if you want to force offline mode):
   ```pwsh
   python Rag 2/hybrid_rerank/ingest.py
   ```
5. Start the hybrid search CLI:
   ```pwsh
   python Rag 2/hybrid_rerank/main.py
   ```

If you move or rename the PDFs, edit `ingest.py` (function `_default_doc_paths`) to point to the new locations before rebuilding the index.
