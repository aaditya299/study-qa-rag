from fastapi import FastAPI,UploadFile,File
from db import init_db
from ingest import ingest_pdf
from pydantic import BaseModel
from retrieve import answer_question
import shutil
import tempfile
import os

app=FastAPI(title="Study Material Q&A Assistant")

class AskRequest(BaseModel):
    question:str
    top_k:int =5

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
async def root():
    return {"status": "running"}

@app.post("/upload")
async def upload_pdf(file: UploadFile=File(...)):
    with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as tmp:
        shutil.copyfileobj(file.file,tmp)
        tmp_path=tmp.name
    try:
        ingest_pdf(tmp_path,source_file=file.filename)
    finally:
        os.remove(tmp_path)
    return {"status":"ok","filename":file.filename}

@app.post("/ask")
async def ask (request:AskRequest):
    result=answer_question(request.question,top_k=request.top_k)
    return result