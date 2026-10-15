import asyncio
import random
import time


async def producer(queue):
    """Create jobs and put them into the queue."""
    for job_id in range(1, 21):
        await queue.put(job_id)
        print(f"Produced job {job_id}")

    # Tell every worker that no more jobs are coming.
    for _ in range(4):
        await queue.put(None)


async def worker(worker_id: int, queue):
    """Take jobs from the queue and process them."""
    while True:
        job = await queue.get()

        try:
            if job is None:
                print(f"Worker {worker_id}: stopping")
                return

            print(f"Worker {worker_id}: processing job {job}")

            # Simulate I/O work, such as waiting for an API.
            await asyncio.sleep(random.uniform(0.5, 2.0))

            print(f"Worker {worker_id}: completed job {job}")

        finally:
            queue.task_done()


async def main():
    queue = asyncio.Queue()

    workers = [asyncio.create_task(worker(i, queue)) for i in range(4)]

    # Start the producer.
    await producer(queue)

    await queue.join()

    await asyncio.gather(*workers, return_exceptions=True)


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - start
    print(f"\nTotal execution time: {elapsed:.2f}s")
