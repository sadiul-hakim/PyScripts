import asyncio
import random
import time

async def work(w_id: int) -> None:
    print(f"Worker {w_id} started working....")
    time = random.uniform(0,2)
    await asyncio.sleep(time)
    print(f"Worker {w_id} done working in {time} sec...")

async def main():
    await asyncio.gather(
        *(work(i) for i in range(1,100001)),
        return_exceptions = True
    )

if __name__ == "__main__":
    start_time = time.perf_counter()
    asyncio.run(main())

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print(f"Elapsed time: {elapsed_time:.2f} sec")
