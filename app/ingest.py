import pymupdf
from sentence_transformers import SentenceTransformer
from db import Chunk,SessionLocal,init_db

model=SentenceTransformer("all-MiniLM-L6-v2")

def extract_pages(pdf_path:str):
    doc=pymupdf.open(pdf_path)
    for i,page in enumerate(doc,start=1):
        yield i,page.get_text()
    doc.close()

def looks_like_heading(line: str)->bool:
    stripped=line.strip()
    if not stripped or len(stripped)>80:
        return False
    return stripped.isupper() or stripped.istitle()

def split_into_sections(text:str):
    lines =text.split("\n")
    sections=[]
    current_title="Untitled section"
    current_lines=[]
    for line in lines:
        if looks_like_heading(line):
            if current_lines:
                sections.append((current_title,"\n".join(current_lines)))
            current_title=line.strip()
            current_lines=[]
        else:
            current_lines.append(line)
    
    if current_lines:
        sections.append((current_title,"\n".join(current_lines)))
    return sections

if __name__ == "__main__":
    import sys
    for page_num, text in extract_pages(sys.argv[1]):
        print(f"=== Page {page_num} ===")
        for title, body in split_into_sections(text):
            print(f"  [{title}] -> {body[:80]}...")
