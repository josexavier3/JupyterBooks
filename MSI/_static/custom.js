// DEMI · abrir num separador novo APENAS conteúdo "diferente" (recursos
// externos): links externos do Sphinx (class "external"), URLs http(s)
// (Guia da NOVA, Google Colab) e o lançador JupyterLite (/lite/).
// A navegação interna do livro (barra lateral, anterior/seguinte, logo->índice,
// âncoras) fica no MESMO separador.
document.addEventListener("DOMContentLoaded", function () {
  var sel = "a.external, a[href^='http://'], a[href^='https://'], a[href*='/lite/']";
  document.querySelectorAll(sel).forEach(function (a) {
    a.setAttribute("target", "_blank");
    a.setAttribute("rel", "noopener noreferrer");
  });
});
