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

def fixed_size_chunks(text: str,max_words=500,overlap=50):
    words=text.split()
    if len(words)<=max_words:
        return [text]
    chunks=[]
    start=0
    while start<len(words):
        end=start+max_words
        chunks.append(" ".join(words[start:end]))
        start=end-overlap
    return chunks

def chunk_document(pdf_path:str,source_file:str):
    results=[]
    for page_number,page_text in extract_pages(pdf_path):
        for section_title,section_text in split_into_sections(page_text):
            if not section_text.strip():
                continue
            for sub_chunk in fixed_size_chunks(section_text):
                results.append({
                    "source_file":source_file,
                    "page_number":page_number,
                    "section_title":section_title,
                    "content":sub_chunk.strip(),
                })
    return results

if __name__ == "__main__":
    import sys
    chunks = chunk_document(sys.argv[1], source_file=sys.argv[1].split("/")[-1])
    print(f"Total chunks: {len(chunks)}\n")
    for c in chunks:
        print(f"[{c['source_file']} | page {c['page_number']} | {c['section_title']}]")
        print(f"  {c['content'][:80]}...\n")