import os
import secrets
import string

import redis

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWD = os.getenv("REDIS_PASSWD")


def generate_key(length):
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))


redis_client = redis.Redis(
    host=REDIS_HOST,
    port=int(REDIS_PORT),
    db=0,
    password=REDIS_PASSWD,
)

for _ in range(100):
    key = generate_key(32)

    print(key)

    redis_client.set(f"keys:{key}", 1)
