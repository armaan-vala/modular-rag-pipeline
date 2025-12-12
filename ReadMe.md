


# SaaS-Agent: Modular RAG AI Pipeline

A production-ready, environment-agnostic AI pipeline that ingests documents, creates embeddings, and performs Retrieval-Augmented Generation (RAG) using Groq (Llama 3) and a decoupled vector store.

Built with **FastAPI**, **LangChain logic**, **ChromaDB**, and **Groq**.

## 📂 Project Structure
````markdown

├── src/
│   ├── ingestion.py       # Handles loading (PDF/TXT) & cleaning logic
│   ├── embedder.py        # Abstract wrapper for Embeddings (Local/OpenAI)
│   ├── vector_store.py    # Decoupled Store Interface (ChromaDB/Postgres)
│   ├── retriever.py       # Logic to find relevant document chunks
│   ├── answer_engine.py   # RAG Logic (Constructs Prompt + Calls LLM)
│   └── interfaces.py      # Abstract Base Classes (The Contracts)
├── static/                # Frontend UI (HTML/CSS/JS)
├── main.py                # FastAPI Service & Async Hooks
├── demo.ipynb             # Jupyter Notebook Demo
├── requirements.txt       # Dependencies
└── .env                   # Environment Variables

````

## 🚀 Setup & Installation

### 1\. Prerequisites

  * Python 3.9+
  * A [Groq API Key](https://console.groq.com/) (Free)

### 2\. Installation

Clone the repository and install dependencies:

```bash
git clone <repository-url>
cd saas-agent
pip install -r requirements.txt
```

### 3\. Environment Configuration

Create a `.env` file in the root directory:

```properties
# LLM Provider
GROQ_API_KEY="gsk_your_actual_api_key_here"

# Database (Optional if using local ChromaDB)
DATABASE_URL="postgresql://user:pass@localhost:5432/db"
```

-----

## 💻 Usage

### Option A: Web Interface (Recommended)

Launch the full-stack application with the Chat UI.

1.  **Start the Server:**
    ```bash
    uvicorn main:app
    ```
2.  **Open Browser:**
    Go to [http://127.0.0.1:8000](http://127.0.0.1:8000).
3.  **Interact:**
      * **Upload:** Select a PDF/TXT file on the left sidebar to ingest it.
      * **Chat:** Ask questions about the document on the right.

### Option B: API Endpoints (Swagger UI)

Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to test the raw API.

  * `POST /ingest`: Uploads and processes a file asynchronously.
  * `POST /query`: Asks a question to the RAG engine.
  * `GET /health`: Checks system status.

### Option C: Jupyter Notebook Demo

To see the Python logic running step-by-step without the server:

1.  Open `demo.ipynb` in VS Code or Jupyter Lab.
2.  Run the cells to Ingest, Retrieve, and Answer programmatically.

-----

## ⚙️ Customization & Architecture

This project follows the **Dependency Inversion Principle**. You can swap components without breaking the app.

### 1\. Changing the LLM

Modify `src/answer_engine.py`.

  * **Current:** Uses `GroqLLM` (Llama 3.1).
  * **To Change:** Implement the `BaseLLM` interface for OpenAI, Anthropic, or HuggingFace.

### 2\. Changing the Vector Store

Modify `src/vector_store.py`.

  * **Current:** Uses `ChromaDB` (Local file-based).
  * **To Change:** We have a preserved `pgvector` implementation for Postgres/Supabase. Simply uncomment the Postgres code and provide a `DATABASE_URL`.

### 3\. Changing Embeddings

Modify `src/embedder.py`.

  * **Current:** Uses `sentence-transformers/all-MiniLM-L6-v2` (Local/Free).
  * **To Change:** Switch to OpenAI Embeddings by updating the `embed` method.

-----




