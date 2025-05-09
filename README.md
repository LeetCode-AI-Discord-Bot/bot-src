<p align="center">
  <img src="./assets/carti-cash-carti.gif" width="300px">
</p>

# PLU LeetCode Discord Bot 

*(Also know as leencode-carti)*

## Table of Contents

- [PLU LeetCode Discord Bot](#plu-leetcode-discord-bot)
  - [Table of Contents](#table-of-contents)
  - [Overview of The Project](#overview-of-the-project)
  - [Env Variables](#env-variables)
  - [Setup For Local Development](#setup-for-local-development)
    - [Step 1 (Env Variables)](#step-1-env-variables)
    - [Step 2 (Docker)](#step-2-docker)
    - [Step 3 (Setup Python Environment)](#step-3-setup-python-environment)
    - [Step 4 (Run Bot)](#step-4-run-bot)
  - [Production](#production)

##  Overview of The Project

Create a Discord bot to help people with LeetCode and technical interview prep using GPT-4 
(or possibly Google AI models or any LLM model). It would be similar to how Dr. Cao's bot 
works, but with improvements and prompt adjustments. 

The bot should be able to provide examples and hints based on what the user inputs, whether 
in the form of text, code, or images. It should also be capable of holding a text conversation, 
similar to ChatGPT.

Additionally, since this is a Discord bot, it will use threads to organize communication between 
itself and users. Using threads will improve communication and organization, making it easier 
for users to find previous messages and enabling more collaborative work.

##  Env Variables

These are the environment variables required to be defined before running the bot server:

- `DISCORD_BOT_TOKEN`: The bot token from the Discord Developer Portal
- `REDIS_URL`: The connection string to the Redis database
- `DISCORD_GUILD_ID`: The server ID (not the channel ID) of the Discord server
- `OPENAI_API_KEY`: The API OpenAI
- `LEETCODE_API_KEY`: The API key for LeetCode API
- `TAVILY_API_KEY`: The API key for Tavily API
- `CODE_SERVER_URL`: The URL of the code server (use for running python code, Agent tooling)
- `IS_PRODUCTION`: Whether the bot is running in production (True or False)

**Note:** Instead of specifying the channel ID, the bot will use roles to determine which channels 
it can read from/write to. This makes it more scalable and easier to manage.

**Example**

```txt
DISCORD_BOT_TOKEN={bot token}
REDIS_URL={connection string to redis}
DISCORD_GUILD_ID={server id}
OPENAI_API_KEY={openai api key}
TAVILY_API_KEY={tavily api key}
LEETCODE_API_KEY={leetcode api key}
CODE_SERVER_URL={code server url}
IS_PRODUCTION={True or False}
```

If you need help setting up roles on discord please follow this guide:

https://zapier.com/blog/discord-roles/

If that is still confusing, DM Gabe.

**IMPORTANT: DON'T LEAK YOUR API KEYS OR SHARE THEM WITH ANYONE**

##  Setup For Local Development

These are the steps to setup the bot for local development (running on your local machine).

### Step 1 (Env Variables)

First make sure you have all the API keys define in the env variables.

- [OpenAI](https://openai.com/)
- [Discord Developer Dashboard](https://discord.com/developers/applications)
  - Other resources for understanding how to setup a discord bot:
    - https://www.youtube.com/watch?v=H98fj3gnYbw
    - https://www.youtube.com/watch?v=4IxLBKPVyXE
    - https://www.freecodecamp.org/news/create-a-discord-bot-with-javascript-nodejs/

For the server id, you can either create your own discord server or use a existing one. 
Just make sure you add the discord bot to the server.

**Copying server id:**

Basically right click on the server and copy the server id.

![](./assets/Screenshot%202025-01-23%20at%207.20.04 AM.png)

>[NOTE] For testing purposes, you may want to use your own server. But feel free to use 
>the public server. DM Gabe if you want to use the public server.

For the redis connection string, please define it as follows:

```txt
REDIS_URL=redis://localhost:6379
CODE_SERVER_URL=http://localhost:8000
```

This is only for local development purposes. This will not work in production.

### Step 2 (Docker)

Download and install Docker.

This project uses docker to manage our database used to store chat sessions. The database we are 
using is redis and to best install redis on your local machine is via docker.

Follow the link below and install docker for your machine. This does require you to restart your 
machine after installing.

>[NOTE] Don't make a account for docker desktop. This will mess everything up.

[Docker Download](./assets/Docker.png)

### Step 3 (Setup Python Environment)

Make sure to use python 3.13.1 or newer. (Honestly anything 3.12 should also work as well)

Run the following commands to create a local python environment. Do this at the root of the project. 
(Don't forget to clone the repo first and cd into it). All commands should be done at the root of 
the project.

```bash
python -m venv venv (Or use the one in VS Code)

source venv/bin/activate (Only for Mac and Linux)

.\venv\Scripts\activate.bat (Only for Windows)

pip install -r requirements.txt
```

**To exit out of the environment use this command:**

```bash
deactivate
```

>[NOTE]: If you are modifying the `remote-code-server` folder, you need to run these commands inside that folder

### Step 4 (Run Bot)

Before you can run the bot you need to run the database first (aka redis). To do that run the 
following command at the root of the project.

```bash
docker compose -f docker-compose.dev.yml up
```

This will download the latest version of redis and run it on the port 6379. Make sure the terminal 
doesn't give you any errors and says that redis is running.

Now you can run the bot.

```bash
python bot.py
```

>[NOTE]: If you are modifying the `remote-code-server` folder, you need to run these commands inside that folder. Also don't forget to run that as well, since `docker-compose.dev.yml` does not run that service.

>[NOTE] Make sure that you are still in the python environment. If you are not, go back to step 3 
>and activate it and run this command again

**Now you are all set up! Yay!**


## Production

Run this single command to run the bot in production.

```bash
docker compose up
```

Or add it to your own build system.

>[NOTE]: We are using coolify to manage our build to production
