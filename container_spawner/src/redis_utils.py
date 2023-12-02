import os
from uuid import uuid4

import redis
import requests

from .tools import get_secret

REDIS_HOST = os.getenv("REDIS_HOST", get_secret("REDIS_HOST"))
REDIS_PORT = int(os.getenv("REDIS_PORT", get_secret("REDIS_PORT")))
REDIS_PASSWD = os.getenv("REDIS_PASSWD", get_secret("REDIS_PASSWD"))

START_PORT = int(os.getenv("START_PORT", "1024"))

CONTAINER_QUOTA_PER_IP = int(os.getenv("CONTAINER_QUOTA_PER_IP", "5"))

NODE_PUB_IP = (
    requests.get("https://checkip.amazonaws.com", timeout=15)
    .content[:-1]
    .decode("utf-8")
)

HOUR_S = 3600
HOURS_AMMMOUNT = int(os.getenv("HOURS_AMMMOUNT", "1"))
CONTAINER_TIMEOUT = HOUR_S * HOURS_AMMMOUNT


class RedisUtils:
    def __init__(self):
        self.client = redis.Redis(REDIS_HOST, REDIS_PORT, password=REDIS_PASSWD)

    def count_keys(self, pattern) -> int:
        keys = self.client.keys(pattern)

        count = len(keys)

        return count

    def valid_ip_quota_atomic(self, ip) -> bool:
        """ """

        pattern = f"quota:{ip}:*"

        curr_ammount = self.count_keys(pattern)

        if curr_ammount >= CONTAINER_QUOTA_PER_IP:
            return False

        key = f"quota:{ip}:{str(uuid4())}"

        self.client.set(key, "1", ex=CONTAINER_TIMEOUT)

        return True

    def check_valid_key(self, usr_key) -> bool:
        """ """

        key = f"keys:{usr_key}"

        return self.client.get(key) is not None

    def get_next_port(self) -> int:
        """ """

        key = f"nodes:{NODE_PUB_IP}"

        if self.client.get(key) is None:
            self.client.set(key, START_PORT, 24 * 3600 * 7)

        return self.client.incr(key)
