import typing as tp
import redis
import json
import random
import time
import uuid

def generate_json(N: int = 2 * 10**6) -> tp.List[dict]:
    res = []
    for i in range(N):
        res.append({
            "name": str(uuid.uuid1()),
            "age": random.randint(0, 100),
            "id": i,
            "sex": "male" if random.random() < 0.5 else "female",
        })
    return res

# connect
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

TRIES = 10000

objs = generate_json(TRIES)

print('SET All:')
# string
s = time.time()
for obj in objs:
    i = random.randint(0, 200_000)
    r.delete(f'string:{i}')
    r.set(f'string:{i}', json.dumps(obj))
f = time.time()
print(f'string: {(f - s) * 1000 / TRIES:.3f}ms per request')

# hset
s = time.time()
for obj in objs:
    i = random.randint(0, 200_000)
    r.hdel(f'hset:{i}', *obj.keys())
    r.hset(f'hset:{i}', mapping=obj)
f = time.time()
print(f'hset: {(f - s) * 1000 / TRIES:.3f}ms per request')

# list
s = time.time()
for obj in objs:
    i = random.randint(0, 200_000)
    r.lpop(f'list:{i}', len(obj))
    r.lpush(f'list:{i}', *obj.values())
f = time.time()
print(f'list: {(f - s) * 1000 / TRIES:.3f}ms per request')

# zset
s = time.time()
for obj in objs:
    i = random.randint(0, 200_000)
    r.zrem(f'zset:{i}', *range(5))
    r.zadd(f'zset:{i}', mapping={
        f"{el}:{obj[el]}": j for j, el in enumerate(obj)
    })

f = time.time()
print(f'zset: {(f - s) * 1000 / TRIES:.3f}ms per request')


print()


print('SET Field:')
# string
s = time.time()
for _ in range(TRIES):
    i = random.randint(0, 200_000)
    el = json.loads(r.get(f'string:{i}'))
    el['name'] = obj['name']
    r.set(f'string:{i}', json.dumps(el))
f = time.time()
print(f'string: {(f - s) * 1000 / TRIES:.3f}ms per request')

# hset
s = time.time()
for _ in range(TRIES):
    i = random.randint(0, 200_000)
    el = r.hset(f'hset:{i}', 'name', obj['name'])
f = time.time()
print(f'hset: {(f - s) * 1000 / TRIES:.3f}ms per request')

# list
s = time.time()
for _ in range(TRIES):
    i = random.randint(0, 200_000)
    r.lpop(f'list:{i}', 1)
    r.lpush(f'list:{i}', obj['name'])
f = time.time()
print(f'list: {(f - s) * 1000 / TRIES:.3f}ms per request')

# zset
s = time.time()
for _ in range(TRIES):
    i = random.randint(0, 200_000)
    el = r.zadd(f'zset:{i}', {f'name:{obj["name"]}': 0})
f = time.time()
print(f'zset: {(f - s) * 1000 / TRIES:.3f}ms per request')
