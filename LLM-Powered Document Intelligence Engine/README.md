# LLM-Powered Document Intelligence Engine

This project is an interview-ready document intelligence platform built with FastAPI, SQLAlchemy, and a lightweight RAG-style query flow.

## Features
- PDF / DOCX / TXT upload handling
- Authentication and user registration
- Document retrieval and query endpoint
- SQLite-backed storage for demo use
- Docker deployment support

## Run locally
1. Create and activate a virtual environment.
2. Install dependencies:
   python -m pip install -r requirements.txt
3. Start the API:
   python -m uvicorn app.main:app --reload
4. Open the API docs at http://127.0.0.1:8000/docs

## Run with Docker
1. docker compose up --build
2. Open http://localhost:8000/docs

## Test
python -m pytest -vv

## Interview summary
This project demonstrates backend APIs, authentication, storage, document processing, retrieval logic, testing, and containerized deployment for a junior-to-mid software engineer portfolio.
