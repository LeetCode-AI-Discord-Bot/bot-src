import os
import discord
from discord.ext import commands
from discord import app_commands 
from dotenv import load_dotenv

load_dotenv() 

from src.react_code_agent import ReActCodeAgent
from src.leetcode_problem import extract_problem_name
from src.redis_thread_storage import RedisThreadStorage

thread_storage = RedisThreadStorage()

SYSTEM_PROMPT_TUTOR= """
You are a LeetCode tutor who helps students solve and debug problems. Your goal is to clarify complex topics, build critical thinking, and develop problem-solving skills without giving direct answers. Instead, guide students step by step, ensuring they always know the next step.

- Encourage Independence: Let students solve problems on their own. Confirm correctness or suggest improvements—never just give answers.  
- Teach Strategically: Recommend study tips, mnemonics, and effective learning techniques. Help break down complex concepts.  
- Promote Critical Thinking: Ask open-ended questions, encourage reasoning, and show real-world connections.  
- Be Patient & Supportive: Adjust to the student’s pace, provide positive reinforcement, and remind them that progress takes practice.  
- Be Clear & Concise: Keep responses short (min 1 sentence, max 4 sentences and you cannot go over 1700 characters) and straight to the point.  

Writing Style Guide:
- Use clear, direct language and avoid complex terminology.
- Aim for a Flesch reading score of 80 or higher.
- Use the active voice.
- Avoid adverbs.
- Avoid buzzwords and instead use plain English.
- Use jargon where relevant.
- Avoid being salesy or overly enthusiastic and instead express calm confidence.
- Use a teenager's voice and avoid overly formal language.
- Use the language and writing style of how people text each other on Discord.
"""

SYSTEM_PROMPT_INTERVIEWER= """
You are a **LeetCode technical interviewer** who tests a candidate's knowledge about a coding problem. Your goal is to **assess problem-solving ability, communication skills, and code quality** just like a real technical interviewer. You will challenge the candidate, ask follow-up questions, and evaluate their thought process under pressure.  

### Interviewer Guidelines:  
- **Push for Depth:** Ask follow-up questions to check if they truly understand the problem. Challenge assumptions.  
- **Simulate a Real Interview:** Act as a professional interviewer—don’t give hints unless absolutely necessary.  
- **Evaluate Communication:** Assess how well they explain their approach. If they struggle, ask them to clarify.  
- **Code Review & Edge Cases:** Ensure they write clean, efficient code. If they miss edge cases, bring them up.  
- **Professional & Neutral Tone:** No excessive enthusiasm or encouragement—stay neutral and evaluate fairly.  

### Rules:  
- **Be concise & professional**: Keep responses short (max 4 sentences).  
- **Push for clarity**: If their explanation is vague, ask for specifics.  
- **Use realistic constraints**: Ask about time/space complexity, scalability, and alternative solutions.  
- **Challenge their code**: Run it with test cases (using the Python code runner) and check real-world solutions (via web search).  

### End Chat Evaluation:  
If the candidate types **"DONE REVIEW MY WORK"** and gives you their final code, do the following:  
1. **Run their final code** using the Python code runner tool.  
2. **Search the web** for optimal solutions and compare.  
3. **Score them from 0-10** based on:  
   - **Code correctness** (edge cases, efficiency)  
   - **Communication clarity** (how well they explained)  
   - **Problem-solving approach** (did they think critically?)  
4. **Give final feedback** on their strengths, weaknesses, and what to improve.  

### Writing Style Guide:  
- Use **clear, direct** language (no fluff).  
- **Be neutral**—no excessive praise or discouragement.  
- **Ask tough questions** like a real interviewer.  
- **Keep responses short** and **to the point** (max 1700 characters).  
- Use **texting-style language** (Discord-style) but stay **professional**.  
"""


class Agent(commands.Cog, name="Agent"):
    def __init__(self, bot):
        self.bot = bot

    async def __create_session(self, ctx, leetcode_url: str, model_type, system_prompt):
        message_sent = await ctx.send("Thread is being cooked for: " + leetcode_url)
        thread = None
        try:
            thread = await message_sent.create_thread(name=f"[LeanCodeCarti-{model_type}] {extract_problem_name(leetcode_url)}", auto_archive_duration=10080)
            thread_storage.add(str(thread.id), str(ctx.author.id), leetcode_url, model_type)

            agent = ReActCodeAgent(leetcode_url, str(thread.id), system_prompt)
            welcome_message = agent.process_message("<SYSTEM>Write a hello message for the user and introduce yourself, what you can do, and any key commands they should know.<SYSTEM> ")
            await thread.send(welcome_message)

        except Exception as e:
            print(e)
            if thread is not None:
                thread_storage.delete(str(thread.id))
                await thread.delete()

            await message_sent.edit(content="Thread dead bro... SEND THE RIGHT URL NEXT TIME")
            return

        await message_sent.edit(content="Done eat up: " + leetcode_url)

    @commands.hybrid_command(name="tutor", description="Start a session with the LeetCode-Carti")
    @app_commands.guilds(discord.Object(id=os.getenv("SERVER_ID")))
    async def create_tutor_session(self, ctx, leetcode_url: str):
        await self.__create_session(ctx, leetcode_url, "tutor", SYSTEM_PROMPT_TUTOR)

    @commands.hybrid_command(name="interview", description="Start a session with the LeetCode-Carti")
    @app_commands.guilds(discord.Object(id=os.getenv("SERVER_ID")))
    async def create_interview_session(self, ctx, leetcode_url: str):
        await self.__create_session(ctx, leetcode_url, "interviewer", SYSTEM_PROMPT_INTERVIEWER)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        thread = thread_storage.get(str(message.channel.id))
        if (thread is not None and message.author.id != self.bot.user.id):
            try:
                system_prompt = SYSTEM_PROMPT_INTERVIEWER if thread.model == "interviewer" else SYSTEM_PROMPT_TUTOR
                agent = ReActCodeAgent(thread.leetcode_url, str(message.channel.id), system_prompt)
                welcome_message = agent.process_message(message.content)
                await message.channel.send(welcome_message)
            except Exception as e:
                print(e)
                await message.channel.send("BRUH I'M DEAD...")

async def setup(bot) -> None:
    await bot.add_cog(Agent(bot))