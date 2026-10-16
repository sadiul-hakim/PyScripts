import json
import time
from pathlib import Path

TASKS_FILE = Path(__file__).parent / "task_stream.log"


def main():
    producer_id = f"Producer-{time.time_ns() % 1000}"
    print(f"=== {producer_id} Ready ===")
    print("Type a task and hit Enter. Type 'exit' to quit.\n")

    while True:
        task_text = input("Task > ").strip()
        if not task_text:
            continue
        if task_text.lower() == "exit":
            break

        payload = {
            "producer": producer_id,
            "text": task_text,
            "timestamp": time.time(),
        }

        # Appending to an open file is thread- and process-safe for single lines
        with open(TASKS_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")
            f.flush()

        print(f"Sent: {task_text}")


if __name__ == "__main__":
    main()
