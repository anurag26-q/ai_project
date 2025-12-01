"""Quick start script to set up the RAG chatbot."""
import os
import sys
from pathlib import Path


def check_environment():
    """Check if environment is properly set up."""
    print("🔍 Checking environment setup...")
    
    # Check if .env exists
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        print("📝 Please create a .env file from .env.example:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your OPENAI_API_KEY")
        return False
    
    # Check if GOOGLE_API_KEY is set
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_google_api_key_here":
        print("❌ GOOGLE_API_KEY not configured!")
        print("📝 Please add your Google API key to the .env file")
        return False
    
    print("✅ Environment configured correctly!")
    return True


def setup_vector_store():
    """Initialize the vector store with transaction data."""
    print("\n📦 Setting up vector store...")
    
    try:
        from src.vector_store import setup_vector_store
        
        # Check if vector store already exists
        chroma_path = Path("./chroma_db")
        force_recreate = not chroma_path.exists()
        
        if force_recreate:
            print("Creating new vector store...")
        else:
            print("Vector store already exists, loading...")
        
        manager = setup_vector_store(force_recreate=force_recreate)
        print("✅ Vector store ready!")
        return True
    
    except Exception as e:
        print(f"❌ Error setting up vector store: {e}")
        return False


def test_chatbot():
    """Test the chatbot with a sample query."""
    print("\n🤖 Testing chatbot...")
    
    try:
        from src.rag_chain import RAGChatbot
        
        chatbot = RAGChatbot()
        result = chatbot.query("What is Amit's total spending?")
        
        print(f"\n📝 Test Query: What is Amit's total spending?")
        print(f"💬 Answer: {result['answer']}")
        print(f"📄 Sources: {len(result['source_documents'])} transactions retrieved")
        print("✅ Chatbot is working!")
        return True
    
    except Exception as e:
        print(f"❌ Error testing chatbot: {e}")
        return False


def main():
    """Run the quick start setup."""
    print("="*60)
    print("🚀 RAG Chatbot Quick Start")
    print("="*60)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Setup vector store
    if not setup_vector_store():
        sys.exit(1)
    
    # Test chatbot
    if not test_chatbot():
        sys.exit(1)
    
    # Success!
    print("\n" + "="*60)
    print("✅ Setup complete! You can now:")
    print("="*60)
    print("1. Start FastAPI backend:")
    print("   python main.py")
    print("   Then visit: http://localhost:8000/docs")
    print()
    print("2. Launch Gradio UI:")
    print("   python run_ui.py")
    print("   Then visit: http://localhost:7860")
    print("="*60)


if __name__ == "__main__":
    main()
