#!/usr/bin/env python3
"""Simple test script to interact with the RAG Chatbot API."""

import requests
import json

API_BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint."""
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print("Health Check:")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_transactions():
    """Test the transactions endpoint."""
    try:
        response = requests.get(f"{API_BASE_URL}/transactions")
        print("\nTransactions:")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"Transactions test failed: {e}")
        return False

def test_chat(query):
    """Test the chat endpoint."""
    try:
        payload = {"query": query}
        response = requests.post(
            f"{API_BASE_URL}/chat",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        print(f"\nChat Query: {query}")
        print("Response:")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"Chat test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=== RAG Chatbot API Test ===\n")
    
    # Test health
    if not test_health():
        print("❌ Health check failed. Make sure the API is running.")
        return
    
    # Test transactions
    if not test_transactions():
        print("❌ Transactions endpoint failed.")
        return
    
    # Test chat queries
    test_queries = [
        "What is Amit's total spending?",
        "Show me Riya's purchase history",
        "Which product was purchased most often?",
        "What are the total sales for January 2024?"
    ]
    
    print("\n=== Testing Chat Queries ===")
    for query in test_queries:
        test_chat(query)
        print("-" * 50)

if __name__ == "__main__":
    main()