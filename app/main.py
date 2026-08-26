from fastapi import FastAPI
from db import init_db
app=FastAPI(title="Study Material Q&A Assistant")

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
async def root():
    return {"status": "running"}

