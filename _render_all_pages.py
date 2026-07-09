#!/usr/bin/env python3
# Render EVERY page of every target paper PDF to images/<stem>_pages/pNN.png
# (vector figures that _extract_figs can't grab are covered by whole-page renders)
import os, glob, pathlib, sys
import fitz  # pymupdf

ESSAY = pathlib.Path("/Users/jiyancai/Desktop/CJYsama/MAIN/resources/llmdeepthink/essay")
OUT = ESSAY / "learn" / "images"
OUT.mkdir(parents=True, exist_ok=True)

# stem -> keyword used to locate the PDF (matched against filename, spaces removed, case-insensitive)
STEM_PDF = {
    "abmcts": "Wider or Deeper",
    "agentfold": "AgentFold",
    "agentic_reasoning": "Agentic Reasoning",
    "bao": "Bao- Learning to Steer",
    "bavt": "SpendlessReasonBetter",
    "bayesqo": "Learned Offline Query Planning via Bayesian",
    "booster": "Boost Automatic Database Tuning",
    "dbot": "D-Bot- An LLM-Powered",
    "deepconf": "DEEP THINK WITH CONFIDENCE",
    "delta": "Delta- A Learned Mixed",
    "emulating_rag": "EMULATING RETRIEVAL",
    "fastgres": "FASTgres",
    "kepler": "Kepler Robust",
    "lero": "Lero- A Learning-to-Rank",
    "lits": "LiTS- A Modular",
    "llmopt": "LLMOPT- LEARNING",
    "llmqo": "Can Large Language Models Be",
    "llmsteer": "LLMSTEER-",
    "master_mcts": "MASTER- A Multi-Agent",
    "mcts_ahd": "Monte Carlo Tree Search for Comprehensive Exploration",
    "pqo_query_logs": "Leveraging Query Logs and Machine Learning for Parametric",
    "r2ag": "R 2AG- Incorporating",
    "rankpqo": "RankPQO- Learning-to-Rank",
    "reactree": "ReAcTree",
    "reasoning_bank": "ReasoningBank",
    "rest_mcts": "ReST-MCTS",
    "s1_simple_test_time_scaling": "s1- Simple",
    "sefrqo": "SEFRQO-",
    "simrag": "SimRAG-",
    "tabtracer": "TabTracer-",
    "taobao_advertising": "Enhancing Taobao",
    "toolchain": "ToolChain",
    "training_free_qo": "Training-Free Query Optimization",
    "wider_or_deeper": "Wider or Deeper",
}

ZOOM = 2.0
mat = fitz.Matrix(ZOOM, ZOOM)

def find_pdf(keyword):
    kw = keyword.lower().replace(" ", "")
    best = None
    for p in glob.glob(str(ESSAY / "**" / "*.pdf"), recursive=True):
        name = pathlib.Path(p).stem.lower().replace(" ", "")
        if kw in name:
            return pathlib.Path(p)
    return None

total = 0
for stem, kw in STEM_PDF.items():
    pdf = find_pdf(kw)
    if not pdf:
        print(f"[MISS] {stem} <- {kw}")
        continue
    dest = OUT / f"{stem}_pages"
    dest.mkdir(parents=True, exist_ok=True)
    try:
        doc = fitz.open(pdf)
    except Exception as e:
        print(f"[ERR] {stem}: {e}")
        continue
    n = len(doc)
    cnt = 0
    for pno in range(n):
        fname = dest / f"p{pno+1:02d}.png"
        if fname.exists():
            cnt += 1
            continue
        try:
            pix = doc[pno].get_pixmap(matrix=mat)
            pix.save(str(fname))
            cnt += 1
        except Exception as e:
            print(f"[W] {stem} p{pno+1}: {e}")
    total += cnt
    print(f"[OK] {stem}: {cnt}/{n} pages -> images/{stem}_pages/  (from {pdf.name})")
print(f"\nDONE. total page images: {total}")
