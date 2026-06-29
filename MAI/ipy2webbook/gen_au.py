#!/usr/bin/env python3
"""Refactor legacy raw-HTML Au*.md link pages into theme-aware Jupyter Book
pages (sphinx-design card grids). Handles both label styles:
  '... > Problema #1 </a>'  (MSI)   and   '... > #6 </a>'  (MAI)
Reads originals from ./_orig_backup, writes new versions to ./ ."""
import re, sys, pathlib

SRC = pathlib.Path("_orig_backup")
DST = pathlib.Path(".")

# url, then the number shown as the link text (inside the anchor's <span>).
# [^>]* skips the span attributes (which contain '11pt' etc.) up to its '>'.
anchor_re = re.compile(
    r'href="(https://colab\.research\.google\.com[^"]+)"'
    r'.*?<span[^>]*>\s*(?:Problema\s*)?#?\s*(\d+[a-z]?)',
    re.DOTALL)
title_re = re.compile(r'^#\s+(.*)$', re.MULTILINE)
subtitle_re = re.compile(r'<i>\s*(.*?)\s*</i>', re.DOTALL)
BADGE = "https://colab.research.google.com/assets/colab-badge.svg"

# Tabela de ligação cartão->notebook (preenchida por make_mai_skeleton.py e
# validada à mão) + link JupyterLite. Ausente => só Colab, sem botão.
NB_DIR = pathlib.Path(__file__).resolve().parents[2] / "notebooks" / "MAI"
LITE = "../lite/lab/index.html?path=MAI/{}"
JLITE = ("https://img.shields.io/badge/Abrir-no%20browser-F37626"
         "?logo=jupyter&logoColor=white")

def _load_links():
    f = pathlib.Path(__file__).resolve().parent / "mai_links.yml"
    if not f.exists():
        return {}
    try:
        import yaml
    except ImportError:
        return {}
    data = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
    # {Au: [filename ou None por ordem de cartão]}
    return {au: [(e or {}).get("nb") for e in entries]
            for au, entries in data.items() if isinstance(entries, list)}

LINKS = _load_links()

def build(md: str, au: str = "") -> str:
    title = title_re.search(md).group(1).strip()
    m = subtitle_re.search(md)
    subtitle = re.sub(r'\s+', ' ', m.group(1)).strip() if m else ""
    probs = anchor_re.findall(md)
    nbs = LINKS.get(au, [])
    out = [f"# {title}", ""]
    if subtitle:
        out += [f"*{subtitle}*", ""]
    out += ["::::{grid} 2 3 4 4", ":gutter: 3", ""]
    for k, (url, num) in enumerate(probs):
        out += [
            f":::{{grid-item-card}} Problema&nbsp;#{num}",
            ":text-align: center",
            f'<a href="{url}" target="_blank" rel="noopener"><img '
            f'src="{BADGE}" alt="Abrir no Colab"></a>',
        ]
        nb = nbs[k] if k < len(nbs) else None
        if nb and (NB_DIR / nb).exists():
            out.append(
                f'<br><a href="{LITE.format(nb)}" target="_blank" rel="noopener">'
                f'<img src="{JLITE}" alt="Abrir no browser (JupyterLite)"></a>'
            )
        out += [":::", ""]
    out += ["::::", ""]
    return "\n".join(out)

if __name__ == "__main__":
    dry = "--dry" in sys.argv
    for f in sorted(SRC.glob("Au??.md")):
        new = build(f.read_text(encoding="utf-8"), f.stem)
        n = new.count("grid-item-card")
        orig = len(re.findall(r'colab\.research\.google', f.read_text(encoding='utf-8')))
        flag = "" if n == orig else "  <-- MISMATCH"
        print(f"{f.name}: {n} cards (orig {orig})  | "
              f"{new.count('no%20browser')} JupyterLite{flag}")
        if dry:
            if f.name == "Au01.md":
                print("------ Au01 preview ------\n" + new)
        else:
            (DST / f.name).write_text(new, encoding="utf-8")
