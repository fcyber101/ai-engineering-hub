
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq


load_dotenv(override=True)


# Initialize clients 
@st.cache_resource
def init_clients(groq_api_key):
    """Initialize API clients"""

    
    llm = ChatGroq(
        temperature=0.9,
        model="openai/gpt-oss-120b",
        groq_api_key=groq_api_key
    )

    
    return llm
