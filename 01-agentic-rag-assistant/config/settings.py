

### LLM ###

from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv
load_dotenv()


load_dotenv(override=True)


groq_api_key = os.getenv("GROQ_API_KEY")
MODEL = "openai/gpt-oss-120b"

llm = ChatGroq(
    temperature=0,
    model=MODEL,  
    groq_api_key=groq_api_key 
)


