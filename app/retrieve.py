import os
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from google import genai
from db import Chunk, SessionLocal
load_dotenv()
model=SentenceTransformer("all-MiniLM-L6-v2")
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
GEMINI_MODEL="gemini-3.6-flash"

def retrieve_chunks(query:str,top_k:int=5):
    db=SessionLocal()
    try:
        query_embedding=model.encode(query).tolist()
        results=(
            db.query(Chunk)
            .order_by(Chunk.embedding.cosine_distance(query_embedding))
            .limit(top_k)
            .all()
        )
        return results
    finally:
        db.close()

def build_prompt(query:str,chunks: list[Chunk])->str:
    context_blocks=[]
    for c in chunks:
        location=f"{c.source_file}, page {c.page_number}, section: {c.section_title}"
        context_blocks.append(f"[{location}]\n{c.content}")
    context="\n\n---\n\n".join(context_blocks)
    return f"""You are a study assistant. Answer the question using ONLY the context below.
        If the answer isn't in the context, say so clearly instead of guessing.
        Cite the source (file, page, section) for each claim you make.
        
        Context:
        {context}

        Question: {query}

        Answer:"""
    
def answer_question(query:str, top_k:int=5)->dict:
    chunks=retrieve_chunks(query,top_k)
    if not chunks:
        return {"answer": "No study material has been ingested yet.", "sources": []}
    prompt=build_prompt(query,chunks)
    response=client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )
    sources= [
        {
            "source_file":c.source_file,
            "page_number":c.page_number,
            "section_title":c.section_title,
        }
        for c in chunks
    ]
    return {"answer":response.text, "sources":sources}

if __name__ == "__main__":
    import sys
    result = answer_question(sys.argv[1])
    print("ANSWER:\n", result["answer"])
    print("\nSOURCES:")
    for s in result["sources"]:
        print(" -", s)