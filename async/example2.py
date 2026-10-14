import time
import asyncio


async def fetch_data(param: int) -> str:
    print(f"Do something with {param}...")
    await asyncio.sleep(param)
    print(f"Done with {param}")
    return f"Result of {param}"


async def main():
    task1 = fetch_data(
        1
    )  # function call just returned a coroutine object, did not run the code
    task2 = fetch_data(2)
    result1 = await task1
    print("Fetch 1 fully completed")
    result2 = await task2
    print("Fetch 2 fully completed")
    return [result1, result2]


t1 = time.perf_counter()

results = asyncio.run(main())
print(results)

t2 = time.perf_counter()

print(f"Finished in {t2 - t1:.2f} seconds")
