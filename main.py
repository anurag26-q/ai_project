"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.api.routes import router, initialize_chatbot


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup: Initialize the chatbot
    print("Starting up RAG Chatbot API...")
    initialize_chatbot()
    yield
    # Shutdown: Cleanup (if needed)
    print("Shutting down RAG Chatbot API...")


# Create FastAPI app
app = FastAPI(
    title="RAG-Powered Transactional Chatbot",
    description="A Retrieval-Augmented Generation chatbot for answering questions about customer transactions",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, tags=["Chatbot"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
