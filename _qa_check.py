#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, sys
from html.parser import HTMLParser

LEARN = "/Users/jiyancai/Desktop/CJYsama/MAIN/resources/llmdeepthink/essay/learn"
IMG = os.path.join(LEARN, "images")

VOID = {"area","base","br","col","embed","hr","img","input","link","meta","param","source","track","wbr"}

class TagChecker(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errors = []
    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        self.stack.append((tag, self.getpos()))
    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append(f"extra closing </{tag}> at {self.getpos()}")
            return
        top, pos = self.stack[-1]
        if top == tag:
            self.stack.pop()
        else:
            # try to find match
            found = None
            for i in range(len(self.stack)-1, -1, -1):
                if self.stack[i][0] == tag:
                    found = i
                    break
            if found is None:
                self.errors.append(f"unmatched </{tag}> at {self.getpos()} (top={top})")
            else:
                skipped = [t for t,_ in self.stack[found+1:]]
                self.errors.append(f"</{tag}> at {self.getpos()} closes but unclosed inside: {skipped}")
                self.stack = self.stack[:found]

def check_file(path):
    with open(path, encoding="utf-8") as f:
        html = f.read()
    issues = []
    # closing tag
    if not re.search(r"</html>\s*$", html):
        if "</html>" not in html:
            issues.append("MISSING </html>")
        else:
            issues.append("</html> not at EOF (trailing content)")
    # parse tag balance
    p = TagChecker()
    try:
        p.feed(html)
    except Exception as e:
        issues.append(f"PARSE ERROR: {e}")
    if p.stack:
        issues.append(f"UNCLOSED TAGS: {[t for t,_ in p.stack]}")
    for e in p.errors:
        issues.append(e)
    return issues, html

def main():
    files = sorted(os.listdir(LEARN))
    htmls = [f for f in files if f.endswith(".html")]
    report = []
    # 1) full_translation image refs
    ft = [f for f in htmls if f.endswith("_full_translation.html")]
    da = [f for f in htmls if f.endswith("_deep_analysis.html")]
    missing_imgs = []
    for f in ft:
        path = os.path.join(LEARN, f)
        with open(path, encoding="utf-8") as fh:
            txt = fh.read()
        for m in re.finditer(r'src="(images/[^"]+)"', txt):
            src = m.group(1)
            full = os.path.join(LEARN, src)
            if not os.path.exists(full):
                missing_imgs.append((f, src))
    # 2) deep_analysis link injection targets
    link_issues = []
    for f in da:
        path = os.path.join(LEARN, f)
        with open(path, encoding="utf-8") as fh:
            txt = fh.read()
        if "Full Translation" not in txt and "full_translation" not in txt:
            link_issues.append((f, "NO translation link found"))
            continue
        m = re.search(r'href="([a-z0-9_]+_full_translation\.html)"', txt)
        if not m:
            link_issues.append((f, "link present but target not matched"))
            continue
        target = m.group(1)
        if not os.path.exists(os.path.join(LEARN, target)):
            link_issues.append((f, f"target missing: {target}"))
    # 3) tag balance / closing for all
    tag_issues = []
    for f in htmls:
        issues, _ = check_file(os.path.join(LEARN, f))
        if issues:
            tag_issues.append((f, issues))
    # output
    print("="*70)
    print(f"FULL TRANSLATION FILES: {len(ft)}")
    print(f"DEEP ANALYSIS FILES: {len(da)}")
    print(f"TOTAL HTML: {len(htmls)}")
    print("="*70)
    print("\n[1] BROKEN IMAGE REFERENCES (full_translation):")
    if missing_imgs:
        for f, src in missing_imgs:
            print(f"  {f} -> {src}")
    else:
        print("  NONE")
    print("\n[2] DEEP ANALYSIS LINK ISSUES:")
    if link_issues:
        for f, msg in link_issues:
            print(f"  {f}: {msg}")
    else:
        print("  NONE")
    print("\n[3] TAG BALANCE / CLOSING ISSUES (all html):")
    if tag_issues:
        for f, iss in tag_issues:
            print(f"  {f}:")
            for i in iss:
                print(f"      - {i}")
    else:
        print("  NONE")
    print("\nDONE")

if __name__ == "__main__":
    main()
