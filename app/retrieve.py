import os
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from google import genai
from db import Chunk, SessionLocal
load_dotenv()
model=SentenceTransformer("all-MiniLM-L6-v2")
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
GEMINI_MODEL="gemini-2.0-flash"