"""

main1 : asyncio.to_thread() — running synchronous functions in separate threads.
Best suited for : Blocking I/O

main2 : ProcessPoolExecutor with run_in_executor() — running synchronous functions in separate processes. A separate Python process executes the function. This can use multiple CPU cores for CPU-intensive Python code.
Best suited for : CPU-intensive calculations
"""

import time
import asyncio
from concurrent.futures import ProcessPoolExecutor


def fetch_data(param: int) -> str:
    print(f"Do something with {param}...", flush=True)
    time.sleep(param)
    print(f"Done with {param}")
    return f"Result of {param}"


async def main():
    task1 = asyncio.create_task(
        asyncio.to_thread(fetch_data, 1)
    )  # This schedules the task and runs the function
    task2 = asyncio.create_task(asyncio.to_thread(fetch_data, 2))

    result1 = await task1
    print("Thread 1 fully completed")
    result2 = await task2  # await makes the process wait here until all done
    print("Thread 2 fully completed")

    return [result1, result2]


async def main2():
    loop = asyncio.get_running_loop()

    with ProcessPoolExecutor() as executor:
        task1 = loop.run_in_executor(executor, fetch_data, 1)
        task2 = loop.run_in_executor(executor, fetch_data, 2)

        result1 = await task1
        print("Process 1 fully completed")
        result2 = await task2  # await makes the process wait here until all done
        print("Process 2 fully completed")

        return [result1, result2]


if __name__ == "__main__":
    t1 = time.perf_counter()

    results = asyncio.run(main())
    print(results)

    t2 = time.perf_counter()

    print(f"Finished in {t2 - t1:.2f} seconds")
