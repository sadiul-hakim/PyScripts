import asyncio
import json
from pathlib import Path

TASKS_FILE = Path(__file__).parent / "task_stream.log"

async def async_worker(name: str, queue: asyncio.Queue):
	while True:
		task = await queue.get()
		print(f"[{name}] Starting: '{task['text']}' from {task['producer']}")
		
		await asyncio.sleep(1)
		
		print(f"[{name}] Done: '{task['text']}'")
		queue.task_done()

async def file_tailer(queue: asyncio.Queue):
	TASKS_FILE.touch(exist_ok=True)
	
	with open(TASKS_FILE, "r", encoding="utf-8") as f:
		f.seek(0, 2)
		
		while True:
			line = f.readline()
			if not line:
				await asyncio.sleep(0.2)
				continue
			try:
				task_data = json.loads(line.strip())
				await queue.put(task_data)
			except json.JSONDecodeError:
				continue

async def main():
	queue = asyncio.Queue()
	
	workers = [
		asyncio.create_task(async_worker(f"Worker-{i}", queue))
		for i in range(1,4)
	]

	print("=== Worker Engine Running (Listening for Producer inputs) ===")
	await file_tailer(queue)

if __name__ == "__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print("\nWorker engine stopped.")
