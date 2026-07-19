import os
import shutil
import stat

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from clone import clone_repository
from parser import parse_repo
from chunker import chunk_repo
from embeddings import embed_chunks, model
from retrieval import build_index, save_index, load_index, search
from llm import ask_question



app = FastAPI()
templates = Jinja2Templates(directory="../templates")
app.mount("/static", StaticFiles(directory="../static"), name="static")

current_index = None
current_metadata = None
current_repo_name = None

def remove_readonly(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {})


import shutil

@app.post("/index")
def index_repo(repo_url: str = Form(...)):
    global current_index, current_metadata, current_repo_name

    try:
        repo_path = clone_repository(repo_url)
        if repo_path is None:
            return JSONResponse({"error": "Failed to clone repository. Check the URL and try again."}, status_code=400)

        parsed_files = parse_repo(repo_path)
        chunks = chunk_repo(parsed_files)
        embedded = embed_chunks(chunks)
        index, metadata = build_index(embedded)

        current_index = index
        current_metadata = metadata
        current_repo_name = repo_url.split("/")[-1].replace(".git", "")

        shutil.rmtree(repo_path, onerror=remove_readonly)

        return JSONResponse({
            "success": f"Indexed {current_repo_name} — {len(chunks)} chunks ready.",
            "repo_name": current_repo_name
        })
    except Exception as e:
        return JSONResponse({"error": f"Something went wrong: {str(e)}"}, status_code=500)

@app.post("/ask")
def ask(question: str = Form(...)):
    if current_index is None:
        return JSONResponse({"error": "No repository indexed yet. Please index a repo first."}, status_code=400)

    try:
        query_embedding = model.encode(question)
        retrieved = search(current_index, current_metadata, query_embedding, k=5)
        result = ask_question(question, retrieved)

        return JSONResponse({
            "question": question,
            "answer": result["answer"],
            "sources": result["sources"]
        })
    except Exception as e:
        return JSONResponse({"error": f"Something went wrong: {str(e)}"}, status_code=500)