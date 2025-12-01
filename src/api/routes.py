"""FastAPI routes for the RAG chatbot."""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from src.api.schemas import (
    ChatRequest,
    ChatResponse,
    HealthCheck,
    TransactionListResponse,
    TransactionSchema
)
from src.data_loader import load_transactions
from src.rag_chain import RAGChatbot

# Create router
router = APIRouter()

# Global chatbot instance (will be initialized on startup)
chatbot_instance: RAGChatbot = None


def get_chatbot() -> RAGChatbot:
    """Dependency to get the chatbot instance."""
    global chatbot_instance
    if chatbot_instance is None:
        raise HTTPException(status_code=503, detail="Chatbot not initialized")
    return chatbot_instance


def initialize_chatbot():
    """Initialize the chatbot on app startup."""
    global chatbot_instance
    try:
        print("Initializing RAG Chatbot...")
        chatbot_instance = RAGChatbot()
        print("RAG Chatbot initialized successfully!")
    except Exception as e:
        print(f"Error initializing chatbot: {e}")
        raise


@router.get("/health", response_model=HealthCheck)
async def health_check():
    """
    Check the health status of the API.
    
    Returns:
        HealthCheck with status information
    """
    try:
        transactions = load_transactions()
        vector_store_ok = chatbot_instance is not None
        
        return HealthCheck(
            status="healthy" if vector_store_ok else "degraded",
            message="RAG Chatbot API is running",
            vector_store_initialized=vector_store_ok,
            total_transactions=len(transactions)
        )
    except Exception as e:
        return HealthCheck(
            status="unhealthy",
            message=f"Error: {str(e)}",
            vector_store_initialized=False,
            total_transactions=0
        )


@router.get("/transactions", response_model=TransactionListResponse)
async def get_transactions():
    """
    Get all transactions from the database.
    
    Returns:
        List of all transactions
    """
    try:
        transactions = load_transactions()
        transaction_schemas = [TransactionSchema(**txn) for txn in transactions]
        
        return TransactionListResponse(
            transactions=transaction_schemas,
            total=len(transaction_schemas)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading transactions: {str(e)}")


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, chatbot: RAGChatbot = Depends(get_chatbot)):
    """
    Chat with the RAG-powered bot about transactions.
    
    Args:
        request: ChatRequest containing the user's query
        chatbot: RAGChatbot instance (injected dependency)
        
    Returns:
        ChatResponse with the answer and source documents
    """
    try:
        # Query the chatbot
        result = chatbot.chat(request.query, use_memory=request.use_memory)
        
        return ChatResponse(
            answer=result["answer"],
            sources=result["sources"],
            query=request.query
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


@router.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "RAG-Powered Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "transactions": "/transactions",
            "chat": "/chat (POST)",
            "docs": "/docs"
        }
    }
