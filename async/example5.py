import time
import asyncio


async def fetch_data(param: int) -> str:
    print(f"Do something with {param}...")
    time.sleep(param)
    print(f"Done with {param}")
    return f"Result of {param}"


async def main():
    task1 = asyncio.create_task(
        fetch_data(1)
    )  # This schedules the task and runs the function
    task2 = asyncio.create_task(fetch_data(3))

    result2 = await task2  # await makes the process wait here until all done
    print("Fetch 2 fully completed")
    result1 = await task1
    print("Fetch 1 fully completed")

    return [result1, result2]


t1 = time.perf_counter()

results = asyncio.run(main())
print(results)

t2 = time.perf_counter()

print(f"Finished in {t2 - t1:.2f} seconds")
