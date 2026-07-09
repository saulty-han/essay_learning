import os, glob, sys
from pypdf import PdfReader

PDF_DIR = "/Users/jiyancai/Desktop/CJYsama/MAIN/resources/llmdeepthink/essay"
OUT_DIR = "/Users/jiyancai/Desktop/CJYsama/MAIN/resources/llmdeepthink/essay/learn"

# keyword -> output filename base
TARGETS = {
    "Enhancing Taobao": "taobao_advertising",
    "AgentFold": "agentfold",
    "TabTracer": "tabtracer",
    "ReasoningBank": "reasoning_bank",
    "Comprehensive Exploration in LLM-Based Automatic Heuristic": "mcts_ahd",
    "ReST-MCTS": "rest_mcts",
    "LiTS- A Modular": "lits",
    "D-Bot- An LLM-Powered": "dbot",
    "Learned Offline Query Planning via Bayesian": "bayesqo",
    "ReAcTree": "reactree",
    "Spend Less": "bavt",
    "Reason Better": "bavt",
    "LLMOPT- LEARNING": "llmopt",
}

def find_pdf(keyword):
    for f in os.listdir(PDF_DIR):
        if keyword.lower() in f.lower() and f.lower().endswith(".pdf"):
            return os.path.join(PDF_DIR, f)
    # try glob
    cands = glob.glob(os.path.join(PDF_DIR, "*" + keyword.split()[0] + "*.pdf"))
    if cands:
        return cands[0]
    return None

for kw, out in TARGETS.items():
    pdf = find_pdf(kw)
    if not pdf:
        print(f"[MISS] {out} <- {kw}")
        continue
    try:
        r = PdfReader(pdf, strict=False)
        parts = []
        for i, pg in enumerate(r.pages):
            try:
                t = pg.extract_text() or ""
            except Exception as e:
                t = f"[err {e}]"
            parts.append(f"=== PAGE {i+1} ===\n{t}")
        txt = "\n".join(parts)
        outp = os.path.join(OUT_DIR, out + "_full_text.txt")
        with open(outp, "w", encoding="utf-8", errors="replace") as fh:
            fh.write(txt)
        print(f"[OK] {out} ({len(r.pages)} pages) <- {os.path.basename(pdf)}")
    except Exception as e:
        print(f"[ERR] {out}: {e}")
