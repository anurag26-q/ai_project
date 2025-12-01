"""RAG chain implementation for question answering."""
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationalRetrievalChain

from src.vector_store import VectorStoreManager

# Load environment variables
load_dotenv()


class RAGChatbot:
    """RAG-powered chatbot for transactional data queries."""
    
    def __init__(
        self,
        vector_store_manager: Optional[VectorStoreManager] = None,
        llm_model: Optional[str] = None,
        temperature: float = 0,
        top_k: int = 3
    ):
        """
        Initialize the RAG chatbot.
        
        Args:
            vector_store_manager: VectorStoreManager instance
            llm_model: OpenAI model name
            temperature: LLM temperature (0 = deterministic)
            top_k: Number of documents to retrieve
        """
        self.llm_model = llm_model or os.getenv("LLM_MODEL", "gemini-1.5-flash")
        print(f'llm_model : {self.llm_model}')
        self.temperature = float(os.getenv("TEMPERATURE", temperature))
        print(f'temperature : {self.temperature}')
        self.top_k = int(os.getenv("TOP_K_RESULTS", 5))  # Increased default for better retrieval
        print(f'top_k : {self.top_k}')
        
        # Initialize vector store manager
        if vector_store_manager is None:
            from src.vector_store import setup_vector_store
            self.vector_store_manager = setup_vector_store()
        else:
            self.vector_store_manager = vector_store_manager
        
        # Initialize Google Gemini LLM
        self.llm = ChatGoogleGenerativeAI(
            model=self.llm_model,
            temperature=self.temperature,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            convert_system_message_to_human=True
        )
        print(f'LLM : {self.llm}')
        
        # Get retriever
        self.retriever = self.vector_store_manager.get_retriever(top_k=self.top_k)
        
        # Initialize LangChain memory
        self.memory = ConversationBufferWindowMemory(
            k=10,
            memory_key="chat_history",
            return_messages=True,
            output_key="answer"
        )
        
        # Create conversational retrieval chain
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            memory=self.memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": self._get_qa_prompt()}
        )
        print(f'Conversational RAG Chain created successfully')
    

    

    
    def _get_qa_prompt(self) -> ChatPromptTemplate:
        """Get the QA prompt template for the retrieval chain."""
        template = """You are an intelligent transaction assistant that understands natural language queries about customer purchases and spending, even when they contain typos or grammatical errors.

Transaction Context:
{context}

User Question: {question}

Instructions:
- Understand the user's intent despite any spelling mistakes or grammatical errors
- For spending questions, calculate totals by summing all transaction amounts for the customer
- For purchase history questions, list all transactions with product names, amounts (₹), and dates
- If a customer name appears in different cases or with typos, match it intelligently
- If no data exists for a customer/product, clearly state that no transactions were found for that specific customer or product in the database
- Always format currency with ₹ symbol
- Be conversational and helpful

Answer:"""
        
        return ChatPromptTemplate.from_template(template)



    def query(self, question: str) -> Dict[str, Any]:
        """
        Answer a question using RAG with memory.
        
        Args:
            question: User's question
            
        Returns:
            Dictionary containing:
                - answer: The generated answer
                - source_documents: Retrieved documents used as context
        """
        try:
            result = self.chain({"question": question})
            return {
                "answer": result["answer"],
                "source_documents": result["source_documents"],
                "sources": [doc.metadata for doc in result["source_documents"]]
            }
        except Exception as e:
            return {
                "answer": "I'm sorry, I encountered an error processing your question. Please try again.",
                "source_documents": [],
                "sources": []
            }
    
    def chat(self, question: str, use_memory: bool = True) -> Dict[str, Any]:
        """
        Chat with the bot with memory support.
        
        Args:
            question: User's question
            use_memory: Whether to use conversation memory
            
        Returns:
            Dictionary with answer and sources
        """
        if use_memory:
            return self.query(question)
        else:
            # Clear memory temporarily for this query
            temp_memory = self.memory.chat_memory.messages.copy()
            self.memory.clear()
            result = self.query(question)
            # Restore memory
            self.memory.chat_memory.messages = temp_memory
            return result
    
    def get_last_question(self) -> Optional[str]:
        """Get the last question from memory."""
        messages = self.memory.chat_memory.messages
        if messages:
            for msg in reversed(messages):
                if hasattr(msg, 'type') and msg.type == 'human':
                    return msg.content
        return None
    
    def clear_memory(self):
        """Clear conversation history."""
        self.memory.clear()


def main():
    """Test the RAG chatbot."""
    print("Initializing RAG Chatbot...")
    chatbot = RAGChatbot()
    
    # Test queries including ones with typos and errors
    test_questions = [
        "Show me Riya's purchase history.",
        "What is Amit's total spending?", 
        "what are thing that rohit brough",  # Test typo handling
        "wat did amit buy",  # Test multiple typos
        "Which product was purchased most often?",
        "What did Karan buy?"
    ]
    
    print("\n" + "="*80)
    print("Testing RAG Chatbot")
    print("="*80)
    
    for question in test_questions:
        print(f"\n🔍 Question: {question}")
        result = chatbot.query(question)
        print(f"💬 Answer: {result['answer']}")
        print(f"📄 Sources: {len(result['source_documents'])} documents retrieved")
        print("-" * 80)


if __name__ == "__main__":
    main()
