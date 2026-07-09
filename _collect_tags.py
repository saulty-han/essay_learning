#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re
LEARN = "/Users/jiyancai/Desktop/CJYsama/MAIN/resources/llmdeepthink/essay/learn"
files = sorted(f for f in os.listdir(LEARN) if f.endswith("_full_translation.html"))
vocab_open = set()
vocab_close = set()
for f in files:
    txt = open(os.path.join(LEARN, f), encoding="utf-8").read()
    for m in re.finditer(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)', txt):
        slash, name = m.group(1), m.group(2).lower()
        if slash:
            vocab_close.add(name)
        else:
            vocab_open.add(name)
print("OPEN TAGS:", sorted(vocab_open))
print("CLOSE TAGS:", sorted(vocab_close))
print("IN OPEN NOT CLOSE:", sorted(vocab_open - vocab_close))
print("IN CLOSE NOT OPEN:", sorted(vocab_close - vocab_open))
