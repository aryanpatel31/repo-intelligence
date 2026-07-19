from sentence_transformers import SentenceTransformer
from typing import List, Dict

model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks: List[Dict]) -> List[Dict]:
    texts = [chunk["text"] for chunk in chunks]

    #single batched call
    embeddings = model.encode(texts, show_progress_bar = True)

    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding

    return chunks

