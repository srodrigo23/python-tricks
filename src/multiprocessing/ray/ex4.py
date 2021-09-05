# Slow approach.
import ray, time

@ray.remote
def add(x, y):
    time.sleep(1)
    return x + y

values = [1, 2, 3, 4, 5, 6, 7, 8]
while len(values) > 1:
    values = [add.remote(values[0], values[1])] + values[2:]
result = ray.get(values[0])
print(result)

# Fast approach.
values = [1, 2, 3, 4, 5, 6, 7, 8]
while len(values) > 1:
    values = values[2:] + [add.remote(values[0], values[1])]
result = ray.get(values[0])
print(result)