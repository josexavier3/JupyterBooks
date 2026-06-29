// DEMI · abrir ligações num separador novo.
// Abrange: links externos do Sphinx (class "external"), URLs http(s)
// (Guia da NOVA, Google Colab), o lançador JupyterLite (/lite/) e os links
// de navegação da BARRA LATERAL esquerda (nav.bd-docs-nav — aulas/secções) e
// os botões anterior/seguinte do rodapé (a.left-prev / a.right-next).
// NÃO afeta âncoras na própria página.
document.addEventListener("DOMContentLoaded", function () {
  var sel = "a.external, a[href^='http://'], a[href^='https://'], a[href*='/lite/'], nav.bd-docs-nav a[href], a.left-prev, a.right-next";
  document.querySelectorAll(sel).forEach(function (a) {
    a.setAttribute("target", "_blank");
    a.setAttribute("rel", "noopener noreferrer");
  });
});
