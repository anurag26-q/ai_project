"""Pydantic schemas for API requests and responses."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class TransactionSchema(BaseModel):
    """Schema for a single transaction."""
    id: int
    customer: str
    product: str
    amount: float
    date: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "customer": "Amit",
                "product": "Laptop",
                "amount": 55000,
                "date": "2024-01-12"
            }
        }


class ChatRequest(BaseModel):
    """Schema for chatbot query request."""
    query: str = Field(..., description="User's question about transactions")
    use_memory: bool = Field(True, description="Whether to use conversation memory")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is Amit's total spending?",
                "use_memory": True
            }
        }


class SourceDocument(BaseModel):
    """Schema for a source document."""
    content: str
    metadata: Dict[str, Any]


class ChatResponse(BaseModel):
    """Schema for chatbot response."""
    answer: str = Field(..., description="The chatbot's answer")
    sources: List[Dict[str, Any]] = Field(..., description="Source transaction metadata")
    query: str = Field(..., description="Original query")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Amit spent a total of ₹55,700.",
                "sources": [
                    {"id": 1, "customer": "Amit", "product": "Laptop", "amount": 55000, "date": "2024-01-12"},
                    {"id": 2, "customer": "Amit", "product": "Mouse", "amount": 700, "date": "2024-02-15"}
                ],
                "query": "What is Amit's total spending?"
            }
        }


class HealthCheck(BaseModel):
    """Schema for health check response."""
    status: str
    message: str
    vector_store_initialized: bool
    total_transactions: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "message": "RAG Chatbot API is running",
                "vector_store_initialized": True,
                "total_transactions": 5
            }
        }


class TransactionListResponse(BaseModel):
    """Schema for transaction list response."""
    transactions: List[TransactionSchema]
    total: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "transactions": [
                    {"id": 1, "customer": "Amit", "product": "Laptop", "amount": 55000, "date": "2024-01-12"}
                ],
                "total": 1
            }
        }
