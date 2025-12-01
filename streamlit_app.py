"""Streamlit UI for RAG Chatbot with charts and memory (latest Q/A only, no loops)."""
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Page config
st.set_page_config(
    page_title="RAG Chatbot - Transactional Data",
    page_icon="🤖",
    layout="wide"
)

# ---------------- Session State ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_question" not in st.session_state:
    st.session_state.last_question = None
if "input_key" not in st.session_state:
    st.session_state.input_key = 0






# ---------------- API Config ----------------
API_BASE = os.getenv("API_BASE", "http://localhost:8000")


def get_transactions():
    """Get transactions from API."""
    try:
        response = requests.get(f"{API_BASE}/transactions", timeout=5)
        if response.status_code == 200:
            return response.json().get("transactions", [])
        return []
    except Exception:
        return []


def chat_with_bot(query: str):
    """Send query to chatbot API."""
    try:
        response = requests.post(
            f"{API_BASE}/chat",
            json={"query": query, "use_memory": True},
            timeout=10,
        )
        if response.status_code == 200:
            return response.json()
        # if API returned an error body
        try:
            detail = response.json().get("detail", "Unknown error")
        except Exception:
            detail = "Unknown error"
        return {"answer": f"API Error: {detail}", "sources": []}
    except Exception as e:
        return {"answer": f"Connection error: {str(e)}", "sources": []}


# ---------------- Charts ----------------
def create_monthly_chart(df: pd.DataFrame):
    """Create monthly spending chart."""
    if df.empty:
        return None

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M").astype(str)
    monthly_spending = df.groupby("month")["amount"].sum().reset_index()

    fig = px.line(
        monthly_spending,
        x="month",
        y="amount",
        title="Monthly Spending Trend",
        markers=True,
    )
    fig.update_layout(height=400)
    return fig


def create_customer_chart(df: pd.DataFrame):
    """Create customer spending chart."""
    if df.empty:
        return None

    customer_spending = df.groupby("customer")["amount"].sum().reset_index()
    customer_spending = customer_spending.sort_values("amount", ascending=False)

    fig = px.bar(
        customer_spending,
        x="customer",
        y="amount",
        title="Total Spending by Customer",
        color="amount",
    )
    fig.update_layout(height=400)
    return fig


# ---------------- API Health Check ----------------
def check_api_status():
    global API_BASE
    endpoints = ["http://fastapi:8000", "http://localhost:8000", API_BASE]

    for endpoint in endpoints:
        try:
            response = requests.get(f"{endpoint}/health", timeout=5)
            if response.status_code == 200:
                API_BASE = endpoint
                return True
        except Exception as e:
            print(f"Failed to connect to {endpoint}: {e}")
            continue
    return False


# ---------------- UI Layout ----------------
st.title("🤖 RAG-Powered Transactional Chatbot")

# API Status indicator
api_online = check_api_status()
if api_online:
    st.success("✅ Backend API is online - Full RAG functionality available")
else:
    st.warning("⚠️ Backend API is offline - Using local fallback mode")

st.markdown("Ask questions about customer transactions using natural language!")

# ----- Sidebar: Analytics -----
with st.sidebar:
    st.header("📊 Analytics")

    transactions = get_transactions()
    if transactions:
        df = pd.DataFrame(transactions)

        # Monthly spending chart
        monthly_fig = create_monthly_chart(df)
        if monthly_fig:
            st.plotly_chart(monthly_fig, use_container_width=True)

        # Customer spending chart
        customer_fig = create_customer_chart(df)
        if customer_fig:
            st.plotly_chart(customer_fig, use_container_width=True)

        # Transaction summary
        st.subheader("📋 Summary")
        st.metric("Total Transactions", len(df))
        st.metric("Total Amount", f"₹{df['amount'].sum():,.0f}")
        st.metric("Unique Customers", df["customer"].nunique())
    else:
        st.error("Could not load transaction data - API may be offline")

# ----- Main chat area -----
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("💬 Chat with Transaction Assistant")

    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

with col2:
    st.subheader("🕒 Memory")

    # Show last question button
    if st.button("Show My Last Question"):
        if st.session_state.last_question:
            st.info(f"**Last Question:** {st.session_state.last_question}")
        else:
            st.warning("No previous questions found")

    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.last_question = None
        st.session_state.input_key += 1



# ----- Chat input (bottom) -----
user_input = st.chat_input(
    "Ask about transactions...",
    key=f"chat_input_{st.session_state.input_key}",
)

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.last_question = user_input

    # Get bot response
    with st.spinner("Thinking..."):
        response = chat_with_bot(user_input)
        answer = response["answer"]

    # Add assistant message
    st.session_state.messages.append({"role": "assistant", "content": answer})
    
    # Increment key to reset input
    st.session_state.input_key += 1
    st.rerun()

# ----- Footer -----
st.markdown("---")
st.markdown("Built with Streamlit, FastAPI, LangChain, and Google Gemini")
