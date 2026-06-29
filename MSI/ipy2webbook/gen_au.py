#!/usr/bin/env python3
"""Refactor the legacy raw-HTML Au*.md link pages into clean, theme-aware
Jupyter Book pages using sphinx-design card grids (works in light & dark)."""
import re, sys, pathlib

SRC = pathlib.Path("_orig_backup")          # originals (untouched)
DST = pathlib.Path(".")                      # write new versions here

anchor_re = re.compile(
    r'href="(https://colab\.research\.google\.com[^"]+)".*?Problema\s*#?\s*(\d+)',
    re.DOTALL)
title_re = re.compile(r'^#\s+(.*)$', re.MULTILINE)
subtitle_re = re.compile(r'<i>\s*(.*?)\s*</i>', re.DOTALL)

BADGE = "https://colab.research.google.com/assets/colab-badge.svg"

# Edição publicada dos notebooks (../../sync_notebooks.py) + link JupyterLite.
# Cartão Au{NN} #num  ->  Au{NN}_P{num:03d}.ipynb. Só liga se o ficheiro existir.
NB_DIR = pathlib.Path(__file__).resolve().parents[2] / "notebooks" / "MSI"
LITE = "../lite/lab/index.html?path=MSI/{}"
JLITE = ("https://img.shields.io/badge/Abrir-no%20browser-F37626"
         "?logo=jupyter&logoColor=white")

def build(md: str, au_idx: int) -> str:
    title = title_re.search(md).group(1).strip()
    m = subtitle_re.search(md)
    subtitle = re.sub(r'\s+', ' ', m.group(1)).strip() if m else ""
    probs = anchor_re.findall(md)            # list of (url, number) in order

    out = [f"# {title}", ""]
    if subtitle:
        out += [f"*{subtitle}*", ""]
    out += ["::::{grid} 2 3 4 4", ":gutter: 3", ""]
    for url, num in probs:
        out += [
            f":::{{grid-item-card}} Problema&nbsp;#{num}",
            ":text-align: center",
            f'<a href="{url}" target="_blank" rel="noopener"><img '
            f'src="{BADGE}" alt="Abrir no Colab"></a>',
        ]
        nb = f"Au{au_idx:02d}_P{int(num):03d}.ipynb"
        if (NB_DIR / nb).exists():
            out.append(
                f'<br><a href="{LITE.format(nb)}" target="_blank" rel="noopener">'
                f'<img src="{JLITE}" alt="Abrir no browser (JupyterLite)"></a>'
            )
        out += [":::", ""]
    out += ["::::", ""]
    return "\n".join(out)

def main():
    dry = "--dry" in sys.argv
    files = sorted(SRC.glob("Au??.md"))
    for f in files:
        au_idx = int(f.stem[2:])
        new = build(f.read_text(encoding="utf-8"), au_idx)
        if dry:
            if f.name == "Au01.md":
                print(new)
                print(f"\n[Au01 has {new.count('grid-item-card')} problem cards]")
            continue
        (DST / f.name).write_text(new, encoding="utf-8")
    if not dry:
        # quick sanity: report counts (cards + botões JupyterLite)
        for f in files:
            new = build(f.read_text(encoding='utf-8'), int(f.stem[2:]))
            print(f"{f.name}: {new.count('grid-item-card')} cards"
                  f"  | {new.count('no%20browser')} JupyterLite")

if __name__ == "__main__":
    main()
