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
        self.top_k = int(os.getenv("TOP_K_RESULTS", 50))  # Maximum retrieval for comprehensive queries
        print(f'top_k : {self.top_k}')
        
        # Initialize vector store manager
        if vector_store_manager is None:
            from src.vector_store import setup_vector_store
            self.vector_store_manager = setup_vector_store(force_recreate=True)
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
        template = """You are a transaction assistant. Use ALL transaction data in the context to answer questions accurately.

Transaction Context:
{context}

User Question: {question}

IMPORTANT RULES:
- For "all customers" or "total spending" queries: You MUST include EVERY customer and EVERY transaction found in the context above
- For individual customer queries: Find ALL transactions for that specific customer
- Always list every transaction found in the context - do not skip any
- Show complete calculations with customer names, products, amounts, and dates
- Group transactions by customer when showing totals
- Format amounts in Indian Rupees (Rs.) with proper formatting
- If the context contains multiple transactions, list them ALL in your answer

ANSWER FORMAT FOR "ALL CUSTOMERS" QUERIES:
1. List each customer with their transactions
2. Show the total for each customer
3. Calculate and show the grand total at the end

Example for comprehensive queries:
"Here are all the transactions:

Amit:
- 2024-01-12: Laptop - Rs.55,000
- 2024-02-15: Mouse - Rs.700
Total for Amit: Rs.55,700

[... continue for ALL customers in context ...]

Grand Total: Rs.[sum of all]"

Answer:"""
        
        return ChatPromptTemplate.from_template(template)



    def query(self, question: str) -> Dict[str, Any]:
        """
        Answer a question using RAG with intelligent, dynamic retrieval and conversation memory.
        The system automatically retrieves all documents and lets the LLM decide what to use.
        
        Args:
            question: User's question
            
        Returns:
            Dictionary containing:
                - answer: The generated answer
                - source_documents: Retrieved documents used as context
        """
        try:
            # Always retrieve ALL transactions and let the LLM intelligently use what it needs
            # This removes the need for static keyword matching
            all_docs = self.vector_store_manager.vectorstore.similarity_search(
                question, 
                k=14  # Retrieve all 14 transactions - let LLM decide what's relevant
            )
            
            # Create context from all documents
            context = "\n\n".join([doc.page_content for doc in all_docs])
            
            # Get conversation history
            chat_history = self.memory.load_memory_variables({}).get("chat_history", [])
            
            # Format chat history for the prompt
            history_text = ""
            if chat_history:
                history_text = "\n\nPrevious Conversation:\n"
                for msg in chat_history[-6:]:  # Last 3 exchanges (6 messages)
                    role = "User" if msg.type == "human" else "Assistant"
                    history_text += f"{role}: {msg.content}\n"
            
            # Use enhanced prompt that guides the LLM to use appropriate level of detail
            prompt = ChatPromptTemplate.from_template(
                """You are an intelligent transaction assistant with access to all transaction data.
{history}
Available Transaction Data:
{context}

Current Question: {question}

Think step-by-step:
1. Check if this is a follow-up question referring to previous conversation
2. What is the user asking for? (specific customer, comparison, total, analysis, etc.)
3. Which transactions are relevant to answer this question?
4. What level of detail does the user want? (concise summary vs detailed breakdown)

Response Guidelines:
- If this is a follow-up question, use context from previous conversation
- For simple "total" or "how much" questions: Provide a concise answer with just the final number
- For "show me" or "list" questions: Provide detailed breakdown
- For "all customers" with "list each": Show complete breakdown by customer
- For comparisons or rankings: Show relevant comparisons
- Always be accurate and use all relevant data
- Use Indian Rupee format: Rs.X,XXX or ₹X,XXX

Answer the question appropriately:"""
            )
            
            chain = prompt | self.llm | StrOutputParser()
            answer = chain.invoke({
                "context": context, 
                "question": question,
                "history": history_text
            })
            
            # Save to memory
            self.memory.save_context(
                {"question": question},
                {"answer": answer}
            )
            
            return {
                "answer": answer,
                "source_documents": all_docs,
                "sources": [doc.metadata for doc in all_docs]
            }
            
        except Exception as e:
            print(f"[ERROR] Query failed: {e}")
            import traceback
            traceback.print_exc()
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
