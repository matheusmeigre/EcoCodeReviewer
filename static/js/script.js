/**
 * Eco-Code Reviewer v4.0 - Frontend Logic
 * Integração com Groq API + UI Modernizada + Auto-detecção Inteligente
 */

// URL relativa funciona tanto local quanto na Vercel
const API_URL = window.location.origin;

// Variável global para armazenar a linguagem selecionada
let selectedLanguage = "auto";

// Timer para debounce da auto-detecção
let detectionTimer = null;

/**
 * Inicialização ao carregar a página
 */
document.addEventListener("DOMContentLoaded", function () {
  initializeLanguagePills();
  initializeCodeInput();
  initializeMoreLangsDropdown();
});

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

      // Feedback visual
      if (selectedLanguage === "auto") {
        showToast("🔍 Modo Auto-detectar ativado", "info", 2000);
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
 * Inicializa o textarea com auto-detecção inteligente
 */
function initializeCodeInput() {
  const codeInput = document.getElementById("codeInput");

  codeInput.addEventListener("input", function () {
    // Só detecta se estiver em modo "auto"
    if (selectedLanguage === "auto" && codeInput.value.trim().length > 30) {
      // Debounce de 500ms
      clearTimeout(detectionTimer);
      detectionTimer = setTimeout(() => {
        runAutoDetection(codeInput.value);
      }, 500);
    }
  });
}

/**
 * Executa a auto-detecção de linguagem em tempo real
 */
function runAutoDetection(code) {
  const detected = detectLanguage(code);
  const feedback = document.getElementById("detectionFeedback");

  if (detected) {
    feedback.innerHTML = `
      <i class="fas fa-check-circle"></i>
      Detectado: <strong>${getLanguageDisplayName(detected)}</strong>
    `;
    feedback.style.color = "var(--accent-green)";
  } else {
    feedback.innerHTML = `
      <i class="fas fa-question-circle"></i>
      Linguagem não identificada
    `;
    feedback.style.color = "var(--text-muted)";
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
  const codeInput = document.getElementById("codeInput");
  const code = codeInput.value.trim();
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
    console.error("Erro na análise:", error);
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
  explanationContent.innerHTML =
    data.explanationHtml || data.explanation || "Sem explicação disponível.";

  // Aplicar syntax highlighting no código dentro da explicação
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

  // Código otimizado
  const optimizedCode = data.optimizedCode || code;
  document.getElementById("optimizedCode").textContent = optimizedCode;

  // Aplicar syntax highlighting no código otimizado
  setTimeout(() => {
    const codeBlock = document.getElementById("optimizedCode");
    codeBlock.className = `language-${getLanguageForPrism(selectedLanguage)}`;
    Prism.highlightElement(codeBlock);
  }, 100);

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

/**
 * Limpa todos os campos
 */
function clearAll() {
  // Limpa textarea
  document.getElementById("codeInput").value = "";

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

      if (data.api_status !== "configured") {
        showToast(
          "⚠️ API Groq não configurada. Configure GROQ_API_KEY nas variáveis de ambiente da Vercel.",
          "warning"
        );
      }
    }
  } catch (error) {
    console.warn(
      "⚠️ Backend não está respondendo. Verifique se o servidor está rodando."
    );
    showToast(
      "Aviso: Não foi possível conectar ao servidor. Verifique se o backend está rodando.",
      "warning"
    );
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

// Event Listeners
document.addEventListener("DOMContentLoaded", function () {
  const codeInput = document.getElementById("codeInput");
  if (codeInput) {
    // Debounce para não processar a cada tecla
    let timeout;
    codeInput.addEventListener("input", function () {
      clearTimeout(timeout);
      timeout = setTimeout(() => {
        onCodeInput();
      }, 500);
    });

    // Detectar também no paste
    codeInput.addEventListener("paste", function () {
      setTimeout(() => {
        onCodeInput();
      }, 100);
    });
  }
});
