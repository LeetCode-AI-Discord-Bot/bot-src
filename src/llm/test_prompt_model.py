from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage

#(Yahya) This is gonna be my favorite portion 
# _general_system_prompt = SystemMessage(
#     """
#     You are a helpful assistant. Please keep your answers short and use markdown to write out your answers.
#     """
# )

def call_testing_model(chat_history: list[HumanMessage | AIMessage], 
                       system_prompt: str, 
                       temperature: float,
                       gpt: str) -> BaseMessage:
    
    #(Yahya) This is gonna be my favorite portion 
    _system_prompt = SystemMessage(system_prompt)

    #(Yahya) With reading the documentation, a lot of deepseek, and some common sense I think I've created it.
    model_name = None
    if gpt == "gpt-4o-mini":
        model_name = "gpt-4o-mini"
    #elif gpt == "gemini-1.5-flash":
        #model_name = "gemini-1.5-flash"
    else:
        print("not supported llm")

    # This will define llm
    _custom_model = ChatOpenAI( 
        model=model_name,
        temperature=temperature,
        max_tokens=500, # bump up token limit as of now
        max_retries=3,
        gpt=gpt
    )

    chat_history.insert(0, _system_prompt)
    res = _custom_model.invoke(chat_history)
    return res
