import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

# Instantiate model globally so it's reused across runs
llm = ChatOpenAI(
    model="gemini/gemini-3.5-flash-lite",
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("UPSTREAM_API_URL"),
)
