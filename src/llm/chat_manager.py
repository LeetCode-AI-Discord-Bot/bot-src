import json
from langchain_core.messages import HumanMessage, AIMessage

from src import bot as discord
from src.redis_store import redis_store

from .gemini import call_gemini_normal
from .openai import call_gpt_normal, call_o1mini_normal
from .test_prompt_model import call_testing_model

_MAX_CHAT_MESSAGES = 10
_AI_MODELS = {
    "GEMINI_NORMAL": call_gemini_normal,
    "GPT_NORMAL": call_gpt_normal,
    "O1MINI_NORMAL": call_o1mini_normal,
    # "TESTING_MODEL": call_testing_model
}


def _convert_json_to_chat_objects(json_data: list[dict]) -> list[HumanMessage | AIMessage]:
    messages = []
    for data in json_data:
        if data["role"] == "user":
            messages.append(HumanMessage(content=data["msg"]))
        elif data["role"] == "bot":
            messages.append(AIMessage(content=data["msg"]))
    return messages

#(Yahya) Modify this by adding in gpt selection
def _call_models(model_name: str, 
                 chat_history: list[dict], 
                 new_prompt: str, 
                 summary_history=None, 
                 system_prompt=None, 
                 temperature=None,
                 gpt=None) -> str | None:
    try:
        if _AI_MODELS.get(model_name) is None:
            return None

        formatted_history = _convert_json_to_chat_objects(chat_history)
        if summary_history is not None:
            formatted_history.append(
                AIMessage(content=f"Summary of pervious chat messages and label it as \"SUMMARY OF PREVIOUS CHAT MESSAGES\": {summary_history}"))

        formatted_history.append(HumanMessage(content=new_prompt))

        data = None
        if model_name == "TESTING_MODEL":
            data = call_testing_model(formatted_history, system_prompt, temperature, gpt)
        else:
            data = _AI_MODELS.get(model_name)(formatted_history)

        return data.content
    except Exception as e:
        print(e)
        return None

# TODO (Gabe) This is simple, should also add a way to pass in previous summaries as well
def _summarize_chat_history(chat_history: list[dict]) -> str:
    first_msgs = chat_history[:_MAX_CHAT_MESSAGES]
    return _call_models("GEMINI_NORMAL", first_msgs, "Summarize the chat history")

# TODO (Gabe) Add more error handling
# TODO (Yahya) Modify this by adding in gpt selection
async def send_message(thread_id: int, prompt: str):
    session = json.loads(redis_store.get(thread_id))
    if session is None:
        return
    
    if len(session.get("chat")) > _MAX_CHAT_MESSAGES:
        summary = _summarize_chat_history(session.get("chat"))
        session["summary_chat"] = summary
        session["chat"] = session.get("chat")[_MAX_CHAT_MESSAGES:]
        redis_store.set(thread_id, json.dumps(session))

    summary_of_chat = None
    if session.get("summary_chat") is not None or session.get("summary_chat") != "":
        summary_of_chat = session.get("summary_chat")

    thread = discord.bot.get_channel(session["id"])
    await thread.trigger_typing()

    new_ai_message = _call_models(session.get("model"),
                                  session.get("chat"),
                                  prompt,
                                  summary_of_chat,
                                  session.get("system_prompt"),
                                  session.get("temp"),
                                  session.get("gpt"))

    if new_ai_message is None:
        await thread.send("**Error: Model not found or something went wrong**")
        return  # exit of out loop since key does not exist

    session["chat"].append(
    {
        "role": "user",
        "msg": prompt
    })
    session["chat"].append(  
    {
        "role": "bot",
        "msg": new_ai_message
    })

    redis_store.set(thread_id, json.dumps(session))

    for i in range(0, len(new_ai_message), 2000):
        await thread.send(new_ai_message[i:i + 2000])
