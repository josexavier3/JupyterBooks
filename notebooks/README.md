# notebooks/ — fonte dos `.ipynb` executáveis (JupyterLite)

Esta pasta é a **fonte única** dos notebooks que correm no browser via JupyterLite.
Tudo o que estiver aqui aparece no explorador de ficheiros da app publicada.

## Estrutura sugerida

```
notebooks/
  requirements.txt        # pacotes que os notebooks importam (doc + teste local)
  demo/                   # notebook de demonstração (apagar quando já não fizer falta)
  MSI/                    # Au01_P1.ipynb, Au01_P2.ipynb, ...
  MSII/
  MAI/
  ProjFLMEA/
```

## Migrar do Google Colab para aqui

Os problemas estão hoje em Colab/Drive (links nos cartões `AuNN.md`). Para cada um:

1. No Colab: **Ficheiro → Transferir → .ipynb**.
2. Guardar em `notebooks/<UC>/AuNN_Pk.ipynb` (nome estável, sem espaços).
3. Confirmar que só usa pacotes do Pyodide (`numpy`, `scipy`, `matplotlib`,
   `sympy`, `pandas`). Para outros, acrescentar no notebook uma 1.ª célula:
   `%pip install nome-do-pacote`.
4. Reconstruir: `bash build_lite.sh`.

## Ligar os cartões do livro ao JupyterLite

Cada notebook fica acessível por URL no JupyterLite, por exemplo:

```
<base>/lite/lab/index.html?path=MSI/Au01_P1.ipynb
```

Podes manter o badge do Colab **e** acrescentar um botão "Abrir no browser
(JupyterLite)" nos cartões — ver `INTERACTIVE.md` na raiz para o passo de geração.
