import json
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

from src import bot as discord
from src.redis_store import redis_store

from .gemini import call_gemini_normal

_MAX_CHAT_MESSAGES = 10
_AI_MODELS = {
    "GOOGLE_NORMAL": call_gemini_normal
}


def _convert_json_to_chat_objects(json_data: list[dict]) -> list[HumanMessage | AIMessage]:
    messages = []
    for data in json_data:
        if data["role"] == "user":
            messages.append(HumanMessage(content=data["msg"]))
        elif data["role"] == "bot":
            messages.append(AIMessage(content=data["msg"]))
    return messages


def _call_models(model_name: str, chat_history: list[dict], new_prompt: str, summary_history=None) -> BaseMessage | None:
    try:
        if _AI_MODELS.get(model_name) is None:
            return None

        formatted_history = _convert_json_to_chat_objects(chat_history)
        if summary_history is not None:
            formatted_history.append(
                AIMessage(content=f"Summary of pervious chat messages: {summary_history}"))

        formatted_history.append(HumanMessage(content=new_prompt))
        data = _AI_MODELS.get(model_name)(formatted_history)
        return data
    except Exception as e:
        print(e)
        return None


def _summarize_chat_history(chat_history: list[dict]) -> str:
    first_msgs = chat_history[0:len(chat_history) - _MAX_CHAT_MESSAGES]
    return _call_models("GOOGLE_NORMAL", first_msgs, "Summarize the chat history").content


async def send_message(thread_id: int, prompt: str):
    session = json.loads(redis_store.get(thread_id))
    if session is None:
        return

    summary_of_chat = None
    if len(session.get("chat")) > _MAX_CHAT_MESSAGES:
        summary_of_chat = _summarize_chat_history(session.get("chat"))

    thread = discord.bot.get_channel(session["id"])
    await thread.trigger_typing()

    new_ai_message = _call_models(session.get("model"),
                                  session.get("chat"),
                                  prompt,
                                  summary_of_chat)

    if new_ai_message is None:
        await thread.send("**Error: Model not found or something went wrong**")
        return  # exit of out loop since key does not exist

    session["chat"].append({
        "role": "bot",
        "msg": new_ai_message.content
    })

    redis_store.set(thread_id, json.dumps(session))
    await thread.send(new_ai_message.content)
