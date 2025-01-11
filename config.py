import os

AUTH_TOKEN = os.getenv("AUTH_TOKEN", "default_token")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))