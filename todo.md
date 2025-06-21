Create CDN gif tool for llm
- https://www.reddit.com/r/CartiCulture/comments/1h5zy6g/which_song_had_the_best_music_video/
- Need to make this it own tool

Just a junk file for things todo and resources, nothing really important

FUTURE TODO
- Allow image uploading via user
- Clean up dead threads when the are achieved (do this via webhooks and redis)
- Connect to user leetcode account to get their submissions and problem history
- Do ranking system for cs club
- Add deep research, take weblink and convert into markdown for llm to read


LAST TODO
- [x] Create logger: 
  - https://stackoverflow.com/questions/6386698/how-to-write-to-a-file-using-the-logging-python-module
  - https://docs.python.org/3/howto/logging.html
- [x] Create Python code runner server
- [x] Bring over and run own docker instance of leetcode api as a service
- [x] Create docker deployment script
- [x] Add more memes to funny commands
- [x] Play with prompt (create tutor and interview role play)
- [x] Send to kobe and other people on server

Links
- https://langchain-ai.github.io/langgraph/reference/graphs/?h=compiledgraph#langgraph.graph.graph.CompiledGraph.stream
- https://stackoverflow.com/questions/43274476/is-there-a-way-to-check-if-a-subprocess-is-still-running
- https://langchain-ai.github.io/langgraph/tutorials/introduction/#part-1-build-a-basic-chatbot
- https://python.langchain.com/docs/tutorials/agents/#define-tools

Saved Links
https://pypi.org/project/discord-webhook/
https://docs.python.org/3/library/urllib.parse.html
https://github.com/matthewwithanm/python-markdownify
https://pypi.org/project/requests/
https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html
https://redis.readthedocs.io/en/stable/index.html
https://discordpy.readthedocs.io/en/stable/api.html?highlight=create_thread#discord.Message.channel
https://langchain-ai.github.io/langgraph/concepts/memory/#summarizing-past-conversations
https://github.com/openai/gpt-discord-bot/blob/main/src/utils.py
https://github.com/kkrypt0nn/Python-Discord-Bot-Template/blob/main/bot.py
https://www.interviewcoder.co/#pricing
https://langchain-ai.github.io/langgraph/how-tos/persistence_redis/#define-imports-and-helper-functions
https://github.com/alfaarghya/alfa-leetcode-api?tab=readme-ov-file
https://docs.python.org/3/library/subprocess.html
https://langchain-ai.github.io/langgraph/prebuilt/#available-libraries
https://python.langchain.com/docs/how_to/custom_tools/
https://python.langchain.com/docs/tutorials/agents/#define-tools


https://www.reddit.com/r/MachineLearning/comments/1b5gyy3/p_need_help_finetuning_a_llm_to_act_as_an_ai/
https://yzy-twts.com/
https://medium.com/aiprompts/turn-your-chat-gpt-into-ye-with-one-prompt-9ddfc2e55bc8

Prompting
- https://www.reddit.com/r/ChatGPT/comments/160v556/what_is_the_best_way_to_prompt_chatgpt_to_tutor/
- https://www.lewis-lin.com/blog/chatgpt-prompt-for-an-ai-tutor
- https://medium.com/@anferneeck/ultimate-prompting-guide-to-using-chatgpt-for-learning-596911742d8a
- https://sites.psu.edu/kent/2024/10/30/chatgpt-prompt-for-tutoring/
- Typically, a default temperature setting for ChatGPT would be around 0.7 (try 0.5)

Model compare agents
- https://machine-learning-made-simple.medium.com/gpt-vs-claude-vs-gemini-for-agent-orchestration-b3fbc584f0f7
- https://www.promptingguide.ai/research/llm-agents

How to do tooling
- Add in https://brave.com/search/api/
- Scrape content of website: https://jina.ai/reader/

Rewrite bot to be class base
- https://github.com/kkrypt0nn/Python-Discord-Bot-Template/blob/main/bot.py#L210

Pull from leetcode
-  https://github.com/alfaarghya/alfa-leetcode-api

How to run code
- https://github.com/judge0/judge0/blob/master/docker-compose.yml
 
Create tools for agent
- Web search
- Content grab
- Run code
- Create simple system prompt

Optional
- Different speech types (funny optional, talk like carti, kanye, sleep joe, chad trump), just a prompt thing
- Save to memory
- Pull from memory
- Code run window (off load to website)

NOTE
- Create a class for each json file type for parsing
- Don't worry about cleaning / achieve threads yet
- Don't worry about rate limiting
- Don't worry about citing website
- Just get it to work
- Move redis connection to be saved into bot
- Move openai connection to saved into bot
- Steel docker image from them
- Just put on main server
- NOTE: Have to write everything in one single file, to not have to deal with package issues