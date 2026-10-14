"""

main1 : asyncio.to_thread() — running synchronous functions in separate threads.
Best suited for : Blocking I/O

main2 : ProcessPoolExecutor with run_in_executor() — running synchronous functions in separate processes. A separate Python process executes the function. This can use multiple CPU cores for CPU-intensive Python code.
Best suited for : CPU-intensive calculations
"""

"""
| Method                   | When to use                                                                                                                                                         |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `asyncio.create_task()`  | Schedule a coroutine to run concurrently.                                                                                                                           |
| `asyncio.gather()`       | Run multiple awaitables concurrently and collect results in input order. Use `return_exceptions=True` to collect exceptions as results instead of propagating them. |
| `asyncio.TaskGroup()`    | Manage related tasks together. Automatically waits for all tasks on exit and cancels sibling tasks if one fails. Best for structured concurrency.                   |
| `asyncio.to_thread()`    | Run a blocking synchronous function in a worker thread, mainly for I/O-bound work.                                                                                  |
| `loop.run_in_executor()` | Run synchronous work in a thread or process pool; useful when you need to choose the executor explicitly.                                                           |
| `ProcessPoolExecutor`    | Run CPU-heavy Python functions in separate processes for potential parallel execution.                                                                              |
| `await`                  | Wait for an awaitable's result while letting the event loop run other tasks.                                                                                        |

Quick rule of thumb:

- Multiple async API calls → `asyncio.gather()`
- Related tasks that should finish as a group → `asyncio.TaskGroup()`
- Schedule one coroutine in the background → `asyncio.create_task()`
- Blocking I/O function → `asyncio.to_thread()`
- CPU-intensive calculations → `ProcessPoolExecutor`

Important: `gather()` and `TaskGroup()` are not alternatives to threads or processes; they coordinate asynchronous tasks. You can combine them with `to_thread()` when needed.
"""

"""
| Behavior                     | `asyncio.gather()`                                              | `asyncio.TaskGroup()`                                   |
| ---------------------------- | --------------------------------------------------------------- | ------------------------------------------------------- |
| One task raises an exception | Propagates the first exception by default                       | Cancels the remaining tasks                             |
| Other tasks                  | Usually continue running                                        | Cancelled and awaited before exiting the group          |
| Error handling               | Other tasks may still be running after the exception propagates | Group waits for tasks to finish or cancel               |
| Exceptions                   | Typically propagates one exception                              | Raises an `ExceptionGroup` containing the task failures |

In short:

- `gather()` — if one task fails, reports the error but does not automatically cancel the other tasks.
- `TaskGroup()` — if one task fails, cancels the remaining tasks and waits for them to finish cleaning up.

Note: `gather(return_exceptions=True)` collects exceptions as results instead of propagating them immediately. `TaskGroup` is generally preferable when tasks are related and should succeed or fail together.
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
