import queue
import threading
import time
from pathlib import Path

write_queue = queue.Queue()

def disk_writer_thread(filepath: str):
    with open(filepath, "a", encoding="utf-8") as f:
        while True:
            chunk = write_queue.get()
            if chunk is None:  # Shutdown signal
                write_queue.task_done()
                break
            
            # Drain whatever else is waiting to do one large batched write
            batch = [chunk]
            while not write_queue.empty():
                try:
                    batch.append(write_queue.get_nowait())
                except queue.Empty:
                    break
            
            f.writelines(batch)
            for _ in batch:
                write_queue.task_done()

path = Path(__file__).parent / "thread_file.txt"
# Start background thread
t = threading.Thread(target=disk_writer_thread, args=(path,), daemon=True)
t.start()

start_time = time.perf_counter()

# Producers push data without waiting on disk:
for i in range(50000):
    write_queue.put(f"{i}. Data\n")

# Wait to finish and clean up
write_queue.join()
write_queue.put(None)
t.join()

elapsed_time = time.perf_counter() - start_time
print(f"Elapsed time: {elapsed_time:.6f} seconds")
