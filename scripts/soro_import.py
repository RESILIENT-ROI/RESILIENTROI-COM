#!/usr/bin/env python3
"""Import new Soro articles from its RSS feed as Hugo page bundles.

Writes content/posts/<slug>/index.md (+ local images) for each feed item
that is not already in the repo. Prints the slugs it created, one per line,
so the workflow can open one pull request per article.

Usage: soro_import.py FEED_URL [--author NAME] [--only SLUG]
"""
import argparse
import email.utils
import hashlib
import html
import os
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

try:
    from markdownify import markdownify as to_md
except ImportError:  # fall back to raw HTML; goldmark unsafe=true renders it
    to_md = None

POSTS = os.path.join("content", "posts")
NS = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "media": "http://search.yahoo.com/mrss/",
    "dc": "http://purl.org/dc/elements/1.1/",
}
UA = {"User-Agent": "resilientroi-soro-import/1.0"}


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def slugify(text):
    text = html.unescape(text).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:80].rstrip("-") or "post"


def text_of(item, tag):
    el = item.find(tag, NS)
    return (el.text or "").strip() if el is not None and el.text else ""


def existing_guids():
    guids = set()
    if not os.path.isdir(POSTS):
        return guids
    for root, _, files in os.walk(POSTS):
        if "index.md" in files:
            with open(os.path.join(root, "index.md"), encoding="utf-8") as f:
                m = re.search(r'^soro_guid:\s*"(.*)"\s*$', f.read(), re.M)
                if m:
                    guids.add(m.group(1))
    return guids


def localise_images(body_html, bundle):
    """Download <img> sources into the bundle and rewrite them to local names."""
    def repl(m):
        src = html.unescape(m.group(2))
        if not src.startswith("http"):
            return m.group(0)
        path = urllib.parse.urlparse(src).path
        ext = os.path.splitext(path)[1].lower()
        if ext not in {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".avif"}:
            ext = ".jpg"
        name = "img-" + hashlib.sha1(src.encode()).hexdigest()[:10] + ext
        try:
            data = fetch(src)
        except Exception as e:  # keep remote URL if download fails
            print(f"warn: image {src}: {e}", file=sys.stderr)
            return m.group(0)
        with open(os.path.join(bundle, name), "wb") as f:
            f.write(data)
        return f"{m.group(1)}{name}{m.group(3)}"

    return re.sub(r'(<img\b[^>]*?\bsrc=["\'])([^"\']+)(["\'])', repl, body_html, flags=re.I)


def yq(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("feed")
    ap.add_argument("--author", default="Resilient ROI")
    ap.add_argument("--skip", default="", help="comma-separated slugs to skip (open PRs)")
    a = ap.parse_args()
    skip = {s for s in a.skip.split(",") if s}

    root = ET.fromstring(fetch(a.feed))
    items = root.findall("./channel/item")
    seen = existing_guids()
    created = []

    for item in items:
        title = html.unescape(text_of(item, "title"))
        link = text_of(item, "link")
        guid = text_of(item, "guid") or link or title
        if not title or guid in seen:
            continue
        slug = slugify(title)
        bundle = os.path.join(POSTS, slug)
        if slug in skip or os.path.exists(bundle):
            continue

        body = text_of(item, "content:encoded") or text_of(item, "description")
        summary = re.sub(r"<[^>]+>", " ", html.unescape(text_of(item, "description")))
        summary = re.sub(r"\s+", " ", summary).strip()
        if len(summary) > 160:
            summary = summary[:157].rsplit(" ", 1)[0] + "..."
        pub = text_of(item, "pubDate") or text_of(item, "dc:date")
        try:
            date = email.utils.parsedate_to_datetime(pub).date().isoformat()
        except Exception:
            date = pub[:10] if re.match(r"\d{4}-\d{2}-\d{2}", pub) else ""
        tags = [html.unescape(c.text.strip()) for c in item.findall("category") if c.text]

        os.makedirs(bundle)
        body = localise_images(body, bundle)
        if to_md:
            body = to_md(body, heading_style="ATX", bullets="-").strip()

        fm = [
            "---",
            f"title: {yq(title)}",
            f"date: {date}" if date else None,
            f"description: {yq(summary)}",
            "tags: [" + ", ".join(yq(t) for t in tags) + "]",
            f"author: {yq(a.author)}",
            "version: 0.1",
            f"soro_guid: {yq(guid)}",
            "---",
        ]
        with open(os.path.join(bundle, "index.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(x for x in fm if x is not None) + "\n\n" + body + "\n")
        created.append(slug)

    print(f"feed items: {len(items)}, new: {len(created)}", file=sys.stderr)
    for s in created:
        print(s)


if __name__ == "__main__":
    main()
