import faiss
import numpy as np
import pickle
from typing import List, Dict, Tuple

def build_index(embedded_chunks: List[Dict]) -> Tuple[faiss.Index, List[Dict]]:
    
    #stacking embedding vectors into one 2D array (num_chunks, 384), faiss requires float32
    vectors = np.array([chunk["embedding"] for chunk in embedded_chunks]).astype("float32")

    faiss.normalize_L2(vectors)

    dimension = vectors.shape[1]
    index = faiss.IndexFlatIP(dimension)
    index.add(vectors)

    return index, embedded_chunks

def save_index(index: faiss.Index, metadata: List[Dict], index_path : str, metadata_path: str) -> None:

    faiss.write_index(index, index_path)

    with open (metadata_path, "wb") as f:
        pickle.dump(metadata, f)

def load_index(index_path: str, metadata_path: str) -> Tuple[faiss.Index, List[Dict]]:
    
    index = faiss.read_index(index_path)

    with open (metadata_path, "rb") as f:
        metadata = pickle.load(f)

    return index, metadata

def search(index: faiss.Index, metadata: List[Dict], query_embedding: np.ndarray, k: int = 5) -> List[Dict]:
    
    query_vector = np.array([query_embedding]).astype("float32")
    faiss.normalize_L2(query_vector)

    distances, indices = index.search(query_vector, k)

    res = []
    for idx, score in zip(indices[0], distances[0]):
        if idx == -1: #faiss returns -1 if fewer than k results
            continue
            
        chunk = metadata[idx]
        res.append({
            "file_path" : chunk["file_path"],
            "text" : chunk["text"],
            "score" : float(score)
        })

    return res
