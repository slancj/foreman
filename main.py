import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def main():
    llm = ChatOpenAI(
        model="gemini/gemini-3.5-flash-lite",
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("UPSTREAM_API_URL"),
    )
    
    response = llm.invoke("Hello! What is the capital of Paris")
    print(response.content)


if __name__ == "__main__":
    main()
