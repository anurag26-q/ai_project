"""Reset vector store to ensure all transactions are properly indexed."""
import os
import shutil
from src.vector_store import setup_vector_store

def reset_vector_store():
    # Remove existing vector store
    vector_db_path = "./chroma_db"
    if os.path.exists(vector_db_path):
        shutil.rmtree(vector_db_path)
        print(f"Removed existing vector store at {vector_db_path}")
    
    # Create fresh vector store
    print("Creating fresh vector store...")
    manager = setup_vector_store(force_recreate=True)
    
    # Verify all transactions are loaded
    collection = manager.vectorstore._collection
    count = collection.count()
    print(f"Vector store now contains {count} documents")
    
    if count == 14:
        print("✅ All 14 transactions successfully loaded!")
    else:
        print(f"⚠️ Expected 14 transactions, but found {count}")

if __name__ == "__main__":
    reset_vector_store()