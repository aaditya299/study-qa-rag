import pymupdf
from sentence_transformers import SentenceTransformer
from db import Chunk,SessionLocal,init_db

model=SentenceTransformer("all-MiniLM-L6-v2")
