from typing import List, Dict
from pathlib import Path

def chunk_file(file_path: str, contents: str, chunk_size: int = 1500, overlap: int = 200) -> List[Dict]:

    lines = contents.splitlines(keepends = True)

    chunks = []
    current_chunk = ""
    current_lines_start = 0

    i = 0
    while i < len(lines):
        line = lines[i]

        if len(current_chunk) + len(line) > chunk_size and current_chunk:
            chunks.append({
                "file_path" : file_path,
                "text" : current_chunk,
            })

            #overlap
            #walking back from end of current_chunk for ~overlap chars, snapping to line breaks
            overlap_text = ""
            back_lines = current_chunk.splitlines(keepends = True)
            j = len(back_lines) - 1

            while j >= 0 and len(overlap_text) < overlap:
                overlap_text = back_lines[j] + overlap_text
                j -= 1
            
            current_chunk = overlap_text

        else:
            current_chunk += line
            i += 1
        
    if current_chunk:
        chunks.append({
            "file_path": file_path,
            "text" : current_chunk,
        })
    
    return chunks

def chunk_repo(parsed_files: List[tuple], chunk_size: int = 1500, overlap: int = 200):

    all_chunks = []

    for file_path, contents in parsed_files:
        all_chunks.extend(chunk_file(file_path, contents, chunk_size, overlap))
    
    return all_chunks

