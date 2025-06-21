import subprocess
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
import redis
import requests

from src.logger import logger
from src.leetcode_problem import LeetCodeProblem
from src.redis_checkpoint_saver import RedisCheckpointSaver

import os
from dotenv import load_dotenv

load_dotenv()    


def create_python_tool(thread_id: str):
    def run_python_code(code: str) -> str:
        """
        Run Python code. This code will be saved as a Python file and then executed. Output of the code will be returned.
        """
        try:
            res = requests.post(os.getenv("CODE_SERVER_URL") + "/run-python", json={"code": code, "thread_id": thread_id})
            return res.json()["result"]
        except Exception as e:
            return "Failed to run tool"
        
    return run_python_code

SEARCH_TOOL = TavilySearch(max_results=2, topic="general")
BASE_MODEL = ChatOpenAI(model_name="gpt-4.1", api_key=os.getenv("OPENAI_API_KEY"))
CHECK_POINT_SAVER = RedisCheckpointSaver(redis.Redis.from_url(os.getenv("REDIS_URL")))

class ReActCodeAgent:
    def __init__(self, leetcode_url: str, thread_id: str, system_prompt: str):
        self.CheckpointSaver = CHECK_POINT_SAVER
        self.model = BASE_MODEL
        self.system_prompt = system_prompt
        self.leetcode_problem = LeetCodeProblem(leetcode_url)
        self.thread_id = thread_id
        self.__tools = [SEARCH_TOOL, create_python_tool(self.thread_id)]
        self.agent_executor = create_react_agent(self.model, self.__tools, checkpointer=self.CheckpointSaver)

    def process_message(self, user_message: str) -> str:
        try:
            system_message = self.system_prompt + "\n\n LeetCode Title: " + self.leetcode_problem.title + "\n\n LeetCode Problem:\n" + self.leetcode_problem.question
            system_message += "\n\n Hints:\n" + "\n".join(self.leetcode_problem.hints) if self.leetcode_problem.hints != [] else "\nNone"
            stream = self.agent_executor.stream(
                {
                    "messages": [
                        SystemMessage(content=system_message),
                        HumanMessage(content=user_message),
                    ] 
                },
                config={"configurable": {"thread_id": self.thread_id}},
                stream_mode="values"
            )

            last_message = None
            for step in stream:
                logger.info(f"[REACT-CODE-AGENT] LLM MESSAGES={step["messages"][-1].content}")
                last_message = step["messages"][-1]

            if not last_message:
                raise Exception("No message was created by model")

            return last_message.content

        except Exception as exc:
            raise Exception(f"Failed to call model: {str(exc)}") from exc

if __name__ == "__main__":
    # NOTE (Gabe): This sucks, but remove src. from import to run local testing of code
    agent = ReActCodeAgent("https://leetcode.com/problems/maximum-subarray/", "1", system_prompt="Test")
    agent.process_message("write a hello welcome message for me regarding the problem")
