import asyncio
import time

async def worker(name: str, queue: asyncio.Queue) -> None:
    while True:
        task = await queue.get()
        if task is None:
            queue.task_done()
            print(f"[{name}] Shutting down.")
            break

        # Simulate doing actual async work (e.g., network request, file processing)
        print(f"\n[{name}] Started processing: '{task}'")
        await asyncio.sleep(3)  # Simulates 3 seconds of background work
        print(f"\n[{name}] Completed: '{task}'")

        queue.task_done()

async def interactive_producer(queue: asyncio.Queue) -> None:
    print("=== Interactive Task Runner ===")
    print("Type any task and press Enter. Type 'exit' to quit.\n")

    while True:
        # Non-blocking input that does NOT freeze running workers
        user_input = await asyncio.to_thread(input, "Enter a task > ")
        clean_text = user_input.strip()

        if not clean_text:
            continue

        if clean_text.lower() == "exit":
            print("\nExiting input prompt. Waiting for remaining tasks to complete...")
            break

        # Push to queue immediately
        await queue.put(clean_text)
        print(f"-> Queued: '{clean_text}'")

async def main():
    queue = asyncio.Queue()

    # Launch 2 background consumers
    workers = [
        asyncio.create_task(worker("Worker-1", queue)),
        asyncio.create_task(worker("Worker-2", queue)),
    ]

    # Run the interactive producer in the foreground
    await interactive_producer(queue)

    # Signal all workers to exit once their work is done
    for _ in workers:
        await queue.put(None)

    # Wait for all queued work and sentinel values to be marked task_done
    await queue.join()
    await asyncio.gather(*workers)
    print("All tasks finished. Program closed.")

if __name__ == "__main__":
    asyncio.run(main())
