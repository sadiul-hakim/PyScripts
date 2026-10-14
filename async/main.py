import asyncio
import time


def sync_function(test_param: str) -> str:
    print("This is a sync function")

    time.sleep(0.5)

    return f"Sync Result : {test_param}"


async def async_function(test_param: str) -> str:
    print("This is a async function")

    await asyncio.sleep(0.5)

    return f"Async Result : {test_param}"


async def main():
    # sync_result = sync_function("Test")
    # print(sync_result)

    # coroutine = async_function("Test")
    # print(coroutine)

    # coroutine_result = await coroutine
    # print(coroutine_result)

    task = asyncio.create_task(async_function("Test"))
    print(task)

    task_result = await task
    print(task_result)


if __name__ == "__main__":
    asyncio.run(main())
