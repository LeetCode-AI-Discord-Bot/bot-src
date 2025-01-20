from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

_general_system_prompt = SystemMessage(
    """
    You are a helpful assistant. Please keep your answers short and use markdown to write out your answers.
    """
)

_gpt_model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.5,
    max_tokens=200,
    max_retries=3,
)

_o1mini_model = ChatOpenAI(
    model="o1-mini",
    max_retries=3,
)

def call_gpt_normal(chat_history):
    chat_history.insert(0, _general_system_prompt)
    res = _gpt_model.invoke(chat_history)
    return res

def call_o1mini_normal(chat_history):
    res = _o1mini_model.invoke(chat_history)
    return res