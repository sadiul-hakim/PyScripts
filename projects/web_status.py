import asyncio
import time
import httpx


URLS = [
    "https://example.com",
    "https://www.python.org",
    "https://www.github.com",
    "https://httpbin.org/status/404",
]


async def check_status(client: httpx.AsyncClient, url: str) -> None:
    start = time.perf_counter()

    try:
        response = await client.get(url, timeout=10)

        elapsed = time.perf_counter() - start

        print(f"{response.status_code} | {elapsed:.2f}s | {url}")
    except httpx.TimeoutException:
        print(f"TIMEOUT | {url}")

    except httpx.RequestError as error:
        print(f"CONNECTION ERROR | {url} | {error}")


async def main() -> None:
    start = time.perf_counter()
    async with httpx.AsyncClient() as client:
        # It waits for the response while allowing the event loop to run other tasks.
        await asyncio.gather(
            *(check_status(client, url) for url in URLS), return_exceptions=True
        )
    elapsed = time.perf_counter() - start
    print(f"\nTotal execution time: {elapsed:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
