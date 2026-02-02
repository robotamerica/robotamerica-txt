#!/usr/bin/env python3
import os
import re
import time
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

BASE = "https://robotameri.ca/"
ARCHIVE = urljoin(BASE, "archive/")

OUT_DIR = "docs"
POSTS_DIR = os.path.join(OUT_DIR, "posts")
PAGES_DIR = os.path.join(OUT_DIR, "pages")

# Add/remove pages you want mirrored as “site pages”
STATIC_PAGES = [
    "archive/",
    "links/",
    "tools/",
    "manifesto/",
]

UA = "robotamerica-txt-mirror/1.0 (+https://robotameri.ca/)"

session = requests.Session()
session.headers.update({"User-Agent": UA})

def fetch(url: str) -> str:
    r = session.get(url, timeout=30)
    r.raise_for_status()
    return r.text

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

def extract_post_urls_from_archive(html: str):
    soup = BeautifulSoup(html, "html.parser")

    # On Bear sites, archive list is typically in main content as links
    urls = []
    for a in soup.select("main a[href], a[href]"):
        u = normalize(a.get("href", ""))
        if not u or not is_internal(u):
            continue

        p = urlparse(u).path

        # Skip obvious non-post routes
        if p.startswith("/archive") or p.startswith("/tags") or p.startswith("/feed") or p.startswith("/search"):
            continue
        if any(p.startswith("/" + x.strip("/")) for x in ["links", "tools", "manifesto"]):
            continue

        # Keep only single-slug paths: /something/ (Bear posts)
        if re.fullmatch(r"/[A-Za-z0-9\-]+/?", p):
            urls.append(u)

    # De-dupe while preserving order
    seen = set()
    out = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out

def pick_main_content(soup: BeautifulSoup):
    main = soup.find("main")
    if main:
        return main
    body = soup.body
    return body if body else soup

def html_to_markdown(html: str, source_url: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # Drop non-content
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    container = pick_main_content(soup)

    # Remove nav/header/footer inside main (if present)
    for tag in container.find_all(["nav", "header", "footer"]):
        tag.decompose()

    # Ensure links are absolute so your mirror is standalone
    for a in container.find_all("a", href=True):
        a["href"] = normalize(a["href"])

    # Convert HTML → Markdown
    md_body = md(str(container), heading_style="ATX")  # # headings

    # Clean up excessive blank lines
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

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(POSTS_DIR, exist_ok=True)
    os.makedirs(PAGES_DIR, exist_ok=True)

    # Seed from archive
    archive_html = fetch(ARCHIVE)
    post_urls = extract_post_urls_from_archive(archive_html)

    manifest_lines = []
    site_chunks = []

    # Mirror static pages
    manifest_lines.append("## pages\n")
    for rel in STATIC_PAGES:
        url = urljoin(BASE, rel)
        out_name = slug_from_path(urlparse(url).path) + ".md"
        out_path = os.path.join(PAGES_DIR, out_name)

        content = html_to_markdown(fetch(url), url)
        write_file(out_path, content)

        manifest_lines.append(f"- [{out_name}](pages/{out_name}) — {url}\n")
        site_chunks.append(f"\n\n---\n\n## {url}\n\n")
        site_chunks.append(content)

        time.sleep(0.25)

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

        time.sleep(0.25)

    # index.md
    index_md = (
        "# robotamerica — markdown mirror\n\n"
        f"- seed: {ARCHIVE}\n"
        f"- generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n\n"
        "---\n\n"
        + "".join(manifest_lines)
        + "\n"
    )
    write_file(os.path.join(OUT_DIR, "index.md"), index_md)

    # site.md (single-file mirror)
    site_md = (
        "# robotamerica — whole site (markdown mirror)\n\n"
        f"- seed: {ARCHIVE}\n"
        f"- generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n\n"
        "This is a machine-generated Markdown mirror of robotameri.ca.\n\n"
        "---\n"
        + "".join(site_chunks)
        + "\n"
    )
    write_file(os.path.join(OUT_DIR, "site.md"), site_md)

    print(f"Done: {len(STATIC_PAGES)} pages + {len(post_urls)} posts → {OUT_DIR}/")

if __name__ == "__main__":
    main()
