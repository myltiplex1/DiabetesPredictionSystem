from langchain_google_genai import ChatGoogleGenerativeAI
from config import GOOGLE_API_KEY
import os


def get_llm(temperature=0.7, max_tokens=800):
    """
    Returns configured Gemini 1.5 Flash chat model through LangChain
    """
    # Safety: make sure we have the key
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")

    llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",               # ← this should work immediately
    google_api_key=GOOGLE_API_KEY,
    temperature=0.7,
    max_output_tokens=2048,
)
    
    return llm