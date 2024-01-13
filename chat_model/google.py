import os
from langchain_google_genai import ChatGoogleGenerativeAI

MODEL = os.environ.get("MODEL")
GOOGLE_API_KEY=os.environ.get("GOOGLE_API_KEY")

def make_chat_with_google_model(query):
    llm = ChatGoogleGenerativeAI(model=MODEL)
    return llm.invoke(query + "give the result with full html css")
