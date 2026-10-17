import argparse
import asyncio
from pathlib import Path
import re
import sys
import time
import urllib.parse
import httpx


def resolve_to_raw_url(target: str) -> str:
    """If given a standard GitHub repo URL, converts it to its raw README URL.

    Example:
      https://github.com/psf/requests ->
      https://raw.githubusercontent.com/psf/requests/main/README.md
    """
    gh_match = re.match(r"^https?://github\.com/([^/]+)/([^/]+)/?$", target.strip())
    if gh_match:
        owner, repo = gh_match.groups()
        return f"https://raw.githubusercontent.com/{owner}/{repo}/main/README.md"
    return target


async def fetch_markdown_content(client: httpx.AsyncClient, source: str) -> str:
    """Fetches markdown text from either a remote HTTP/HTTPS URL or a local file path."""
    parsed = urllib.parse.urlsplit(source)

    # 1. Remote URL Case
    if parsed.scheme in ("http", "https"):
        target_url = resolve_to_raw_url(source)
        print(f"📥 Downloading markdown from: {target_url}")

        try:
            resp = await client.get(target_url, follow_redirects=True, timeout=10.0)
            # If default branch was 'master' instead of 'main', try fallback
            if resp.status_code == 404 and "githubusercontent.com" in target_url:
                fallback_url = target_url.replace("/main/", "/master/")
                resp = await client.get(
                    fallback_url, follow_redirects=True, timeout=10.0
                )

            resp.raise_for_status()
            return resp.text
        except httpx.HTTPStatusError as e:
            print(
                f"Error: Failed to download file (HTTP {e.response.status_code})",
                file=sys.stderr,
            )
            sys.exit(1)
        except Exception as e:
            print(f"Error downloading: {e}", file=sys.stderr)
            sys.exit(1)

    # 2. Local File Case
    local_path = Path(source)
    if not local_path.exists():
        print(
            f"Error: Local file '{source}' not found and is not a valid URL.",
            file=sys.stderr,
        )
        sys.exit(1)

    return local_path.read_text(encoding="utf-8", errors="replace")


def extract_urls(text: str) -> list[str]:
    """Finds all HTTP/HTTPS links from markdown syntax."""

    print("Extracting urls....")
    patterns = [
        r"!?\[.*?\]\((https?://[^\s\)]+)\)",
        r"^\s*\[.*?\]:\s*(https?://[^\s]+)",
        r"<(https?://[^>]+)>",
        r"(?<!\()(https?://[a-zA-Z0-9.\-_~:/?#\[\]@!$&'*+,;=%]+)",
    ]

    found = []
    for pattern in patterns:
        found.extend(re.findall(pattern, text, flags=re.MULTILINE))

    cleaned = []
    for raw in found:
        url = raw.rstrip(".,;)>'\"")
        parsed = urllib.parse.urlsplit(url)
        if parsed.scheme in ("http", "https") and parsed.netloc:
            cleaned.append(url)

    return list(dict.fromkeys(cleaned))


async def verify_url(
    client: httpx.AsyncClient,
    sem: asyncio.Semaphore,
    url: str,
    timeout: float,
) -> dict:
    """Checks URL health using HEAD with fallback to GET."""
    async with sem:
        start = time.perf_counter()
        for method in ("HEAD", "GET"):
            try:
                resp = await client.request(
                    method,
                    url,
                    timeout=timeout,
                    follow_redirects=True,
                )
                if method == "HEAD" and resp.status_code in (403, 404, 405):
                    continue

                latency_ms = (time.perf_counter() - start) * 1000
                return {"url": url, "status": resp.status_code, "latency": latency_ms}
            except httpx.HTTPStatusError as e:
                latency_ms = (time.perf_counter() - start) * 1000
                return {
                    "url": url,
                    "status": e.response.status_code,
                    "latency": latency_ms,
                }
            except httpx.TimeoutException:
                return {"url": url, "status": "TIMEOUT", "latency": 0.0}
            except httpx.ConnectError:
                return {"url": url, "status": "CONN_ERR", "latency": 0.0}
            except httpx.RequestError as e:
                return {"url": url, "status": f"ERR:{type(e).__name__}", "latency": 0.0}

        return {"url": url, "status": "FAIL", "latency": 0.0}


async def main_async(target: str, max_concurrency: int, timeout: float):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    async with httpx.AsyncClient(headers=headers, verify=False) as client:
        # Step 1: Download or read markdown
        content = await fetch_markdown_content(client, target)
        urls = extract_urls(content)

        if not urls:
            print("No HTTP/HTTPS URLs found in the markdown.")
            return

        print(
            f"Extracted {len(urls)} unique URL(s). Verifying (max {max_concurrency} concurrent)..."
        )
        print("-" * 80)

        # Step 2: Concurrently check all links
        sem = asyncio.Semaphore(max_concurrency)
        start_time = time.perf_counter()

        tasks = [verify_url(client, sem, u, timeout) for u in urls]
        results = await asyncio.gather(*tasks)

        elapsed = time.perf_counter() - start_time

        # Step 3: Print report
        broken = 0
        print(f"{'Status':<10} | {'Latency':<9} | {'URL'}")
        print("-" * 80)

        for r in results:
            status = str(r["status"])
            ok = status.isdigit() and int(status) < 400
            if ok:
                flag = "✅"
            else:
                flag = "❌"
                broken += 1

            latency_str = f"{r['latency']:.0f}ms" if r["latency"] > 0 else "---"
            print(f"{flag} {status:<7} | {latency_str:<9} | {r['url']}")

        print("-" * 80)
        print(
            f"Finished in {elapsed:.2f}s | "
            f"Working: {len(urls) - broken} | Broken: {broken}"
        )


def cli():
    parser = argparse.ArgumentParser(
        description="Download a README/Markdown file and check all its links asynchronously."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default="https://github.com/psf/requests",
        help="Local file path, direct markdown raw URL, or GitHub repo URL (default: psf/requests)",
    )
    parser.add_argument(
        "-c",
        "--concurrency",
        type=int,
        default=12,
        help="Max concurrent checks (default: 12)",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=5.0,
        help="Timeout per link check in seconds (default: 5.0)",
    )

    args = parser.parse_args()
    asyncio.run(
        main_async(
            args.target,
            max_concurrency=args.concurrency,
            timeout=args.timeout,
        )
    )


if __name__ == "__main__":
    cli()
