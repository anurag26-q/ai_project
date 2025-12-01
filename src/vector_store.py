"""Vector store management using LangChain and ChromaDB."""
import os
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.schema import Document

from src.data_loader import get_all_transaction_texts, get_transaction_metadata

# Load environment variables
load_dotenv()


class VectorStoreManager:
    """Manages the vector store for transaction embeddings."""
    
    def __init__(
        self,
        persist_directory: Optional[str] = None,
        collection_name: Optional[str] = None,
        embedding_model: Optional[str] = None
    ):
        """
        Initialize the vector store manager.
        
        Args:
            persist_directory: Directory to store ChromaDB data
            collection_name: Name of the collection in ChromaDB
            embedding_model: OpenAI embedding model to use
        """
        self.persist_directory = persist_directory or os.getenv("VECTOR_DB_PATH", "./chroma_db")
        self.collection_name = collection_name or os.getenv("COLLECTION_NAME", "transactions")
        self.embedding_model = embedding_model or os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-001")

        print(f' VECTOR STORE ')
        print(f'persist_directory : {self.persist_directory}')
        print(f'collection_name : {self.collection_name}')
        print(f'embedding_model : {self.embedding_model}')
        print(f' VECTOR STORE')
        # print(f'')
        
        # Initialize embeddings using Google Gemini
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=self.embedding_model,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        self.vectorstore: Optional[Chroma] = None
    
    def initialize_store(self, force_recreate: bool = False) -> Chroma:
        """
        Initialize or load the vector store.
        
        Args:
            force_recreate: If True, recreate the store even if it exists
            
        Returns:
            Initialized ChromaDB vector store
        """
        persist_path = Path(self.persist_directory)
        
        # Check if vector store already exists
        if persist_path.exists() and not force_recreate:
            print(f"Loading existing vector store from {self.persist_directory}")
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
                collection_name=self.collection_name
            )
        else:
            print(f"Creating new vector store at {self.persist_directory}")
            # Create the store (will be populated later via ingest)
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
                collection_name=self.collection_name
            )
        
        return self.vectorstore
    
    def ingest_transactions(self) -> None:
        """
        Ingest transaction data into the vector store.
        Creates embeddings for all transactions and stores them.
        """
        if self.vectorstore is None:
            self.initialize_store()
        
        # Get transaction texts and metadata
        transaction_texts = get_all_transaction_texts()
        transaction_metadata = get_transaction_metadata()
        
        # Create Document objects with metadata and unique IDs
        documents = [
            Document(
                page_content=text,
                metadata={**metadata, "doc_id": f"txn_{metadata['id']}"}
            )
            for text, metadata in zip(transaction_texts, transaction_metadata)
        ]
        
        print(f"Ingesting {len(documents)} transactions into vector store...")
        
        # Clear existing data to prevent duplicates
        self.vectorstore.delete_collection()
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
            collection_name=self.collection_name
        )
        
        # Add documents to vector store with unique IDs
        ids = [f"txn_{metadata['id']}" for metadata in transaction_metadata]
        self.vectorstore.add_documents(documents, ids=ids)
        
        # Persist to disk
        self.vectorstore.persist()
        
        print(f"Successfully ingested {len(documents)} transactions!")
    
    def get_retriever(self, top_k: int = 3):
        """
        Get a retriever for similarity-based search.
        
        Args:
            top_k: Number of most relevant documents to retrieve
            
        Returns:
            LangChain retriever object
        """
        if self.vectorstore is None:
            self.initialize_store()
        
        return self.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={"k": top_k, "fetch_k": 50}
        )
    
    def retrieve_transactions(self, query: str, top_k: int = 3) -> List[Document]:
        """
        Retrieve the most relevant transactions for a query.
        
        Args:
            query: User's question or search query
            top_k: Number of results to return
            
        Returns:
            List of most relevant transaction documents
        """
        if self.vectorstore is None:
            self.initialize_store()
        
        results = self.vectorstore.similarity_search(query, k=top_k)
        return results


def setup_vector_store(force_recreate: bool = False) -> VectorStoreManager:
    """
    Convenience function to set up and populate the vector store.
    
    Args:
        force_recreate: Whether to recreate the vector store from scratch
        
    Returns:
        Initialized VectorStoreManager
    """
    manager = VectorStoreManager()
    manager.initialize_store(force_recreate=force_recreate)
    
    # Check if we need to ingest data
    if force_recreate or manager.vectorstore._collection.count() == 0:
        manager.ingest_transactions()
    else:
        print(f"Vector store already contains {manager.vectorstore._collection.count()} documents")
    
    return manager


if __name__ == "__main__":
    # Test vector store setup
    print("Setting up vector store...")
    manager = setup_vector_store(force_recreate=True)
    
    # Test retrieval
    print("\nTesting retrieval...")
    query = "What did Amit buy?"
    results = manager.retrieve_transactions(query, top_k=2)
    
    print(f"\nQuery: {query}")
    print(f"Found {len(results)} relevant transactions:")
    for i, doc in enumerate(results, 1):
        print(f"\n{i}. {doc.page_content}")
        print(f"   Metadata: {doc.metadata}")
