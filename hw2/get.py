import typing as tp
import redis
import json
import random
import time

# connect
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

TRIES = 10000

print('GET All:')
# string
s = time.time()
for _ in range(TRIES):
    i = random.randint(0, 200_000)
    el = json.loads(r.get(f'string:{i}'))
f = time.time()
print(f'string: {(f - s) * 1000 / TRIES:.3f}ms per request')

# hset
s = time.time()
for _ in range(TRIES):
    i = random.randint(0, 200_000)
    el = r.hgetall(f'hset:{i}')
f = time.time()
print(f'hset: {(f - s) * 1000 / TRIES:.3f}ms per request')

# list
s = time.time()
for _ in range(TRIES):
    i = random.randint(0, 200_000)
    el = r.lrange(f'list:{i}', 0, 5)
f = time.time()
print(f'list: {(f - s) * 1000 / TRIES:.3f}ms per request')

# zset
s = time.time()
for _ in range(TRIES):
    i = random.randint(0, 200_000)
    el = r.zrange(f'zset:{i}', 0, 5)
f = time.time()
print(f'zset: {(f - s) * 1000 / TRIES:.3f}ms per request')


print()


print('GET Field:')
# string
s = time.time()
for _ in range(TRIES):
    i = random.randint(0, 200_000)
    el = json.loads(r.get(f'string:{i}'))
    el['name']
f = time.time()
print(f'string: {(f - s) * 1000 / TRIES:.3f}ms per request')

# hset
s = time.time()
for _ in range(TRIES):
    i = random.randint(0, 200_000)
    el = r.hget(f'hset:{i}', 'name')
f = time.time()
print(f'hset: {(f - s) * 1000 / TRIES:.3f}ms per request')

# list
s = time.time()
for _ in range(TRIES):
    i = random.randint(0, 200_000)
    el = r.lrange(f'list:{i}', 0, 1)[0]
f = time.time()
print(f'list: {(f - s) * 1000 / TRIES:.3f}ms per request')

# zset
s = time.time()
for _ in range(TRIES):
    i = random.randint(0, 200_000)
    el = r.zrange(f'zset:{i}', 0, 1)
f = time.time()
print(f'zset: {(f - s) * 1000 / TRIES:.3f}ms per request')
