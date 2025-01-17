import os
import time
import json
import threading
from dotenv import load_dotenv
load_dotenv()

import redis

redis_store = redis.Redis.from_url(os.getenv("REDIS_URL"))

def queue_processing():
    while True:
        if redis_store.llen("AI_CHAT_QUEUE") > 0:
            session = redis_store.lpop("AI_CHAT_QUEUE")
            session = json.loads(session)
            print(session)

        time.sleep(10)

queue_processing_thread = threading.Thread(target=queue_processing)