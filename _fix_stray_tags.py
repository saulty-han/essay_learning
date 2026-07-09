#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re
LEARN = "/Users/jiyancai/Desktop/CJYsama/MAIN/resources/llmdeepthink/essay/learn"
ALLOW = {
    'a','b','body','br','code','div','em','h1','h2','h3','h4','h5','head','html',
    'img','li','link','meta','ol','p','script','span','strong','style','sub','sup',
    'table','tbody','td','th','thead','title','tr','ul','blockquote','figure',
    'figcaption','section','center','small','hr','i','u','mark','cite','math','eq',
    'details','summary','pre','noscript'
}
files = sorted(f for f in os.listdir(LEARN) if f.endswith("_full_translation.html"))
pat = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)')

def fix(m):
    slash, name = m.group(1), m.group(2).lower()
    if name in ALLOW:
        return m.group(0)  # legit tag, leave
    # stray <name or </name in prose -> escape the opening <
    return '&lt;' + m.group(0)[1:]

total = 0
changed = []
for f in files:
    p = os.path.join(LEARN, f)
    txt = open(p, encoding="utf-8").read()
    new, n = pat.subn(fix, txt)
    if n:
        open(p, "w", encoding="utf-8").write(new)
        total += n
        changed.append((f, n))
print("Fixed stray '<' tokens:", total)
for f, n in changed:
    print(f"  {f}: {n}")
