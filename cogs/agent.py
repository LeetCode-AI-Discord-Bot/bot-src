import os
import discord
from discord.ext import commands
from discord import app_commands 
from dotenv import load_dotenv

load_dotenv() 

from src.react_code_agent import ReActCodeAgent
from src.logger import logger
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

GIFs:
Use this list of gifs add more life to your conversion with the student (Each gif is label on what they are suppose to represent). Don't add a gif to every message. Only use one gif in your message. Add the link of the gif in your message to use it in your final response. Lastly you can also send a link by itself as your response to have the same meaning of what you are going to response with.

- Happy or Good job: https://media1.tenor.com/m/EwLmp-kB1n4AAAAd/playboi-carti-playboi.gif
- Bad or I cannot do that: https://media1.tenor.com/m/jAShXlQZltoAAAAC/playboi-carti.gif
- Important or key information: https://media.tenor.com/8JE0JHUZj6cAAAAi/speech-bubble.gif
- Hope: https://media.tenor.com/WYrco-rfWr8AAAAM/smile.gif
- Friendship: https://giphy.com/gifs/playboicarti-UFt9TE8mmHlnt4MmWE
- Disagreement:  https://leetcode.com/problems/two-sum/description/
- Confuse: https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExNnJkeThzY2RjNHZlaGg2d2FkZzkwdjgzMGg1cHVwbGk2bnc5dmxtNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/PahKgDncvjzWNtTE0V/giphy.gif
- Great Job: https://i.pinimg.com/originals/07/f6/30/07f6305407e4a06afbf7c9f19baca748.gif 
- Mind blown: https://media1.tenor.com/m/EepPdMy2rbAAAAAd/shocked-ishowspeed.gif
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
        logger.info(f"[AGENT] Create new thread | leetcode url = {leetcode_url} | user id = {ctx.author.id}")
        message_sent = await ctx.send("Thread is being cooked for: " + leetcode_url)
        thread = None
        try:
            thread = await message_sent.create_thread(name=f"[LeanCodeCarti-{model_type}] {extract_problem_name(leetcode_url)}", auto_archive_duration=10080)
            thread_storage.add(str(thread.id), str(ctx.author.id), leetcode_url, model_type)

            agent = ReActCodeAgent(leetcode_url, str(thread.id), system_prompt)
            welcome_message = agent.process_message("<SYSTEM>Write a hello message for the user and introduce yourself, what you can do, and any key commands they should know.<SYSTEM> ")
            await thread.send(welcome_message)

        except Exception as e:
            logger.error(f"[AGENT] Create new thread failed | error = {str(e)}")
            if thread is not None:
                thread_storage.delete(str(thread.id))
                await thread.delete()

            await message_sent.edit(content="Thread dead bro... SEND THE RIGHT URL NEXT TIME")
            return

        await message_sent.edit(content="Done eat up: " + leetcode_url)

    @commands.hybrid_command(name="tutor", description="Start a session with the LeetCode-Carti")
    @app_commands.guilds(discord.Object(id=os.getenv("DISCORD_GUILD_ID")))
    async def create_tutor_session(self, ctx, leetcode_url: str):
        await self.__create_session(ctx, leetcode_url, "tutor", SYSTEM_PROMPT_TUTOR)

    @commands.hybrid_command(name="interview", description="Start a session with the LeetCode-Carti")
    @app_commands.guilds(discord.Object(id=os.getenv("DISCORD_GUILD_ID")))
    async def create_interview_session(self, ctx, leetcode_url: str):
        await self.__create_session(ctx, leetcode_url, "interviewer", SYSTEM_PROMPT_INTERVIEWER)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        thread = thread_storage.get(str(message.channel.id))
        if (thread is not None and message.author.id != self.bot.user.id):
            logger.info(f"[AGENT] Create response message | message = {message.content} | thread id = {message.channel.id} | user id = {message.author.id}")
            try:
                system_prompt = SYSTEM_PROMPT_INTERVIEWER if thread.model == "interviewer" else SYSTEM_PROMPT_TUTOR
                agent = ReActCodeAgent(thread.leetcode_url, str(message.channel.id), system_prompt)
                welcome_message = agent.process_message(message.content)
                await message.channel.send(welcome_message)
            except Exception as e:
                logger.error(f"[AGENT] Fail Create response message | message = {message.content} | thread id = {message.channel.id} | error = {str(e)}")
                await message.channel.send("BRUH I'M DEAD...")

async def setup(bot) -> None:
    await bot.add_cog(Agent(bot))