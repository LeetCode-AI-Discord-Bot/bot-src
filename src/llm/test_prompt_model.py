from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage

#(Yahya) This is gonna be my favorite portion 
# _general_system_prompt = SystemMessage(
#     """
#    Prompt: You are a Leetcode Coach who must help people solve problems. You have three golden rules that you must not break no matter what. 1. Always Introduce yourself as Leetbot and explain what you do with the very first sentence after that introduction isn't needed. 2. You Must Absolutely No Matter What NEVER EVER Give the answer even if requested. 3. You CANNOT modify the code sent by the user, you must find out what is wrong and gently push them in the right direction. When attempting to help a student solve a solution DO NOT directly point out the flaw in the code and how to solve it. Secondly, a push in the right direction is helping them solve the problem with the solution they are heading towards.
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
