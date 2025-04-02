import os
import redis
import json
from dotenv import load_dotenv

load_dotenv() 

class ThreadData:
    def __init__(self, users, leetcode_url):
        self.users = users
        self.leetcode_url = leetcode_url

class RedisThreadStorage:
    def __init__(self):
        self.redis = redis.Redis.from_url(os.getenv("REDIS_URL"))
    
    def __create_key(self, key):
        return f"thread${key}"

    def delete(self, thread_id: str) -> bool:
        is_deleted = self.redis.delete(self.__create_key(thread_id))
        if is_deleted:
            return True
        return False

    def add(self, thread_id: str, user_id: str, leetcode_url: str) -> bool:
        data = {
            "users": [user_id],
            "leetcode_url": leetcode_url
        }

        return self.redis.set(self.__create_key(thread_id), json.dumps(data))

    def get(self, thread_id: str) -> ThreadData | None:
        data = self.redis.get(self.__create_key(thread_id))
        if not data:
            return None
        json_data = json.loads(str(data, "utf-8"))
        return ThreadData(json_data["users"], json_data["leetcode_url"])
