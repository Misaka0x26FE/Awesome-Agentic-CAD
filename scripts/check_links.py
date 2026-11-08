#!/usr/bin/env python3
"""Check HTTP(S) links in Markdown files.

Usage:
    python scripts/check_links.py [paths...]

Defaults to README.md, README.zh-CN.md, CONTRIBUTING.md and docs/*.md.
Exit code 1 if any URL returns 4xx/5xx.
"""
from __future__ import annotations

import concurrent.futures
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FILES = [
    ROOT / "README.md",
    ROOT / "README.zh-CN.md",
    ROOT / "CONTRIBUTING.md",
    *sorted((ROOT / "docs").glob("*.md")),
]

URL_RE = re.compile(r"https?://[^\s<>)\]]+")
TRAILING = ".,;:!?\"'"


def collect(paths: list[Path]) -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for raw in URL_RE.findall(text):
            url = raw.rstrip(TRAILING)
            if url.endswith("/"):
                url = url[:-1]
            found.setdefault(url, set()).add(path.name)
    return found


def check(url: str, timeout: int = 20) -> tuple[str, int, str]:
    request = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": "awesome-agentic-cad-linkcheck/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return url, response.status, ""
    except urllib.error.HTTPError as exc:
        if exc.code in (403, 405, 429):
            return _get(url, timeout, exc.code)
        return url, exc.code, exc.reason or ""
    except Exception as exc:  # noqa: BLE001
        return _get(url, timeout, 0, str(exc))


def _get(url: str, timeout: int, prior: int, prior_reason: str = "") -> tuple[str, int, str]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "awesome-agentic-cad-linkcheck/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return url, response.status, ""
    except urllib.error.HTTPError as exc:
        return url, exc.code, exc.reason or prior_reason
    except Exception as exc:  # noqa: BLE001
        return url, prior, f"{prior_reason}; GET failed: {exc}"


def main() -> int:
    paths = [Path(p) for p in sys.argv[1:]] or DEFAULT_FILES
    urls = collect(paths)
    if not urls:
        print("no URLs found")
        return 0

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as pool:
        futures = {pool.submit(check, url): url for url in urls}
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    results.sort(key=lambda item: (item[1] == 200, item[0]))
    failures = 0
    warnings = 0
    for url, status, reason in results:
        if status == 200:
            marker = "OK  "
        elif status in (404, 410):
            marker = "ERR "
            failures += 1
        else:
            marker = "WARN"
            warnings += 1
        files = ", ".join(sorted(urls[url]))
        print(f"{marker} {status:>3} {url}  [{files}] {reason}")

    print(f"\n{len(results)} URLs, {failures} hard failures, {warnings} warnings")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
