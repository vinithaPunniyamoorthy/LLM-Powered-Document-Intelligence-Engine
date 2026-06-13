from fastapi import FastAPI

from app.api import admin, auth, document, query
from app.database.db import init_db

init_db()

app = FastAPI(title="LLM-Powered Document Intelligence Engine")

app.include_router(auth.router)
app.include_router(document.router)
app.include_router(query.router)
app.include_router(admin.router)


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok", "service": "llm-document-intelligence-engine"}
