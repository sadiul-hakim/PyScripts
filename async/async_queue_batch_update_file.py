import asyncio
from pathlib import Path
import time

path = Path(__file__).parent / "async_queue_batch_file.txt"

def sync_batch_write(lines: list[str]) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.writelines(lines)

async def file_writer(queue: asyncio.Queue) -> None:
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break

        batch = [item]
        queue.task_done()

        # Drain all items currently buffered in memory without waiting
        while not queue.empty():
            nxt = queue.get_nowait()
            if nxt is None:
                queue.task_done()
                await queue.put(None)
                break
            batch.append(nxt)
            queue.task_done()

        # One single write call for the entire batch
        await asyncio.to_thread(sync_batch_write, batch)

async def worker(queue: asyncio.Queue, text: str) -> None:
    await queue.put(text)

async def main():
    queue = asyncio.Queue()
    writer_task = asyncio.create_task(file_writer(queue))

    await asyncio.gather(*(worker(queue, f"{i}. Hakim\n") for i in range(1, 50001)))

    await queue.join()
    await queue.put(None)
    await writer_task

if __name__ == "__main__":
    start_time = time.perf_counter()
    asyncio.run(main())
    print(f"Elapsed time: {time.perf_counter() - start_time:.6f} seconds")
