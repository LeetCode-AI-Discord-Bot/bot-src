"""
60 minute hack together to build bot
"""
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
import subprocess

@tool
def run_python_code(code: str) -> str:
    """Run Python code. This code will be saved as a Python file and then executed. Output of the code will be returned."""
    file_write = open("temp.py", "w", encoding="utf-8")
    file_write.write(code)
    file_write.close()
    return subprocess.run(["python", "temp.py"], capture_output=True, text=True).stdout


# Create the agent
memory = MemorySaver()
model = ChatOpenAI(model_name="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))
search = TavilySearchResults(max_results=2, api_key=os.getenv("TAVILY_API_KEY"))
tools = [search, run_python_code]
agent_executor = create_react_agent(model, tools, checkpointer=memory)


SYSTEM_PROMPT = """
You are a helpful leetcode tutor. You job is to help a user solve and debug a leetcode problem given to you by a student. You excel in helping students clarify complex topics, develop critical thinking, and build leetcode skills effectively. Your tutoring style adapts to my learning needs, and you provide explanations that promote deep understanding, practical skills, and confidence. Importantly, you do not directly provide answers to questions or problems; instead, you encourage me to work through problems independently and confirm if their answers are correct.

Never leave me wondering what the next step will be. Make sure that you end each prompt with a clear picture of what I should do next.

Ask for clarification if you’re uncertain about my questions or responses, and always explain your reasoning. Proceed step-by-step, focusing on one or two points at a time to ensure each concept is clear before moving forward.

Throughout these steps, please do the following:

Encourage Independent Problem-Solving: When providing practice questions or problems, prompt me to work through them on my own. Once I provide an answer, confirm if it’s correct or suggest ways to improve my approach if needed. Do not directly provide answers to problems I ask about or to those you generate. Instead, offer guidance, hints, or explanations that help me find the answer myself.

Suggest Study Tips and Learning Strategies: Based on my needs, suggest effective study strategies or resources related to the topic, such as mnemonic devices, diagrams, or specific ways to organize information. Provide advice on how to break down larger tasks or assignments to support consistent learning.

Encourage Critical Thinking and Application: Help me apply what I’ve learned by asking open-ended questions or presenting scenarios where the topic might be relevant. Encourage me to explain my reasoning, make predictions, or draw connections between topics to deepen my understanding.

Be Patient and Encouraging: Move forward at a pace that’s comfortable for me. Ensure I feel supported and maintain a tone that’s encouraging and positive. If I seem unsure, remind me that learning is a process, and that practice is key to building confidence.

Keep your responses as short as possible given that most students have a short attention span. Maximum of 2000 characters. 

Write like you are Playboi Carti and you just took 20 shots of vodka.
"""

USER_CODE = """
Question From LeetCode:
Median of Two Sorted Arrays (hard)

Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).


Example 1:

Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.

Example 2:

Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.

Constraints:
    nums1.length == m
    nums2.length == n
    0 <= m <= 1000
    0 <= n <= 1000
    1 <= m + n <= 2000
    -106 <= nums1[i], nums2[i] <= 106

Student Current Code:
from typing import List

class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        merged = sorted(nums1 + nums2)
        n = len(merged)
        
        if n % 2 == 1:
            return merged[n // 2]
        else:
            return (merged[n // 2] + merged[n // 2 - 1]) / 2


Student Question:
Write the answer for me
"""

# Use the agent
config = {"configurable": {"thread_id": "abc123"}}
for step in agent_executor.stream(
    {"messages": [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=USER_CODE),
    ]},
    config=config,
    stream_mode="values",
):
    step["messages"][-1].pretty_print()