import sys
import asyncio
import os
import shutil
import logging
from typing import List

# --- FIX FOR WINDOWS & ASYNCPG (MUST BE AT THE VERY TOP) ---
# This forces Windows to use the correct event loop for database connections
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# -----------------------------------------------------------

from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Import our modular components
from src.ingestion import IngestionEngine, TextChunker
from src.embedder import Embedder
from src.vector_store import VectorStore
from src.answer_engine import AnswerEngine

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Load environment variables (from .env)
load_dotenv()

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AI_Pipeline")

app = FastAPI(title="SaaS-Agent AI Pipeline")

# --- SERVE FRONTEND ---
# This mounts the "static" folder to the root URL
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")
# ----------------------

# --- Initialize Components ---
ingestion_engine = IngestionEngine()
text_chunker = TextChunker() 
embedder = Embedder()        
vector_store = VectorStore() 
answer_engine = AnswerEngine()

# --- Data Models ---
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[str]

# --- Async Worker Hook (The "Celery-Style" Pattern) ---
async def process_file_background(file_path: str, filename: str):
    """
    This function acts as the 'Worker'. 
    In the future, you can move this logic to Celery/Redis easily.
    """
    try:
        logger.info(f"Starting background processing for: {filename}")
        
        # 1. Ingest (Load & Clean)
        raw_docs = ingestion_engine.load_file(file_path)
        logger.info(f"Loaded {len(raw_docs)} raw documents from {filename}")
        
        # 2. Chunking
        chunked_docs = text_chunker.chunk_documents(raw_docs)
        logger.info(f"Created {len(chunked_docs)} chunks")
        
        if not chunked_docs:
            logger.warning("No text extracted. Stopping.")
            return

        # 3. Embedding (Heavy Compute)
        texts = [doc.content for doc in chunked_docs]
        vectors = embedder.embed(texts)
        logger.info(f"Generated {len(vectors)} vector embeddings")
        
        # 4. Store in Vector DB (Supabase)
        await vector_store.add_documents(chunked_docs, vectors)
        logger.info(f"Successfully stored data for {filename}")

    except Exception as e:
        logger.error(f"Error processing {filename}: {str(e)}")
    finally:
        # Cleanup temp file
        if os.path.exists(file_path):
            os.remove(file_path)

# --- Endpoints ---

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "SaaS-Agent Pipeline"}

@app.post("/ingest")
async def ingest_document(
    background_tasks: BackgroundTasks, 
    file: UploadFile = File(...)
):
    """
    Uploads a document (PDF, TXT, DOCX) and starts processing in the background.
    """
    # 1. Save file temporarily
    temp_dir = "temp_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    temp_path = os.path.join(temp_dir, file.filename)
    
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # 2. Trigger the "Async Hook"
    background_tasks.add_task(process_file_background, temp_path, file.filename)
    
    return {"message": "File received. Processing started in background.", "filename": file.filename}

@app.post("/query", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest):
    """
    Ask a question to the RAG system.
    """
    answer = await answer_engine.answer(request.query)
    
    return {
        "answer": answer,
        "sources": ["Source tracking not implemented in this MVP response"] 
    }