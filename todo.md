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