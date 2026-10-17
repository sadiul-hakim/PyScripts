import argparse
import asyncio
from pathlib import Path
import re
import sys
import time
import urllib.parse
import httpx


def resolve_github_readme_urls(target: str) -> list[str]:
    """Converts a GitHub repo URL into candidate raw README endpoints.

    Checks both .rst and .md across main and master branches.
    """
    gh_match = re.match(r"^https?://github\.com/([^/]+)/([^/]+)/?$", target.strip())
    if gh_match:
        owner, repo = gh_match.groups()
        candidates = []
        for branch in ("main", "master"):
            # RST first since projects like Django prioritize it, then MD
            candidates.append(
                f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.rst"
            )
            candidates.append(
                f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.md"
            )
            candidates.append(
                f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.adoc"
            )
        return candidates
    return [target]


async def fetch_doc_content(client: httpx.AsyncClient, source: str) -> tuple[str, str]:
    """Fetches document text from a local path or candidate remote URLs."""
    parsed = urllib.parse.urlsplit(source)

    if parsed.scheme in ("http", "https"):
        candidates = resolve_github_readme_urls(source)
        for url in candidates:
            try:
                print(f"📥 Checking: {url}")
                resp = await client.get(url, follow_redirects=True, timeout=8.0)
                if resp.status_code == 200:
                    print(f"✅ Found document at: {url}")
                    return resp.text, url
            except httpx.RequestError:
                continue

        print(
            f"Error: Could not find a valid README (.rst or .md) for '{source}'.",
            file=sys.stderr,
        )
        sys.exit(1)

    local_path = Path(source)
    if not local_path.exists():
        print(f"Error: Local file '{source}' not found.", file=sys.stderr)
        sys.exit(1)

    return local_path.read_text(encoding="utf-8", errors="replace"), source


def is_local_host(netloc: str) -> bool:
    """Checks whether a domain/netloc points to a local machine."""
    # Strip port if present (e.g., '127.0.0.1:8000' -> '127.0.0.1')
    host = netloc.split(":")[0].strip("[]").lower()

    # Local hostnames and IPs
    local_identifiers = {"localhost", "127.0.0.1", "0.0.0.0", "::1"}

    return (
        host in local_identifiers
        or host.startswith("127.")  # Entire 127.0.0.0/8 loopback range
        or host.endswith(".local")
        or host.endswith(".localhost")
    )


def extract_urls(text: str) -> list[str]:
    """Extracts URLs from Markdown, reStructuredText, and plain text,

    ignoring loopback/localhost references.
    """
    patterns = [
        # Markdown standard: [text](https://...) or ![alt](https://...)
        r"!?\[(?:[^\[\]]|(?:\([^()]*\)))*\]\((https?://[^\s\)]+)\)",
        # Markdown reference: [id]: https://...
        r"^\s*\[[^\]]+\]:\s*(https?://[^\s]+)",
        # RST inline links: `Text <https://...>`_
        r"`[^`]*?<((?:https?://)[^\s>]+)>`_",
        # RST hyperlink target definition: .. _name: https://...
        r"^\s*\.\.\s+_[^:]+:\s*(https?://[^\s]+)",
        # Angle bracket autolinks: <https://...>
        r"<((?:https?://)[^>]+)>",
        # Bare URLs in text
        r"(?<![\[\(])(https?://[a-zA-Z0-9.\-_~:/?#@!$&'*+,;=%]+)",
    ]

    found = []
    for pattern in patterns:
        found.extend(re.findall(pattern, text, flags=re.MULTILINE))

    cleaned = []
    for raw in found:
        url = raw.rstrip(".,;)>'\"_`[]")

        try:
            parsed = urllib.parse.urlsplit(url)

            # Check valid scheme, valid netloc, and exclude localhosts
            if (
                parsed.scheme in ("http", "https")
                and parsed.netloc
                and not is_local_host(parsed.netloc)
            ):
                cleaned.append(url)
        except ValueError:
            continue

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
        content, source_url = await fetch_doc_content(client, target)
        urls = extract_urls(content)

        if not urls:
            print("No HTTP/HTTPS URLs found in the document.")
            return

        print(
            f"Extracted {len(urls)} unique URL(s). Verifying (max {max_concurrency} concurrent)..."
        )
        print("-" * 80)

        sem = asyncio.Semaphore(max_concurrency)
        start_time = time.perf_counter()

        tasks = [verify_url(client, sem, u, timeout) for u in urls]
        results = await asyncio.gather(*tasks)

        elapsed = time.perf_counter() - start_time

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
        description="Async Link Checker for GitHub repos, Markdown, and RST files."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default="https://github.com/django/django",
        help="Local file path or GitHub repo URL (default: https://github.com/django/django)",
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
