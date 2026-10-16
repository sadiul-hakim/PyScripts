import asyncio
from pathlib import Path
import aiofiles
import time

path = Path(__file__).parent / "async_queue_file.txt"

async def file_writer(queue: asyncio.Queue) -> None:
    # Keeps file open once instead of reopening it on every single write
    async with aiofiles.open(path, "a", encoding="utf-8") as file:
        while True:
            item = await queue.get()
            if item is None:  # Sentinel value signaling completion
                queue.task_done()
                break
            await file.write(item)
            queue.task_done()

async def worker(queue: asyncio.Queue) -> None:
    # Pushing to an asyncio.Queue in memory takes microseconds
	for i in range(1,50001):
		await queue.put(f"{i}. Hakim")

async def main():
    queue = asyncio.Queue()
    writer_task = asyncio.create_task(file_writer(queue))

    # All producers run concurrently without touching the disk directly
    await asyncio.gather(worker(queue), return_exceptions=True)

    # Wait for all writes to drain, then stop writer
    await queue.put(None)
    await queue.join()
    await writer_task

if __name__ == "__main__":
    start_time = time.perf_counter()
    asyncio.run(main())
    elapsed_time = time.perf_counter() - start_time
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
