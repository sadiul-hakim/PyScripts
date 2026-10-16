import asyncio

"""
In an async system, you don't want the chefs sitting idle doing nothing while waiting for all 8 orders to arrive. As soon as the first order hits the conveyor belt, a chef grabs it and starts cooking immediately while the waiter goes to take the next order.

### How the Event Loop Switched Between Them:

1. **`asyncio.create_task(...)` starts the chefs immediately:**
When you called `asyncio.create_task()`, Hakim and Hasan were scheduled in the background. Both reached `await queue.get()`, saw the queue was empty, and went to sleep waiting for items.
2. **The Waiter drops Pizza:**
The waiter printed `Taking order for Pizza....` and put `Pizza` into the queue.


3. **The `await asyncio.sleep(0.2)` yield:**
Right after dropping Pizza, the waiter called `await asyncio.sleep(0.2)`. By awaiting `sleep`, the waiter paused and **handed control back to the event loop**.
4. **Hakim wakes up:**
The event loop saw the waiter was sleeping and noticed Hakim was waiting for an item. The queue now had `Pizza`, so Hakim woke up, grabbed it, and started cooking!



---

### What If You *Want* the Waiter to Finish Everything First?

If your specific goal is for the waiter to take all 8 orders before any chef begins cooking, do not start the chefs until the waiter has finished:

```python
async def main():
    queue = asyncio.Queue()

    # 1. Waiter finishes completely first
    await waiter(queue)

    # 2. Add shutdown signals
    await queue.put(None)
    await queue.put(None)

    # 3. Only now create and start the chefs
    chef1 = asyncio.create_task(chef("Hakim", queue))
    chef2 = asyncio.create_task(chef("Hasan", queue))

    await queue.join()
    await asyncio.gather(chef1, chef2)

```

"""

async def chef(name: str, queue: asyncio.Queue):
    while True:
        dish = await queue.get()

        if dish is None:
            queue.task_done()
            print(f"[{name}] Shift finished. Going home.")
            break

        print(f"[{name}] Cooking {dish}.....")
        await asyncio.sleep(1)
        print(f"[{name}] Finished {dish}!")

        queue.task_done()

async def waiter(queue: asyncio.Queue):
    dishes = ["Pizza", "Burger", "Pasta", "Salad", "Steak", "Meat Balls", "Sandwitch", "Cookies"]
    for dish in dishes:
        print(f"[Waiter] Taking order for {dish}....")
        await queue.put(dish)
        await asyncio.sleep(0.2)

async def main():
    queue = asyncio.Queue()

    chef1 = asyncio.create_task(chef("Hakim",queue))
    chef2 = asyncio.create_task(chef("Hasan",queue))
    await waiter(queue)

    await queue.put(None)
    await queue.put(None)

    await queue.join()
    results = await asyncio.gather(chef1, chef2, return_exceptions = True)

    for result in results:
        if isinstance(result,Exception):
            print(result)

if __name__ == "__main__":
    asyncio.run(main())
