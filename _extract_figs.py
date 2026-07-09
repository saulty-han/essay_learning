#!/usr/bin/env python3
"""Extract figures (images) from all paper PDFs into learn/images/<stem>/."""
import os, glob, pathlib
import fitz  # pymupdf

ESSAY = pathlib.Path("/Users/jiyancai/Desktop/CJYsama/MAIN/resources/llmdeepthink/essay")
OUT = ESSAY / "learn" / "images"
OUT.mkdir(parents=True, exist_ok=True)

pdfs = []
for p in glob.glob(str(ESSAY / "*.pdf")):
    pdfs.append(pathlib.Path(p))
# also subdirs rag/ and learn/ and earlystop/ if they contain target papers
for p in glob.glob(str(ESSAY / "**" / "*.pdf"), recursive=True):
    pdfs.append(pathlib.Path(p))

seen = set()
for pdf in sorted(set(pdfs)):
    stem = pdf.stem
    if stem in seen:
        continue
    seen.add(stem)
    dest = OUT / stem
    dest.mkdir(parents=True, exist_ok=True)
    try:
        doc = fitz.open(pdf)
    except Exception as e:
        print(f"[ERR] {stem}: {e}")
        continue
    count = 0
    for pno in range(len(doc)):
        page = doc[pno]
        imgs = page.get_images(full=True)
        for idx, im in enumerate(imgs):
            xref = im[0]
            try:
                pix = fitz.Pixmap(doc, xref)
            except Exception:
                continue
            if pix.width < 200 or pix.height < 100:
                continue  # skip tiny decorations/icons
            if pix.n > 4:  # CMYK -> RGB
                try:
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                except Exception:
                    continue
            fname = dest / f"{stem}_p{pno+1}_fig{idx+1}.png"
            try:
                pix.save(str(fname))
                count += 1
            except Exception as e:
                print(f"[W] {fname}: {e}")
    print(f"[OK] {stem}: {count} figures -> images/{stem}/")
