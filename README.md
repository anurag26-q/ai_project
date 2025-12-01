# RAG-Powered Chatbot for Transactional Data

A production-ready **Retrieval-Augmented Generation (RAG) chatbot** built with **FastAPI** and **LangChain** that answers natural language questions about customer transactional data.

## 🎯 Features

- ✅ **RAG Pipeline** using LangChain with vector similarity search
- ✅ **ChromaDB** vector database for embedding storage
- ✅ **FastAPI** backend with RESTful API endpoints
- ✅ **Streamlit** web UI with interactive chat interface
- ✅ **Analytics Dashboard** with spending charts and insights
- ✅ **Conversation Memory** to track chat history
- ✅ **Transaction Retrieval** with top-k similarity matching

## 🏗️ Architecture

```
├── transactions.json          # Sample transaction data
├── main.py                    # FastAPI application entry point
├── streamlit_app.py           # Streamlit UI launcher
├── requirements.txt           # Python dependencies
├── requirements_streamlit.txt # Streamlit-specific dependencies
├── .env.example               # Environment variables template
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile                 # FastAPI Docker image
├── Dockerfile.streamlit       # Streamlit Docker image
└── src/
    ├── data_loader.py         # Transaction data loading & preprocessing
    ├── vector_store.py        # ChromaDB vector store management
    ├── rag_chain.py          # LangChain RAG pipeline
    └── api/
        ├── schemas.py        # Pydantic models
        └── routes.py         # FastAPI endpoints
```

## 📦 Installation

### Prerequisites

- Python 3.9+ (for local installation)
- **OR** Docker Desktop (for Docker installation)
- Google API key for Gemini models

### Setup Steps

1. **Clone or navigate to the project directory:**
   ```bash
   cd f:\ai_project
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Already exists at f:\ai_project\venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   # Copy the example file
   copy .env.example .env
   
   # Edit .env and add your Google API key
   # GOOGLE_API_KEY=your-google-api-key-here
   ```

## 🚀 Usage

### Option A: Docker (Recommended)

**Easiest way to get started!**

```bash
# 1. Create .env file
copy .env.example .env
# Edit .env and add your GOOGLE_API_KEY

# 2. Start with Docker Compose
docker-compose up --build
```

Then access:
- **Streamlit UI**: http://localhost:8501
- **FastAPI Docs**: http://localhost:8000/docs

See [DOCKER.md](DOCKER.md) for detailed Docker instructions.

---

### Option B: Local Installation

### Option 1: FastAPI Backend

Start the FastAPI server:

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**API Endpoints:**

- **Interactive Docs:** http://localhost:8000/docs
- **Health Check:** `GET http://localhost:8000/health`
- **Get Transactions:** `GET http://localhost:8000/transactions`
- **Chat:** `POST http://localhost:8000/chat`

**Example API Request:**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is Amit'\''s total spending?"}'
```

**Example Response:**

```json
{
  "answer": "Amit spent a total of ₹55,700.",
  "sources": [
    {"id": 1, "customer": "Amit", "product": "Laptop", "amount": 55000, "date": "2024-01-12"},
    {"id": 2, "customer": "Amit", "product": "Mouse", "amount": 700, "date": "2024-02-15"}
  ],
  "query": "What is Amit's total spending?"
}
```

### Option 2: Streamlit Web UI

Launch the interactive Streamlit interface:

```bash
streamlit run streamlit_app.py
```

Access the UI at: http://localhost:8501

**UI Features:**
- 💬 **Main Chat:** Interactive conversation with the bot
- 📊 **Sidebar Analytics:** Real-time visualizations of spending patterns
- 📋 **Transaction Metrics:** Summary statistics and totals
- 🕒 **Memory Panel:** Last question tracking and chat clearing
- ✅ **API Health Check:** Automatic backend connectivity monitoring

## 🧪 Testing

### Test Data Loader

```bash
python -m src.data_loader
```

### Test Vector Store

```bash
python -m src.vector_store
```

### Test RAG Chain

```bash
python -m src.rag_chain
```

## 📝 Assignment Requirements

### ✅ Completed Tasks

1. **Load & Preprocess Transactional Data**
   - ✅ Implemented in `src/data_loader.py`
   - ✅ Converts transactions to descriptive text

2. **Create Embeddings**
   - ✅ Uses Google Gemini `text-embedding-004`
   - ✅ Managed by `src/vector_store.py`

3. **Implement Similarity-Based Retriever**
   - ✅ `retrieve_transactions()` function
   - ✅ Top-k cosine similarity search via ChromaDB

4. **Build the Chatbot Logic**
   - ✅ RAG pipeline in `src/rag_chain.py`
   - ✅ LangChain RetrievalQA chain
   - ✅ Context-aware responses using Google Gemini

5. **Expected Interactions**
   - ✅ All example queries work correctly

### 🎁 Bonus Features Implemented

- ✅ **Streamlit UI** with modern interface
- ✅ **Analytics Dashboard** with Plotly charts:
  - Customer spending bar chart
  - Monthly spending trend
  - Transaction summary metrics
- ✅ **Conversation Memory** (last question tracking)
- ✅ **Docker Support** with multi-container setup

## 🎓 Example Interactions

**User:** Show me Riya's purchase history.

**Bot:** Riya made two purchases: a Mobile for ₹30,000 on 2024-01-05 and Earbuds for ₹1,500 on 2024-02-20.

---

**User:** What is Amit's total spending?

**Bot:** Amit spent a total of ₹55,700.

---

**User:** Which product was purchased most often?

**Bot:** Based on the available transactions, each product appears only once, so there's no single most popular product. However, the products purchased include Laptop, Mouse, Mobile, Earbuds, and Keyboard.

## 🔧 Configuration

Edit `.env` to customize:

```env
# Google Gemini API Configuration
GOOGLE_API_KEY=your-google-api-key-here

# LLM Configuration
LLM_MODEL=gemini-2.5-flash
EMBEDDING_MODEL=models/text-embedding-004
TEMPERATURE=0                         # 0 = deterministic

# Retrieval Configuration
TOP_K_RESULTS=3                       # Number of similar transactions to retrieve

# Vector Store
VECTOR_DB_PATH=./chroma_db
COLLECTION_NAME=transactions
```

## 🛠️ Technology Stack

- **FastAPI** - Modern Python web framework
- **LangChain** - RAG framework for LLM applications
- **ChromaDB** - Vector database for embeddings
- **Google Gemini** - Embeddings (text-embedding-004) and chat (gemini-2.5-flash)
- **Streamlit** - Web UI for ML applications
- **Plotly** - Interactive charts
- **Pandas** - Data manipulation
- **Pydantic** - Data validation

## 📊 Project Structure Details

### Core Components

1. **Data Layer** (`src/data_loader.py`)
   - Loads `transactions.json`
   - Converts to descriptive text format
   - Provides metadata extraction

2. **Vector Store** (`src/vector_store.py`)
   - Initializes ChromaDB collection
   - Creates embeddings using Google Gemini
   - Provides similarity search retriever

3. **RAG Chain** (`src/rag_chain.py`)
   - Builds LangChain RetrievalQA chain with Gemini
   - Custom prompt engineering
   - Context-aware question answering

4. **API Layer** (`src/api/`)
   - Pydantic schemas for validation
   - FastAPI routes and endpoints
   - Dependency injection for chatbot

5. **UI Layer** (`streamlit_app.py`)
   - Streamlit interface
   - Analytics visualizations
   - Conversation tracking
   - Real-time API health monitoring

## 🚨 Troubleshooting

**Issue:** `ModuleNotFoundError`
- **Solution:** Ensure virtual environment is activated and dependencies are installed

**Issue:** `AuthenticationError` from Google
- **Solution:** Check that `GOOGLE_API_KEY` is set correctly in `.env`

**Issue:** Slow first query
- **Solution:** First query initializes the vector store, subsequent queries are faster

**Issue:** Empty responses
- **Solution:** Ensure `transactions.json` exists and vector store is initialized

## 📄 License

This project is for educational purposes as part of a Python assignment.

## 🤝 Contributing

This is an assignment project, but suggestions are welcome!

---

**Built with ❤️ using FastAPI, LangChain, ChromaDB, Streamlit, and Google Gemini**
