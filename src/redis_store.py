import os
import redis
from dotenv import load_dotenv
load_dotenv()

# Store redis connection
redis_store = redis.Redis.from_url(os.getenv("REDIS_URL"))