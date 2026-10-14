import time
import asyncio
import random


async def fetch_data(param: int) -> str:
    print(f"Do something with {param}...")
    await asyncio.sleep(param)
    print(f"Done with {param}")
    return f"Result of {param}"


async def main():

    task_list = []
    for i in range(1, 50):
        random_num = random.randint(20, 25)
        task = asyncio.create_task(fetch_data(random_num))
        task_list.append(task)

    for task in task_list:
        result = await task
        print(result)


t1 = time.perf_counter()

results = asyncio.run(main())
print(results)

t2 = time.perf_counter()

print(f"Finished in {t2 - t1:.2f} seconds")
