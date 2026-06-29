#!/usr/bin/env python3
"""Gera mai_links.yml: por cada Aula (cartão), lista os problemas (nº do
enunciado) e deixa um campo `nb:` a preencher com o notebook de notebooks/MAI/.
Mostra, em comentário, os notebooks candidatos do capítulo correspondente.

NÃO sobrescreve um mai_links.yml já preenchido (cria mai_links.skeleton.yml).
Correr de MAI/ipy2webbook/:  python make_mai_skeleton.py
"""
import re, pathlib

HERE = pathlib.Path(__file__).resolve().parent
NB_DIR = HERE.parents[1] / "notebooks" / "MAI"

# Correspondência Aula -> Capítulo (deduzida das legendas do _toc.yml).
# Capítulos com 2 aulas repartem os problemas: Au03+Au04->Ch03, etc.
AU2CH = {
    "Au01": "Ch01", "Au02": "Ch02", "Au03": "Ch03", "Au04": "Ch03",
    "Au05": "Ch04", "Au06": "Ch05", "Au07": "Ch05", "Au08": "Ch06",
    "Au09": "Ch07", "Au10": "Ch07", "Au11": "Ch08", "Au12": "Ch08",
    "Au13": "Ch09",
}

prob_re = re.compile(r'Problema&nbsp;#([0-9a-z]+)')


def candidates(ch):
    if not ch:
        return []
    return sorted(p.name for p in NB_DIR.glob(f"MAI_{ch}_P*.ipynb"))


def main():
    out = [
        "# Preencher 'nb:' com o ficheiro de notebooks/MAI/ para cada problema.",
        "# Vazio = sem botão JupyterLite (mantém só o Colab).",
        "# Os candidatos do capítulo estão em comentário por baixo de cada aula.",
        "",
    ]
    hits = misses = 0
    for md in sorted(HERE.glob("Au??.md")):
        au = md.stem
        nums = prob_re.findall(md.read_text(encoding="utf-8"))
        ch = AU2CH.get(au, "")
        out.append(f"{au}:  # -> {ch}")
        for n in nums:
            guess = f"MAI_{ch}_P{n}.ipynb" if ch else ""
            if guess and (NB_DIR / guess).exists():
                out.append(f"  - {{p: {n}, nb: {guess}}}")
                hits += 1
            else:
                out.append(f"  - {{p: {n}, nb: }}  # sem P{n} exato em {ch} -- confirmar")
                misses += 1
        cand = candidates(ch)
        if cand:
            out.append(f"  # candidatos ({ch}): " + ", ".join(cand))
        out.append("")
    out.insert(3, f"# Auto-preenchidos: {hits}  |  por confirmar: {misses}")
    (HERE / "mai_links.skeleton.yml").write_text("\n".join(out), encoding="utf-8")
    print("Escrito mai_links.skeleton.yml  (renomeia para mai_links.yml e preenche)")
    for md in sorted(HERE.glob("Au??.md")):
        au = md.stem
        n = len(prob_re.findall(md.read_text(encoding="utf-8")))
        print(f"  {au} -> {AU2CH.get(au,'?')}: {n} cartões, "
              f"{len(candidates(AU2CH.get(au,'')))} notebooks no capítulo")


if __name__ == "__main__":
    main()
