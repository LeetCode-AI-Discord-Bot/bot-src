import subprocess
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
import redis

from src.leetcode_problem import LeetCodeProblem
from src.redis_checkpoint_saver import RedisCheckpointSaver

import os
from dotenv import load_dotenv

load_dotenv()    

SYSTEM_PROMPT = """
You are a LeetCode tutor who helps students solve and debug problems. Your goal is to clarify complex topics, build critical thinking, and develop problem-solving skills without giving direct answers. Instead, guide students step by step, ensuring they always know the next step.

- Encourage Independence: Let students solve problems on their own. Confirm correctness or suggest improvements—never just give answers.  
- Teach Strategically: Recommend study tips, mnemonics, and effective learning techniques. Help break down complex concepts.  
- Promote Critical Thinking: Ask open-ended questions, encourage reasoning, and show real-world connections.  
- Be Patient & Supportive: Adjust to the student’s pace, provide positive reinforcement, and remind them that progress takes practice.  
- Be Clear & Concise: Keep responses short (min 1 character, max 2000 characters) and straight to the point.  

Writing Style Guide:
- Use clear, direct language and avoid complex terminology.
- Aim for a Flesch reading score of 80 or higher.
- Use the active voice.
- Avoid adverbs.
- Avoid buzzwords and instead use plain English.
- Use jargon where relevant.
- Avoid being salesy or overly enthusiastic and instead express calm confidence.
- Use a teenager's voice and avoid overly formal language.
"""

# https://langchain-ai.github.io/langgraph/reference/graphs/?h=compiledgraph#langgraph.graph.graph.CompiledGraph.stream
# https://stackoverflow.com/questions/43274476/is-there-a-way-to-check-if-a-subprocess-is-still-running
# https://langchain-ai.github.io/langgraph/tutorials/introduction/#part-1-build-a-basic-chatbot
# https://python.langchain.com/docs/tutorials/agents/#define-tools

# Tooling for LLM
# Move this to a server docker image
def run_python_code(code: str) -> str:
    """Run Python code. This code will be saved as a Python file and then executed. Output of the code will be returned."""
    file_write = open("temp.py", "w", encoding="utf-8")
    file_write.write(code)
    file_write.close()
    return subprocess.run(["python", "temp.py"], capture_output=True, text=True).stdout


# TODO: Make bot only run one instance
search = TavilySearchResults(max_results=2, api_key=os.getenv("TAVILY_API_KEY"))
tools = [search, run_python_code]

class ReActAgent:
    def __init__(self, leetcode_url):
        self.CheckpointSaver = RedisCheckpointSaver(redis.Redis.from_url(os.getenv("REDIS_URL")))
        self.model = ChatOpenAI(model_name="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))
        self.leetcode_problem = LeetCodeProblem(leetcode_url)
        self.agent_executor = create_react_agent(self.model, tools, checkpointer=self.CheckpointSaver)

    def process_message(self, user_message: str, thread_id: str) -> str:
        try:
            system_message = SYSTEM_PROMPT + "\n\n LeetCode Title: " + self.leetcode_problem.title + "\n\n LeetCode Problem:" + self.leetcode_problem.question
            system_message += "\n\n Hints:\n" + "\n".join(self.leetcode_problem.hints) if self.leetcode_problem.hints != [] else "\nNone"
            stream = self.agent_executor.stream(
                {
                    "messages": [
                        SystemMessage(content=system_message),
                        HumanMessage(content=user_message),
                    ] 
                },
                config={"configurable": {"thread_id": thread_id}},
                stream_mode="values"
            )

            last_message = None
            for step in stream:
                step["messages"][-1].pretty_print()
                last_message = step["messages"][-1]

            if not last_message:
                raise Exception("No message was created by model")

            return last_message.content

        except Exception as exc:
            raise Exception("Failed to call model") from exc

if __name__ == "__main__":
    agent = ReActAgent("https://leetcode.com/problems/maximum-subarray/")
    agent.process_message("write a hello welcome message for me regarding the problem", "1")
