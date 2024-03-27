import typing as tp
import redis
import time
import random
import json
import uuid


def time_it(func: tp.Callable, *args, **kwargs) -> None:
    s = time.time()
    func(*args, **kwargs)
    f = time.time()
    print(f'took {(f - s) * 1000:.3f}ms')


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

def as_list(r: redis.Redis, objs: tp.List[dict]) -> None:
    for i, obj in enumerate(objs):
        r.lpush(f'list:{i}', *obj.values())


def as_zset(r: redis.Redis, objs: tp.List[dict]) -> None:
    for i, obj in enumerate(objs):
        r.zadd(f'zset:{i}', mapping={
            f"{el}:{obj[el]}": j for j, el in enumerate(obj)
        })


def as_string(r: redis.Redis, objs: tp.List[dict]) -> None:
    for i, obj in enumerate(objs):    
        r.set(f'string:{i}', json.dumps(obj))


def as_hset(r: redis.Redis, objs: tp.List[dict]) -> None:
    for i, obj in enumerate(objs):
        r.hset(f'hset:{i}', mapping=obj)


# connect
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# create json file
objs = generate_json(200_000)

with open('xxx.json', 'w') as f:
    json.dump(objs, f)

# test storage options
print('\nstring: ', end='')
time_it(as_string, r, objs)

print('\nhset: ', end='')
time_it(as_hset, r, objs)

print('\nlist: ', end='')
time_it(as_list, r, objs)

print('\nzset: ', end='')
time_it(as_zset, r, objs)
