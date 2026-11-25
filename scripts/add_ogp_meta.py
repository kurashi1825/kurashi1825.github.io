#!/usr/bin/env python3
"""Add OGP / Twitter Card meta tags to pages that lack them.

Reads <title>, <meta name="description"> and <link rel="canonical"> of each page,
then inserts og:type / og:title / og:description / og:url / og:site_name /
twitter:card right after the canonical link. Idempotent: pages that already have
og:title are skipped.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = [
    "about.html", "privacy.html", "disclaimer.html", "404.html",
    "categories/sim.html", "categories/wifi.html", "categories/card.html",
    "categories/education.html",
    "articles/card-too-many.html", "articles/cashback-guide.html",
    "articles/education-first-month.html", "articles/fixed-cost-3steps.html",
    "articles/home-router-or-hikari.html", "articles/sim-first-conditions.html",
]
SITE_NAME = "くらし比較ラボ"


def esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace('"', "&quot;")
             .replace("<", "&lt;").replace(">", "&gt;"))


def process(path: Path) -> str | None:
    html = path.read_text(encoding="utf-8")
    if 'og:title' in html:
        return None
    title_m = re.search(r"<title>(.*?)</title>", html, re.S)
    desc_m = re.search(r'<meta name="description" content="(.*?)">', html, re.S)
    canon_m = re.search(r'<link rel="canonical" href="(.*?)">', html)
    if not (title_m and canon_m):
        return "skip: missing title or canonical"
    title = title_m.group(1).strip()
    # OG title without the trailing brand suffix
    og_title = re.sub(r"｜くらし比較ラボ$", "", title).strip() or title
    desc = desc_m.group(1).strip() if desc_m else ""
    if len(desc) > 120:
        desc = desc[:117].rstrip() + "…"
    canonical = canon_m.group(1).strip()
    og_type = "article" if path.parts[-2] == "articles" else "website"
    block = (
        f'<meta property="og:type" content="{og_type}">\n'
        f'<meta property="og:title" content="{esc(og_title)}">\n'
        f'<meta property="og:description" content="{esc(desc)}">\n'
        f'<meta property="og:url" content="{esc(canonical)}">\n'
        f'<meta property="og:site_name" content="{SITE_NAME}">\n'
        f'<meta name="twitter:card" content="summary">\n'
    )
    new = html.replace(canon_m.group(0), canon_m.group(0) + "\n" + block, 1)
    path.write_text(new, encoding="utf-8")
    return "updated"


def main() -> int:
    changed = 0
    for rel in PAGES:
        p = ROOT / rel
        if not p.exists():
            print(f"missing {rel}")
            continue
        r = process(p)
        if r == "updated":
            changed += 1
            print(f"updated {rel}")
        elif r:
            print(f"{r} {rel}")
        else:
            print(f"already has OGP {rel}")
    print(f"total updated: {changed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
