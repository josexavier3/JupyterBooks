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

  // Inserir link "← UC Home" no topo da barra lateral de navegação,
  // em todas as páginas que NÃO são já a página raiz da UC.
  var UC_MAP = {
    "MAI":       { file: "mai.html",       label: "Mecânica Aplicada I" },
    "MSI":       { file: "msi.html",       label: "Mecânica dos Sólidos I" },
    "MSII":      { file: "msii.html",      label: "Mecânica dos Sólidos II" },
    "ProjFLMEA": { file: "projflmea.html", label: "Proj. FLMEA" }
  };

  var pathParts = window.location.pathname.replace(/\/+$/, "").split("/");
  var ucKey = null;
  for (var i = 0; i < pathParts.length; i++) {
    if (UC_MAP[pathParts[i]]) { ucKey = pathParts[i]; break; }
  }
  if (!ucKey) return;

  var uc = UC_MAP[ucKey];
  var currentFile = pathParts[pathParts.length - 1];
  if (currentFile === uc.file) return; // já na página raiz

  var navList = document.querySelector(".bd-docs-nav ul.nav.bd-sidenav");
  if (!navList) return;

  var li = document.createElement("li");
  li.className = "toctree-l1 uc-home-link";
  li.innerHTML = '<a class="reference internal" href="' + uc.file + '">' + uc.label + '</a>';
  navList.insertBefore(li, navList.firstChild);
});
