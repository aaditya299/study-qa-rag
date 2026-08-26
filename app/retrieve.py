import os
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from google import genai
from db import Chunk, SessionLocal
load_dotenv()
model=SentenceTransformer("all-MiniLM-L6-v2")
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
GEMINI_MODEL="gemini-2.0-flash"

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
    
if __name__ == "__main__":
    import sys
    results = retrieve_chunks(sys.argv[1])
    for r in results:
        print(f"[{r.source_file} | page {r.page_number} | {r.section_title}]")
        print(f"  {r.content[:100]}...\n")
        