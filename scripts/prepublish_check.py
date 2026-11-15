#!/usr/bin/env python3
"""公開前チェック（無人運用向け）

- 実名・個人情報の混入
- アフィリエイトのプレースホルダ残り
- 内部リンク切れ / title・description の有無
を検査して終了コードで返す。

使い方:  python3 scripts/prepublish_check.py [--strict]
  --strict : プレースホルダが残っていても失敗扱い（公開直前用）
"""
import os
import re
import sys
import html.parser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PERSONAL_PATTERNS = ["heejae", "희재", "노희재", "玉川", "ヒジェ", "nohhuijae", "eietrade"]
PLACEHOLDER_HOSTS = ["example.invalid", "example.github.io"]

issues = []
warnings = []


class PageParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = ""
        self.links = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        for key in ("href", "src"):
            if key in d and d[key]:
                self.links.append(d[key])
        if tag == "title":
            self.in_title = True

    def handle_data(self, data):
        if self.in_title:
            self.title += data

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False


def walk(exts):
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules")]
        for name in filenames:
            if any(name.endswith(e) for e in exts):
                yield os.path.join(dirpath, name)


def main():
    strict = "--strict" in sys.argv

    for path in walk((".html", ".xml", ".js", ".css", ".yml", ".md", ".json")):
        rel = os.path.relpath(path, ROOT)
        text = open(path, encoding="utf-8", errors="ignore").read()
        low = text.lower()
        for pat in PERSONAL_PATTERNS:
            if pat.lower() in low:
                issues.append(f"개인정보 의심 '{pat}' → {rel}")

    pages = list(walk((".html",)))
    for path in pages:
        rel = os.path.relpath(path, ROOT)
        src = open(path, encoding="utf-8").read()
        parser = PageParser()
        parser.feed(src)
        if not parser.title.strip():
            issues.append(f"title 누락 → {rel}")
        if 'name="description"' not in src:
            issues.append(f"description 누락 → {rel}")
        for link in parser.links:
            if link.startswith(("http", "mailto:", "data:", "#", "//")):
                continue
            if link.startswith("/"):
                # サイトルート絶対パス（GitHub Pages ドメイン直下を想定）
                target = os.path.normpath(
                    os.path.join(ROOT, link.split("#")[0].split("?")[0].lstrip("/"))
                )
            else:
                target = os.path.normpath(
                    os.path.join(os.path.dirname(path), link.split("#")[0].split("?")[0])
                )
            if not os.path.exists(target):
                issues.append(f"링크 끊김 '{link}' → {rel}")
        if "example.invalid" in src:
            n = src.count("example.invalid")
            warnings.append(f"제휴 링크 플레이스홀더 {n}개 → {rel}")
        if "example.github.io" in src:
            warnings.append(f"공개 URL 미설정 → {rel}")

    print(f"페이지 {len(pages)}개 검사")
    for w in warnings:
        print("  [WARN]", w)
    for i in issues:
        print("  [FAIL]", i)
    print(f"결과: 실패 {len(issues)}건 / 경고 {len(warnings)}건")

    if issues or (strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
