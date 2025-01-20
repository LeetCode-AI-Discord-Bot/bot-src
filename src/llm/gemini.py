from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage

_general_system_prompt = SystemMessage(
    """
    You are a helpful assistant. Please keep your answers short and use markdown to write out your answers.
    """
)

_google_model_normal = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.5,
    max_tokens=200,
    max_retries=3,
)

def call_gemini_normal(chat_history: list[HumanMessage | AIMessage]) -> BaseMessage:
    chat_history.insert(0, _general_system_prompt)
    res = _google_model_normal.invoke(chat_history)
    return res
