import asyncio
from pathlib import Path
import aiofiles
import time

path = Path(__file__).parent / "async_file.txt"
lock = asyncio.Lock()

async def update_file(text: str) -> None:
	async with lock:
		async with aiofiles.open(path,"a",encoding="utf-8") as file:
			await file.write(text)

async def main():
	results = await asyncio.gather(*(update_file(f"{i}. Hakim\n") for i in range(1,50001)),return_exceptions=True)
	for i,res in enumerate(results,1):
		if isinstance(res, Exception):
			print(f"Task {i} failed with error: {res}")

if __name__ == "__main__":
	start_time = time.perf_counter()
	asyncio.run(main())
	end = time.perf_counter()
	elapsed_time = time.perf_counter() - start_time
	print(f"Elapsed time: {elapsed_time:.6f} seconds")
