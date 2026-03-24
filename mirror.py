#!/usr/bin/env python3
"""
robotamerica markdown mirror (full)

What this version does (reliably):
- Uses /archive/ as the canonical full-history post index (NOT /feed/ which is truncated)
- Discovers pages from homepage header nav + always includes PINNED_PAGES
- Uses browser-like headers to avoid 403 Forbidden
- Fails loudly if blocked or if post count is suspiciously low
- Writes:
  - docs/index.md (manifest)
  - docs/site.md (single-file mirror)
  - docs/posts/*.md (each post)
  - docs/pages/*.md (each page)

Run:
  python mirror.py
"""

import os
import re
import sys
import time
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

BASE = "https://robotameri.ca/"
HOME = BASE
ARCHIVE = urljoin(BASE, "archive/")

OUT_DIR = "docs"
POSTS_DIR = os.path.join(OUT_DIR, "posts")
PAGES_DIR = os.path.join(OUT_DIR, "pages")

# Guaranteed pages (even if nav changes)
PINNED_PAGES = [
    "archive/",
    "links/",
    "tools/",
    "manifesto/",
]

# Gentle crawl delay
SLEEP_SECS = 0.35

# Use a real browser UA; many sites block generic curl/bot UAs.
BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)

session = requests.Session()


def fetch(url: str) -> str:
    """Fetch HTML with browser-like headers and loud failure on blocks."""
    headers = {
        "User-Agent": BROWSER_UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }
    r = session.get(url, headers=headers, timeout=30, allow_redirects=True)

    if r.status_code in (401, 403):
        snippet = (r.text or "")[:200].replace("\n", " ").strip()
        raise RuntimeError(f"BLOCKED ({r.status_code}) fetching {url}. Snippet: {snippet!r}")

    r.raise_for_status()

    text = r.text or ""

    if re.search(r"\bforbidden\b", text, re.IGNORECASE) and len(text) < 2000:
        snippet = text[:200].replace("\n", " ").strip()
        raise RuntimeError(f"Likely blocked fetching {url}. Snippet: {snippet!r}")

    return text


def is_internal(url: str) -> bool:
    return urlparse(url).netloc == urlparse(BASE).netloc


def normalize(href: str) -> str:
    if not href:
        return ""
    if href.startswith("http://") or href.startswith("https://"):
        return href
    return urljoin(BASE, href)


def slug_from_path(path: str) -> str:
    s = path.strip("/").lower()
    s = re.sub(r"[^a-z0-9/_-]+", "-", s)
    s = s.replace("/", "-")
    return s or "home"


def pick_main_content(soup: BeautifulSoup):
    main = soup.find("main")
    if main:
        return main
    body = soup.body
    return body if body else soup


def html_to_markdown(html: str, source_url: str) -> str:
    """Convert page HTML to Markdown, keeping links absolute."""
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    container = pick_main_content(soup)

    for tag in container.find_all(["nav", "header", "footer"]):
        tag.decompose()

    for a in container.find_all("a", href=True):
        a["href"] = normalize(a["href"])

    md_body = md(str(container), heading_style="ATX") 
    md_body = re.sub(r"\n{3,}", "\n\n", md_body).strip() + "\n"

    header = (
        f"# robotamerica — text mirror\n\n"
        f"- source: {source_url}\n"
        f"- generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n\n"
        f"---\n\n"
    )
    return header + md_body


def write_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def extract_post_urls_from_archive(html: str):
    """
    Extract ALL post URLs from /archive/ reliably.

    Critical: pull links only from the archive post list (<ul class="blog-posts">),
    not from arbitrary anchors, so random widgets/nav/scripts don't interfere.
    """
    soup = BeautifulSoup(html, "html.parser")

    post_list = soup.select_one("ul.blog-posts")
    if not post_list:
 
        post_list = soup.select_one("main ul.blog-posts") or soup.select_one("ul.embedded.blog-posts")
    if not post_list:
        raise RuntimeError("Could not find <ul class='blog-posts'> on archive page.")

    urls = []
    for a in post_list.select("a[href]"):
        u = normalize(a.get("href", ""))
        if not u or not is_internal(u):
            continue

        path = urlparse(u).path
        if re.fullmatch(r"/[A-Za-z0-9\-]+/?", path):
            urls.append(u)

    seen, out = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def extract_page_urls_from_home(html: str):
    """
    Discover page-like URLs from homepage header nav.
    (Your homepage has <header><nav>...</nav></header>.)

    We include pinned pages regardless, and we exclude:
    - hash links (#menu, #dark, #light)
    - /feed and /hit endpoints
    - the home path "/"
    """
    soup = BeautifulSoup(html, "html.parser")
    nav = soup.select_one("header nav")
    urls = []

    if nav:
        for a in nav.select("a[href]"):
            href = (a.get("href") or "").strip()
            if not href or href.startswith("#"):
                continue

            u = normalize(href)
            if not u or not is_internal(u):
                continue

            path = urlparse(u).path
            if path in ("/", ""):
                continue
            if path.startswith(("/feed", "/hit")):
                continue

            # Keep "page-like" paths: usually /something/ . We'll mirror what the nav contains.
            # We'll let posts be handled by archive; if nav contains a post-like link, it's harmless.
            urls.append(u)

    # Add pinned pages to guarantee they're always mirrored
    for rel in PINNED_PAGES:
        urls.append(urljoin(BASE, rel))

    # De-dupe preserving order
    seen, out = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(POSTS_DIR, exist_ok=True)
    os.makedirs(PAGES_DIR, exist_ok=True)

    print(f"Home:    {HOME}")
    home_html = fetch(HOME)

    print(f"Archive: {ARCHIVE}")
    archive_html = fetch(ARCHIVE)

    post_urls = extract_post_urls_from_archive(archive_html)
    page_urls = extract_page_urls_from_home(home_html)

    print(f"Posts found in archive: {len(post_urls)}")
    print(f"Pages found (nav+pinned): {len(page_urls)}")

    # Safety guard: if archive parsing breaks, stop instead of generating a partial mirror
    if len(post_urls) < 15:
        raise RuntimeError(
            f"Suspiciously low post count ({len(post_urls)}). "
            "Archive may be blocked, randomized, or markup changed."
        )

    manifest_lines = []
    site_chunks = []
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Mirror pages
    manifest_lines.append("## pages\n")
    for url in page_urls:
        path = urlparse(url).path
        out_name = slug_from_path(path) + ".md"
        out_path = os.path.join(PAGES_DIR, out_name)

        content = html_to_markdown(fetch(url), url)
        write_file(out_path, content)

        manifest_lines.append(f"- [{out_name}](pages/{out_name}) — {url}\n")
        site_chunks.append(f"\n\n---\n\n## {url}\n\n")
        site_chunks.append(content)

        time.sleep(SLEEP_SECS)

    # Mirror posts
    manifest_lines.append("\n## posts\n")
    for url in post_urls:
        slug = slug_from_path(urlparse(url).path)
        out_name = slug + ".md"
        out_path = os.path.join(POSTS_DIR, out_name)

        content = html_to_markdown(fetch(url), url)
        write_file(out_path, content)

        manifest_lines.append(f"- [{out_name}](posts/{out_name}) — {url}\n")
        site_chunks.append(f"\n\n---\n\n## {url}\n\n")
        site_chunks.append(content)

        time.sleep(SLEEP_SECS)

    # index.md
    index_md = (
        "# robotamerica — markdown mirror\n\n"
        f"- seed (posts): {ARCHIVE}\n"
        f"- seed (pages): {HOME}\n"
        f"- generated: {generated_at}\n\n"
        "---\n\n"
        + "".join(manifest_lines)
        + "\n"
    )
    write_file(os.path.join(OUT_DIR, "index.md"), index_md)

    # site.md
    site_md = (
        "# robotamerica — whole site (markdown mirror)\n\n"
        f"- seed (posts): {ARCHIVE}\n"
        f"- seed (pages): {HOME}\n"
        f"- generated: {generated_at}\n\n"
        "This is a machine-generated Markdown mirror of robotameri.ca.\n\n"
        "---\n"
        + "".join(site_chunks)
        + "\n"
    )
    write_file(os.path.join(OUT_DIR, "site.md"), site_md)

    print(f"Done: {len(page_urls)} pages + {len(post_urls)} posts → {OUT_DIR}/")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nAborted.")
        sys.exit(130)
    except Exception as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        sys.exit(1)