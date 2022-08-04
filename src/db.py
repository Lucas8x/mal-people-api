import os

import redis
from rq import Queue

conn = redis.Redis(
  host=os.getenv('REDIS_HOST', '127.0.0.1'),
  port=os.getenv('REDIS_PORT', 49153),
  password=os.getenv('REDIS_PASSWD', 'redispw'),
)

redis_queue = Queue(connection=conn)
