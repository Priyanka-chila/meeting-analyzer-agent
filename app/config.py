import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GEMINI_MODEL  = "gemini-3.5-flash"
# llm= ChatGoogleGenerativeAI(
#     model=GEMINI_MODEL,
#     temperature=0
# )
    


if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY is not configured."
    )