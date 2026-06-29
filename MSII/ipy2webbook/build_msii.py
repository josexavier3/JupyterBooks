#!/usr/bin/env python3
"""Build the MSII Jupyter Book pages from the LaTeX enunciados.
Each Enunciados/Aulas/CAPnn.tex has \\chapter{Title.} and ordered
\\colabkey{<drive-id>} entries (one per problem). Generates AuNN.md (card
grid linking to Colab) and _toc.yml."""
import re, pathlib, yaml

HERE = pathlib.Path(__file__).resolve().parent          # MSII/ipy2webbook
ROOT = HERE.parents[1]                                   # raiz JupyterBooks
# Fonte LaTeX = pasta de trabalho (ano/UC), via sources.yml -> não duplicada aqui.
_CFG = yaml.safe_load((ROOT / "sources.yml").read_text(encoding="utf-8"))
AULAS = (ROOT / _CFG["units"]["MSII"]["tex"]).resolve()
WEB = HERE
BADGE = "https://colab.research.google.com/assets/colab-badge.svg"
COLAB = "https://colab.research.google.com/drive/{}?authuser=1"

# Edição publicada dos notebooks (preenchida por ../../sync_notebooks.py) e link
# para a app JupyterLite. Só é acrescentado o botão se o ficheiro existir.
NB_DIR = pathlib.Path(__file__).resolve().parents[2] / "notebooks" / "MSII"
LITE = "../lite/lab/index.html?path=MSII/{}"
JLITE = ("https://img.shields.io/badge/Abrir-no%20browser-F37626"
         "?logo=jupyter&logoColor=white")

chapter_re = re.compile(r'\\chapter\{([^}]*)\}')
key_re = re.compile(r'\\colabkey\{([A-Za-z0-9_-]+)\}')

def card(num, key, au_idx):
    url = COLAB.format(key)
    out = [
        f":::{{grid-item-card}} Problema&nbsp;#{num}",
        ":text-align: center",
        f'<a href="{url}" target="_blank" rel="noopener">'
        f'<img src="{BADGE}" alt="Abrir no Colab"></a>',
    ]
    nb = f"MSII_Au{au_idx:02d}_P{num}.ipynb"
    if (NB_DIR / nb).exists():
        out.append(
            f'<br><a href="{LITE.format(nb)}" target="_blank" rel="noopener">'
            f'<img src="{JLITE}" alt="Abrir no browser (JupyterLite)"></a>'
        )
    out.append(":::\n")
    return "\n".join(out)

parts = []
caps = sorted(AULAS.glob("CAP*.tex"))
for i, f in enumerate(caps, start=1):
    txt = f.read_text(encoding="utf-8")
    title = chapter_re.search(txt).group(1).strip()
    title = title.rstrip(".").strip() + "."          # normalise one trailing dot
    keys = key_re.findall(txt)
    au = f"Au{i:02d}"
    body = [f"# Aula Prática {i}", "", f"*{title}*", "",
            "::::{grid} 2 3 4 4", ":gutter: 3", ""]
    for n, k in enumerate(keys, start=1):
        body.append(card(n, k, i))
    body += ["::::", ""]
    (WEB / f"{au}.md").write_text("\n".join(body), encoding="utf-8")
    parts.append((title.rstrip("."), au))
    print(f"{au}: {len(keys)} problems  | {title}")

toc = ["# Table of contents — https://jupyterbook.org/customize/toc.html",
       "format: jb-book", "root: msii", "parts:"]
for caption, au in parts:
    toc += [f'  - caption: "{caption}"',
            "    chapters:",
            f"      - file: {au}"]
(WEB / "_toc.yml").write_text("\n".join(toc) + "\n", encoding="utf-8")
print("wrote _toc.yml with", len(parts), "parts")
