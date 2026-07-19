from google import genai
from config import GEMINI_API_KEY
from typing import List, Dict

client = genai.Client(api_key=GEMINI_API_KEY)

def build_prompt(question: str, retrieved_chunks: List[Dict]) -> str:

    context_blocks = []
    for chunk in retrieved_chunks:
        context_blocks.append(f"File: {chunk['file_path']}\n{chunk['text']}")

    context = "\n\n---\n\n".join(context_blocks)

    prompt = f"""You are a code assistant helping a developer understand a codebase.
                 Use ONLY the following code context to answer the question. If the context
                 doesn't contain enough information to answer, say so, DO NOT make things up.

                 CONTEXT:
                 {context}

                 QUESTION:
                 {question}

                 ANSWER:"""

    return prompt

def ask_question(question: str, retrieved_chunks: List[Dict]) -> Dict:
    
    prompt = build_prompt(question, retrieved_chunks)

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )

    sources = list(set(chunk["file_path"] for chunk in retrieved_chunks))

    return {
        "answer" : response.text,
        "sources" : sources,
    }