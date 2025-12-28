/**
 * Eco-Code Reviewer v4.0 - Frontend Logic
 * Integração com Groq API + CodeMirror + Auto-detecção Reativa
 */

// URL relativa funciona tanto local quanto na Vercel
const API_URL = window.location.origin;

// Variável global para armazenar a linguagem selecionada
let selectedLanguage = "auto";

// Timer para debounce da auto-detecção
let detectionTimer = null;

// Instância do CodeMirror
let codeEditor = null;

/**
 * Sistema de logging estruturado para Railway/Vercel
 */
const logger = {
  info: (message, data = {}) => {
    console.log(JSON.stringify({
      level: 'INFO',
      timestamp: new Date().toISOString(),
      message,
      ...data
    }));
  },
  warn: (message, data = {}) => {
    console.warn(JSON.stringify({
      level: 'WARN',
      timestamp: new Date().toISOString(),
      message,
      ...data
    }));
  },
  error: (message, error = null, data = {}) => {
    console.error(JSON.stringify({
      level: 'ERROR',
      timestamp: new Date().toISOString(),
      message,
      error: error ? error.toString() : null,
      stack: error?.stack,
      ...data
    }));
  },
  debug: (message, data = {}) => {
    if (window.location.hostname === 'localhost') {
      console.log(JSON.stringify({
        level: 'DEBUG',
        timestamp: new Date().toISOString(),
        message,
        ...data
      }));
    }
  }
};

/**
 * Inicialização ao carregar a página
 */
document.addEventListener("DOMContentLoaded", function () {
  logger.info("Aplicação iniciada");

  // Verifica se CodeMirror está disponível
  if (typeof CodeMirror === "undefined") {
    logger.error("CodeMirror não carregado");
    showToast(
      "Erro: Editor de código não carregou. Recarregue a página.",
      "danger",
      10000
    );
    return;
  }

  logger.info("CodeMirror carregado", { version: CodeMirror.version });

  initializeCodeMirror();
  initializeLanguagePills();
  initializeMoreLangsDropdown();
});

/**
 * Inicializa o CodeMirror Editor
 */
function initializeCodeMirror() {
  const textarea = document.getElementById("codeInput");
  const container = document.getElementById("codeMirrorContainer");

  if (!container) {
    logger.error("Container CodeMirror não encontrado");
    return;
  }

  try {
    codeEditor = CodeMirror(container, {
      value: "", // Inicia vazio para usar o placeholder
      mode: "text/plain",
      theme: "material-darker",
      lineNumbers: true,
      lineWrapping: true,
      indentUnit: 4,
      tabSize: 4,
      indentWithTabs: false,
      scrollbarStyle: "simple",
      matchBrackets: true,
      autoCloseBrackets: true,
      placeholder: `Cole seu código aqui para análise...

Exemplos suportados:

Python:
  def calcular_soma(numeros):
      resultado = 0
      for i in range(len(numeros)):
          resultado += numeros[i]
      return resultado

SQL:
  SELECT u.nome, COUNT(p.id) as total
  FROM usuarios u
  INNER JOIN pedidos p ON u.id = p.usuario_id
  WHERE p.data > '2025-01-01'
  GROUP BY u.nome

JavaScript:
  function processar(items) {
    const resultado = [];
    for (let i = 0; i < items.length; i++) {
      if (items[i].ativo) {
        resultado.push(items[i]);
      }
    }
    return resultado;
  }

Pressione Ctrl+Enter para analisar`,
      tabSize: 4,
      indentWithTabs: false,
      scrollbarStyle: "simple",
      matchBrackets: true,
      autoCloseBrackets: true,
      extraKeys: {
        "Ctrl-Enter": function () {
          analyzeCode();
        },
        "Cmd-Enter": function () {
          analyzeCode();
        },
      },
    });

    // Force refresh para garantir que o editor seja renderizado
    setTimeout(() => {
      if (codeEditor) {
        codeEditor.refresh();
      }
    }, 100);

    // Auto-detecção reativa enquanto digita
    codeEditor.on("change", function (cm) {
      // Só detecta se estiver em modo "auto"
      if (selectedLanguage === "auto") {
        const code = cm.getValue().trim();
        if (code.length > 30) {
          // Debounce de 400ms para performance
          clearTimeout(detectionTimer);
          detectionTimer = setTimeout(() => {
            runAutoDetectionRealtime(code);
          }, 400);
        }
      }
    });

    logger.info("CodeMirror inicializado com sucesso");
  } catch (error) {
    logger.error("Erro ao inicializar CodeMirror", error);
    // Fallback: mostrar textarea normal
    if (textarea) {
      textarea.style.display = "block";
      textarea.className = "code-editor";
    }
  }
}

/**
 * Inicializa os botões de seleção de linguagem (Pills)
 */
function initializeLanguagePills() {
  const pills = document.querySelectorAll(".lang-pill:not(.lang-pill-more)");

  pills.forEach((pill) => {
    pill.addEventListener("click", function () {
      // Remove active de todos
      pills.forEach((p) => p.classList.remove("active"));

      // Adiciona active no clicado
      this.classList.add("active");

      // Atualiza linguagem selecionada
      selectedLanguage = this.getAttribute("data-lang");
      document.getElementById("languageSelect").value = selectedLanguage;

      // Limpa feedback de detecção
      document.getElementById("detectionFeedback").innerHTML = "";

      // Atualiza modo do CodeMirror se não for auto
      if (selectedLanguage !== "auto" && codeEditor) {
        updateCodeMirrorMode(selectedLanguage);
      }

      // Feedback visual
      if (selectedLanguage === "auto") {
        showToast("🔍 Modo Auto-detectar ativado", "info", 2000);
        // Dispara detecção imediata
        const code = codeEditor.getValue().trim();
        if (code.length > 30) {
          runAutoDetectionRealtime(code);
        }
      } else {
        showToast(
          `Linguagem selecionada: ${selectedLanguage.toUpperCase()}`,
          "success",
          2000
        );
      }
    });
  });
}

/**
 * Inicializa o dropdown de "Mais linguagens"
 */
function initializeMoreLangsDropdown() {
  const moreBtn = document.getElementById("moreLangsBtn");
  const dropdown = document.getElementById("moreLangsDropdown");
  const options = document.querySelectorAll(".lang-option");

  // Toggle dropdown
  moreBtn.addEventListener("click", function (e) {
    e.stopPropagation();
    dropdown.classList.toggle("show");
  });

  // Selecionar linguagem do dropdown
  options.forEach((option) => {
    option.addEventListener("click", function () {
      const lang = this.getAttribute("data-lang");

      // Atualiza linguagem
      selectedLanguage = lang;
      document.getElementById("languageSelect").value = lang;

      // Remove active de todos os pills
      document
        .querySelectorAll(".lang-pill")
        .forEach((p) => p.classList.remove("active"));

      // Fecha dropdown
      dropdown.classList.remove("show");

      // Atualiza CodeMirror
      if (codeEditor) {
        updateCodeMirrorMode(lang);
      }

      // Feedback visual
      showToast(
        `Linguagem selecionada: ${lang.toUpperCase()}`,
        "success",
        2000
      );

      // Limpa feedback de detecção
      document.getElementById("detectionFeedback").innerHTML = "";
    });
  });

  // Fechar dropdown ao clicar fora
  document.addEventListener("click", function (e) {
    if (!moreBtn.contains(e.target) && !dropdown.contains(e.target)) {
      dropdown.classList.remove("show");
    }
  });
}

/**
 * Atualiza o modo (syntax highlighting) do CodeMirror
 */
function updateCodeMirrorMode(language) {
  const modeMap = {
    python: "text/x-python",
    javascript: "text/javascript",
    typescript: "text/typescript",
    java: "text/x-java",
    csharp: "text/x-csharp",
    sql: "text/x-sql",
    nosql: "text/javascript", // MongoDB usa JS
    react: "text/jsx",
    delphi: "text/x-pascal",
  };

  const mode = modeMap[language] || "text/plain";
  codeEditor.setOption("mode", mode);
}

/**
 * Executa a auto-detecção em tempo real (chamada enquanto digita)
 */
function runAutoDetectionRealtime(code) {
  const detected = detectLanguage(code);
  const feedback = document.getElementById("detectionFeedback");

  if (detected) {
    feedback.innerHTML = `
      <i class="fas fa-check-circle"></i>
      Detectado: <strong>${getLanguageDisplayName(detected)}</strong>
    `;
    feedback.style.color = "var(--accent-green)";

    // Atualiza CodeMirror para a linguagem detectada
    if (codeEditor) {
      updateCodeMirrorMode(detected);
    }
  } else {
    feedback.innerHTML = `
      <i class="fas fa-question-circle"></i>
      Linguagem não identificada
    `;
    feedback.style.color = "var(--text-muted)";

    // Reseta para plain text
    if (codeEditor) {
      codeEditor.setOption("mode", "text/plain");
    }
  }
}

/**
 * Retorna o nome de exibição da linguagem
 */
function getLanguageDisplayName(lang) {
  const names = {
    python: "Python",
    javascript: "JavaScript",
    typescript: "TypeScript",
    java: "Java",
    csharp: "C#",
    sql: "SQL",
    nosql: "NoSQL/MongoDB",
    react: "React/ReactJS",
    delphi: "Delphi",
  };
  return names[lang] || lang.toUpperCase();
}

/**
 * Auto-detecção de linguagem baseada em padrões de código (MELHORADA)
 */
function detectLanguage(code) {
  // Padrões de detecção aprimorados
  const patterns = {
    python: [
      /^\s*def\s+\w+\s*\(/m,
      /^\s*class\s+\w+.*:/m,
      /^\s*import\s+\w+/m,
      /^\s*from\s+\w+\s+import/m,
      /^\s*@\w+/m,
      /\bprint\s*\(/,
      /\belif\b/,
      /:\s*$/m, // Dois pontos no final da linha (Python)
    ],
    javascript: [
      /^\s*function\s+\w+\s*\(/m,
      /^\s*const\s+\w+\s*=/m,
      /^\s*let\s+\w+\s*=/m,
      /^\s*var\s+\w+\s*=/m,
      /console\.log\(/,
      /=>\s*{/,
      /\brequire\s*\(/,
      /\bexport\s+(default|const|function)/m,
    ],
    typescript: [
      /:\s*(string|number|boolean|any)\s*[;=\)]/,
      /^\s*interface\s+\w+/m,
      /^\s*type\s+\w+\s*=/m,
      /<\w+>/,
      /as\s+(string|number|boolean)/,
      /:\s*\w+\[\]/,
    ],
    java: [
      /^\s*public\s+class\s+\w+/m,
      /^\s*private\s+(static\s+)?\w+\s+\w+/m,
      /^\s*protected\s+/m,
      /System\.out\.println/,
      /^\s*import\s+java\./m,
      /\bnew\s+\w+\s*\(/,
      /\bpublic\s+static\s+void\s+main/m,
    ],
    csharp: [
      /^\s*public\s+class\s+\w+/m,
      /^\s*private\s+\w+\s+\w+/m,
      /^\s*using\s+System/m,
      /Console\.WriteLine/,
      /\bstring\[\]\s+args\b/,
      /\bnamespace\s+\w+/m,
      /\bvar\s+\w+\s*=\s*new\b/,
    ],
    sql: [
      /^\s*SELECT\s+/im,
      /^\s*INSERT\s+INTO/im,
      /^\s*UPDATE\s+\w+\s+SET/im,
      /^\s*DELETE\s+FROM/im,
      /^\s*CREATE\s+TABLE/im,
      /\bJOIN\b/i,
      /\bWHERE\b/i,
      /\bGROUP\s+BY\b/i,
    ],
    react: [
      /^\s*import\s+React/m,
      /from\s+['"]react['"]/,
      /useState\s*\(/,
      /useEffect\s*\(/,
      /<\/\w+>/,
      /className=/,
      /\bJSX\b/,
      /return\s*\(/,
    ],
    delphi: [
      /^\s*procedure\s+\w+/im,
      /^\s*function\s+\w+.*:\s*\w+/im,
      /^\s*begin\b/im,
      /^\s*end\s*;/im,
      /\bvar\s+\w+\s*:\s*\w+/im,
      /\bunit\s+\w+/im,
    ],
    nosql: [
      /db\.\w+\.find\(/,
      /db\.\w+\.insert/,
      /db\.\w+\.update/,
      /\$match\s*:/,
      /\$group\s*:/,
      /\$project\s*:/,
      /\$lookup\s*:/,
    ],
  };

  // Contagem de matches para cada linguagem
  const scores = {};

  for (const [lang, rules] of Object.entries(patterns)) {
    scores[lang] = 0;
    for (const pattern of rules) {
      if (pattern.test(code)) {
        scores[lang]++;
      }
    }
  }

  // Encontrar linguagem com mais matches
  let maxScore = 0;
  let detectedLang = null;

  for (const [lang, score] of Object.entries(scores)) {
    if (score > maxScore) {
      maxScore = score;
      detectedLang = lang;
    }
  }

  // Retorna apenas se houver confiança suficiente (2+ matches)
  return maxScore >= 2 ? detectedLang : null;
}

/**
 * Função principal de análise de código
 */
async function analyzeCode() {
  // Pega o código do CodeMirror ao invés do textarea
  const code = codeEditor ? codeEditor.getValue().trim() : "";
  let language = selectedLanguage; // Usa a variável global

  if (!code) {
    showToast("Por favor, insira um código para análise.", "warning");
    return;
  }

  // Auto-detectar se necessário
  if (language === "auto") {
    const detected = detectLanguage(code);
    if (detected) {
      language = detected;
      showToast(
        `🔍 Linguagem detectada: ${getLanguageDisplayName(detected)}`,
        "info"
      );
    } else {
      // Fallback: Envia como "auto" e deixa o backend/LLM decidir
      showToast(
        "⚠️ Linguagem não identificada localmente. A IA tentará detectar...",
        "warning"
      );
      language = "auto"; // Mantém como auto para o backend processar
    }
  }

  // Transição de estados
  showLoading();

  // Desabilitar botão
  const analyzeBtn = document.getElementById("analyzeBtn");
  analyzeBtn.disabled = true;
  analyzeBtn.innerHTML =
    '<i class="fas fa-spinner fa-spin"></i> <span class="btn-text">Analisando...</span>';

  try {
    const response = await fetch(`${API_URL}/analyze`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ code: code, language: language }),
    });

    if (!response.ok) {
      throw new Error(`Erro HTTP: ${response.status}`);
    }

    const result = await response.json();

    if (!result.success) {
      throw new Error(result.error || "Erro desconhecido na análise");
    }

    displayResults(result);
    showToast("✅ Análise semântica concluída via IA!", "success");
  } catch (error) {
    logger.error("Erro na análise de código", error);
    showToast(`Erro ao analisar código: ${error.message}`, "danger");
    showEmptyState();
  } finally {
    analyzeBtn.disabled = false;
    analyzeBtn.innerHTML =
      '<i class="fas fa-search"></i> <span class="btn-text">Analisar</span>';
  }
}

/**
 * Exibe os resultados da análise v4.0 (Groq API)
 */
function displayResults(result) {
  // Esconder empty state e mostrar results
  document.getElementById("emptyState").style.display = "none";
  document.getElementById("loadingState").style.display = "none";
  document.getElementById("resultsView").style.display = "block";

  const data = result.data;
  const model = result.model || "gpt-4o-mini";
  const tokens = result.tokens || 0;

  // Quality Score
  const scoreDisplay = document.getElementById("scoreDisplay");
  const scoreStatus = document.getElementById("scoreStatus");
  const scoreMini = document.getElementById("scoreMini");
  const scoreMiniValue = document.getElementById("scoreMiniValue");

  const qualityScore = data.qualityScore || 0;
  scoreDisplay.textContent = qualityScore;
  scoreMiniValue.textContent = qualityScore;
  scoreMini.style.display = "block";

  // Colorir score
  scoreDisplay.classList.remove("score-good", "score-medium", "score-poor");
  if (qualityScore >= 90) {
    scoreDisplay.classList.add("score-good");
    scoreStatus.innerHTML = "✨ Código Excelente!";
  } else if (qualityScore >= 70) {
    scoreDisplay.classList.add("score-medium");
    scoreStatus.innerHTML = "⚠️ Otimizações Recomendadas";
  } else if (qualityScore >= 50) {
    scoreDisplay.classList.add("score-poor");
    scoreStatus.innerHTML = "🔧 Necessita Refatoração";
  } else {
    scoreDisplay.classList.add("score-poor");
    scoreStatus.innerHTML = "🚨 Problemas Críticos Detectados";
  }

  // Métricas v4.0
  const metrics = data.metrics || {};
  document.getElementById("complexityReduction").textContent =
    metrics.complexityReduction || "N/A";
  document.getElementById("memoryImpact").textContent =
    metrics.memoryImpact || "N/A";
  document.getElementById("estimatedSpeedup").textContent =
    metrics.estimatedSpeedup || "N/A";
  document.getElementById("energySavings").textContent =
    metrics.energySavings || "N/A";

  // Model Badge
  document.getElementById("modelBadge").textContent = model.toUpperCase();

  // Explanation (Markdown já convertido para HTML pelo backend)
  const explanationContent = document.getElementById("explanationContent");
  let explanationHtml =
    data.explanationHtml || data.explanation || "Sem explicação disponível.";

  // CRÍTICO: Remover blocos de código grandes que não deveriam estar na explicação
  // Criar elemento temporário para manipular DOM
  const tempDiv = document.createElement("div");
  tempDiv.innerHTML = explanationHtml;

  // Remover blocos <pre><code> que contenham mais de 5 linhas (código completo)
  tempDiv.querySelectorAll("pre code").forEach((codeBlock) => {
    const lines = codeBlock.textContent.split("\n").length;
    if (lines > 5 || codeBlock.classList.contains("language-none")) {
      // Remove o bloco <pre> inteiro
      codeBlock.closest("pre").remove();
    }
  });

  // Remover headers que digam "Código Otimizado" ou similares
  tempDiv.querySelectorAll("h1, h2, h3, h4, h5, h6").forEach((header) => {
    const text = header.textContent.toLowerCase();
    if (text.includes("código otimizado") || text.includes("optimized code")) {
      header.remove();
    }
  });

  explanationContent.innerHTML = tempDiv.innerHTML;

  // Aplicar syntax highlighting no código dentro da explicação (apenas exemplos pequenos)
  setTimeout(() => {
    explanationContent.querySelectorAll("pre code").forEach((block) => {
      Prism.highlightElement(block);
    });
  }, 100);

  // Issues
  if (data.hasIssues && data.issues && data.issues.length > 0) {
    displayIssues(data.issues);
    document.getElementById("issuesSection").style.display = "block";
  } else {
    document.getElementById("issuesSection").style.display = "none";
  }

  // Código otimizado - preservar formatação com syntax highlighting
  let optimizedCode = data.optimizedCode;

  // CRÍTICO: Verificar se o backend retornou apenas placeholder
  const placeholders = [
    "// Código otimizado aqui (se aplicável)",
    "// Código otimizado disponível abaixo",
    "// Código otimizado abaixo",
    "// Código otimizado",
  ];

  if (!optimizedCode || placeholders.some((p) => optimizedCode.trim() === p)) {
    logger.warn("Backend retornou placeholder, usando código original");
    // Pegar código original do editor
    optimizedCode = codeEditor ? codeEditor.getValue() : "";
  }

  const codeBlock = document.getElementById("optimizedCode");

  if (!codeBlock) {
    logger.error("Elemento optimizedCode não encontrado no DOM");
    return;
  }

  logger.debug("Código otimizado preparado para exibição", { 
    length: optimizedCode.length,
    preview: optimizedCode.substring(0, 100)
  });

  const preElement = codeBlock.parentElement;

  // Configurar estilos do <pre> para preservar espaços
  preElement.style.whiteSpace = "pre";
  preElement.style.tabSize = "4";

  // Normalizar quebras de linha
  const normalizedCode = optimizedCode
    .replace(/\r\n/g, "\n")
    .replace(/\r/g, "\n");

  // Inserir código diretamente (textContent preserva formatação)
  codeBlock.textContent = normalizedCode;
  codeBlock.style.whiteSpace = "pre";
  codeBlock.style.display = "block";

  // Aplicar classe de linguagem para syntax highlighting
  codeBlock.className = `language-${getLanguageForPrism(selectedLanguage)}`;

  // Aplicar Prism manualmente
  setTimeout(() => {
    Prism.manual = true;
    Prism.highlightElement(codeBlock);
  }, 10);

  // Footer com info de tokens
  updateFooterInfo(tokens);
}

/**
 * Mapeia linguagem selecionada para classe Prism.js
 */
function getLanguageForPrism(language) {
  const map = {
    python: "python",
    java: "java",
    csharp: "csharp",
    delphi: "pascal",
    javascript: "javascript",
    typescript: "typescript",
    react: "jsx",
    sql: "sql",
    nosql: "javascript",
  };
  return map[language] || "javascript";
}

/**
 * Atualiza rodapé com informações de uso da API
 */
function updateFooterInfo(tokens) {
  const footer = document.querySelector(".mini-footer");
  const existingInfo = document.getElementById("apiInfo");

  if (existingInfo) {
    existingInfo.remove();
  }

  const apiInfo = document.createElement("span");
  apiInfo.id = "apiInfo";
  apiInfo.className = "ms-3 text-muted";
  apiInfo.style.fontSize = "0.85em";
  apiInfo.innerHTML = `<i class="fas fa-robot"></i> Análise via IA | Tokens: ${tokens}`;

  footer.querySelector(".container-fluid").appendChild(apiInfo);
}

/**
 * Exibe os problemas detectados
 */
function displayIssues(issues) {
  const issuesList = document.getElementById("issuesList");
  issuesList.innerHTML = "";

  issues.forEach((issue) => {
    const issueDiv = document.createElement("div");
    issueDiv.className = `issue-item severity-${issue.severity}`;

    issueDiv.innerHTML = `
            <div class="issue-title">
                <i class="fas fa-exclamation-circle"></i>
                <span>${issue.title}</span>
                <span class="issue-badge ${issue.severity}">${getSeverityLabel(
      issue.severity
    )}</span>
            </div>
            <div class="issue-impact">
                <strong>Descrição:</strong> ${issue.description}
            </div>
            <div class="issue-impact">
                <strong>Impacto:</strong> ${issue.impact}
            </div>
            ${
              issue.originalCode
                ? `<div class="issue-code"><code>${escapeHtml(
                    issue.originalCode
                  )}</code></div>`
                : ""
            }
        `;

    issuesList.appendChild(issueDiv);
  });
}

/**
 * Retorna o label amigável para a severidade
 */
function getSeverityLabel(severity) {
  const labels = {
    critical: "Crítico",
    high: "Alta",
    medium: "Média",
    low: "Baixa",
  };
  return labels[severity] || severity;
}

/**
 * Escape HTML para prevenir XSS
 */
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Copia o código otimizado para o clipboard
 */
async function copyOptimizedCode() {
  const code = document.getElementById("optimizedCode").textContent;

  try {
    await navigator.clipboard.writeText(code);
    showToast("Código copiado para a área de transferência!", "success");
  } catch (err) {
    console.error("Erro ao copiar:", err);
    showToast("Erro ao copiar código. Tente selecionar manualmente.", "danger");
  }
}
logger.error("Erro ao copiar código
/**
 * Limpa todos os campos
 */
function clearAll() {
  // Limpa CodeMirror
  if (codeEditor) {
    codeEditor.setValue("");
    codeEditor.setOption("mode", "text/plain");
  }

  // Reseta para modo auto-detectar
  selectedLanguage = "auto";
  document.getElementById("languageSelect").value = "auto";

  // Reseta pills visuais
  document
    .querySelectorAll(".lang-pill")
    .forEach((p) => p.classList.remove("active"));
  document
    .querySelector('.lang-pill[data-lang="auto"]')
    .classList.add("active");

  // Limpa feedback de detecção
  document.getElementById("detectionFeedback").innerHTML = "";

  // Mostra empty state
  showEmptyState();
  document.getElementById("scoreMini").style.display = "none";

  // Remover info de API
  const apiInfo = document.getElementById("apiInfo");
  if (apiInfo) {
    apiInfo.remove();
  }

  showToast("✨ Interface resetada", "info", 2000);
}

/**
 * Mostra o estado vazio
 */
function showEmptyState() {
  document.getElementById("emptyState").style.display = "flex";
  document.getElementById("loadingState").style.display = "none";
  document.getElementById("resultsView").style.display = "none";
}

/**
 * Mostra o loading
 */
function showLoading() {
  document.getElementById("emptyState").style.display = "none";
  document.getElementById("loadingState").style.display = "flex";
  document.getElementById("resultsView").style.display = "none";
}

/**
 * Exibe um toast (notificação)
 */
function showToast(message, type = "info", duration = 5000) {
  // Remover toasts anteriores
  const existingToast = document.querySelector(".custom-toast");
  if (existingToast) {
    existingToast.remove();
  }

  const toastDiv = document.createElement("div");
  toastDiv.className = `alert alert-${type} alert-dismissible fade show custom-toast`;
  toastDiv.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        max-width: 500px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: slideInRight 0.3s ease;
    `;

  toastDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;

  document.body.appendChild(toastDiv);

  // Auto-remover após duração especificada
  setTimeout(() => {
    toastDiv.classList.remove("show");
    setTimeout(() => toastDiv.remove(), 300);
  }, duration);
}

/**
 * Permite análise com Ctrl+Enter
 */
document.getElementById("codeInput")?.addEventListener("keydown", function (e) {
  if (e.ctrlKey && e.key === "Enter") {
    analyzeCode();
  }
});

/**
 * Verificação de saúde da API ao carregar
 */
window.addEventListener("DOMContentLoaded", async () => {
  try {
    const response = await fetch(`${API_URL}/health`);
    if (response.ok) {
      const data = await response.json();
      console.log(`✅ Backend v${data.version} conectado!`);
      console.log(`🤖 Motor: ${data.engine} (${data.model})`);
      console.log(`🔑 API Status: ${data.api_status}`);

      logger.info("Backend conectado", {
        version: data.version,
        engine: data.engine,
        model: data.model,
        api_status: data.api_status
      });

      if (data.api_status !== "configured") {
        logger.warn("API Groq não configurada");
        showToast(
          "⚠️ API Groq não configurada. Configure GROQ_API_KEY nas variáveis de ambiente da Vercel.",
          "warning"
        );
      }
    }
  } catch (error) {
    logger.warn("Backend não respondeu ao healthcheck", error);
  }
});

// Adicionar animação de slide CSS
const style = document.createElement("style");
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    .markdown-content pre {
        background: #2d2d2d;
        border-radius: 8px;
        padding: 1rem;
        overflow-x: auto;
    }
    
    .markdown-content code {
        font-family: 'Fira Code', monospace;
    }
    
    .issue-code {
        margin-top: 0.5rem;
        padding: 0.5rem;
        background: #f8f9fa;
        border-left: 3px solid #ff6b6b;
        border-radius: 4px;
    }
    
    .issue-code code {
        font-family: 'Fira Code', monospace;
        font-size: 0.9em;
    }
`;
document.head.appendChild(style);
