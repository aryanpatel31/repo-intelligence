# Repository Intelligence Platform

Paste a public GitHub repo, ask questions about it in plain English, get answers grounded in the actual code — not just an LLM guessing from its training data.

## How it works

```
GitHub URL
    │
Clone repository (GitPython)
    │
Parse & filter source files (.py, .js, .ts, .md, etc.)
    │
Chunk code into overlapping, line-safe segments
    │
Generate embeddings (sentence-transformers, all-MiniLM-L6-v2)
    │
Build FAISS vector index
    │
User asks a question
    │
Embed question → retrieve top-k relevant chunks (FAISS)
    │
Gemini generates an answer using only the retrieved code
```

## Stack

- **Backend:** FastAPI
- **Repo handling:** GitPython
- **Embeddings:** sentence-transformers (`all-MiniLM-L6-v2`)
- **Vector search:** FAISS (`IndexFlatIP`, cosine similarity via normalized vectors)
- **LLM:** Gemini API (`google-genai`)
- **Frontend:** Jinja2 templates + vanilla JS, no framework

## Repo structure

```
repo-intelligence/
│
├── app/
│   ├── main.py              # FastAPI routes, wires the whole pipeline together
│   ├── clone.py              # Clones a GitHub repo locally
│   ├── parser.py             # Walks the repo, filters + reads source files
│   ├── chunker.py            # Splits file contents into overlapping chunks
│   ├── embeddings.py         # Generates embeddings with sentence-transformers
│   ├── retrieval.py          # Builds/saves/loads/searches the FAISS index
│   ├── llm.py                # Sends retrieved context + question to Gemini
│   └── config.py             # Loads the Gemini API key from .env
│
├── repositories/             # Cloned repos land here temporarily, deleted after indexing
├── vector_store/             # Saved FAISS indexes (gitignored)
│
├── templates/
│   └── index.html            # Single-page UI
│
├── static/
│   ├── style.css
│   └── script.js
│
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup

```bash
conda create -n repo-intelligence python=3.12
conda activate repo-intelligence
pip install -r requirements.txt
```

Get a free Gemini API key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey) — no credit card needed.

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_key_here
```

Run it:
```bash
cd app
uvicorn main:app --reload
```

Open `http://127.0.0.1:8000`, paste a repo URL, hit Index, then ask away.

## A few implementation notes

**Chunking snaps to line boundaries.** Naive fixed-size chunking will cut a function definition in half if it happens to land on a boundary. Chunks here cap at ~1500 characters but always break on a full line, with ~200 characters of overlap between adjacent chunks so nothing important gets orphaned at a boundary.

**FAISS metadata lives outside the index.** FAISS only stores raw vectors — it doesn't know about file paths or source text. A separate pickled list tracks that mapping by position: index position `i` in FAISS corresponds to position `i` in the metadata list.

**Model is `gemini-flash-latest`, not pinned.** Two Gemini model names got deprecated mid-build (`gemini-2.5-flash`, then `gemini-2.5-flash-lite`). Using Google's auto-updating alias means the app doesn't break the next time a model generation gets retired.

**Cloned repos get deleted after indexing.** Once the content's embedded into FAISS, the raw clone isn't needed anymore — deleting it keeps disk usage from growing unbounded as more repos get indexed.

## Not included (yet)

- Single repo indexed at a time, no persistence across restarts
- No architecture summary / dependency graph / per-file summaries
- No Docker setup

## Screenshots

coming soon...