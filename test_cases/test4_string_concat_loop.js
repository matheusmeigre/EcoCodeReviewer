// TESTE 4: String Concatenação em Loop (Geral - JavaScript neste caso)
// Expectativa: Deve detectar concatenação em loop e sugerir join() ou array

function buildReport(items) {
  let report = "";
  for (let i = 0; i < items.length; i++) {
    report += items[i].name + ", ";
  }
  return report;
}

function generateHTML(data) {
  let html = "";
  for (let item of data) {
    html += "<div>" + item + "</div>";
  }
  return html;
}
