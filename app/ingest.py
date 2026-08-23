import pymupdf
from sentence_transformers import SentenceTransformer
from db import Chunk,SessionLocal,init_db

model=SentenceTransformer("all-MiniLM-L6-v2")

def extract_pages(pdf_path:str):
    doc=pymupdf.open(pdf_path)
    for i,page in enumerate(doc,start=1):
        yield i,page.get_text()
    doc.close()

if __name__ == "__main__":
    import sys
    for page_num, text in extract_pages(sys.argv[1]):
        print(f"--- Page {page_num} ---")
        print(text[:200])  