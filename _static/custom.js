// DEMI · abrir num separador novo APENAS conteúdo "diferente" (recursos
// externos): URLs http(s) (Guia da NOVA, Google Colab) e o lançador
// JupyterLite (/lite/).
// A navegação interna do livro fica no MESMO separador — incluindo os cartões
// da página inicial (MAI/ MSI/ MSII/ ProjFLMEA/), que o Sphinx marca como
// "reference external" apesar de serem ligações relativas internas.
document.addEventListener("DOMContentLoaded", function () {
  var sel = "a[href^='http://'], a[href^='https://'], a[href*='/lite/']";
  document.querySelectorAll(sel).forEach(function (a) {
    a.setAttribute("target", "_blank");
    a.setAttribute("rel", "noopener noreferrer");
  });
});
