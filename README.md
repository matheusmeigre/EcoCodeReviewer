# 🌱 Eco-Code Reviewer v2.0

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![AI-Powered](https://img.shields.io/badge/AI-Groq%20LLaMA-orange)](https://groq.com/)

**Ferramenta inteligente de análise de código com foco em sustentabilidade e performance.**

Analise código em **24 linguagens** com recomendações otimizadas para eco-eficiência, detectando problemas de performance, segurança e manutenibilidade.

---

## ✨ Características

- 🤖 **Análise Semântica via IA** (Groq LLaMA 3.3-70B)
- 🔍 **18 Plugins Especializados** para diferentes linguagens
- 🌍 **24 Linguagens Suportadas**
- 📊 **Métricas de Eco-Impact** (CPU, memória, energia)
- ⚡ **Detecção Automática de Linguagem**
- 🎨 **Interface Web Responsiva** com CodeMirror
- 🔧 **Arquitetura Modular** baseada em plugins

---

## 🚀 Linguagens Suportadas

### Backend
- Python, JavaScript/TypeScript, Go, Rust, PHP, Ruby

### Frontend
- React, Vue, Angular, Svelte

### Mobile
- Kotlin, Swift

### Infrastructure & DevOps
- Bash, YAML, Dockerfile, Terraform

---

## 📦 Instalação

### Pré-requisitos
- Python 3.9+
- Chave API Groq (gratuita em [console.groq.com](https://console.groq.com))

### Passos

1. **Clone o repositório:**
```bash
git clone https://github.com/SEU_USUARIO/ecocoder-review.git
cd ecocoder-review
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Configure a chave API:**
```bash
# Windows
set GROQ_API_KEY=sua_chave_aqui

# Linux/Mac
export GROQ_API_KEY=sua_chave_aqui
```

4. **Execute a aplicação:**
```bash
python app_v2.py
```

5. **Acesse no navegador:**
```
http://localhost:5000
```

---

## 🎯 Como Usar

1. **Cole seu código** no editor
2. **Selecione a linguagem** (ou use detecção automática)
3. **Clique em "Analisar"**
4. **Revise os resultados:**
   - Score de qualidade (0-100)
   - Issues detectados com severidade
   - Código otimizado sugerido
   - Métricas de eco-impacto
   - Análise semântica via IA

---

## 🏗️ Arquitetura

```
review_engine/
├── core/
│   ├── engine.py          # Motor de análise
│   └── dto.py             # Data Transfer Objects
├── plugins/               # Plugins especializados
│   ├── python/
│   ├── javascript/
│   ├── go/
│   ├── rust/
│   ├── kotlin/
│   ├── swift/
│   ├── frontend/          # Vue, Angular, Svelte
│   └── infra/             # Bash, YAML, Docker, Terraform
├── detectors/
│   └── language_detector.py
└── ai_layer/
    └── groq_adapter.py    # Integração com IA
```

### Padrões Utilizados
- **Strategy Pattern** (seleção de plugins)
- **Adapter Pattern** (integração com IA)
- **DTO Pattern** (contratos padronizados)

---

## 🔌 Criando Plugins Personalizados

```python
from review_engine.plugins.base_plugin import BasePlugin
from review_engine.core.dto import ReviewResult, Issue, SeverityLevel

class MeuPlugin(BasePlugin):
    def get_supported_languages(self):
        return ["minha_linguagem"]
    
    def get_rules(self):
        return {
            "RULE_001": {
                "name": "Nome da Regra",
                "severity": "high",
                "category": "performance"
            }
        }
    
    def analyze(self, code: str, language: str) -> ReviewResult:
        # Sua lógica de análise
        issues = []
        # ... detectar problemas
        return ReviewResult(language=language, issues=issues)
```

---

## 📊 Métricas de Eco-Impact

O sistema calcula:
- **Complexidade Ciclomática** reduzida
- **Uso de Memória** otimizado
- **Speedup Estimado** (2x, 3x, etc.)
- **Economia de Energia** (% CPU reduzido)

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

---

## 🐛 Troubleshooting

### Erro: "Groq API não configurada"
```bash
# Certifique-se de definir a variável de ambiente
echo $GROQ_API_KEY  # Linux/Mac
echo %GROQ_API_KEY%  # Windows
```

### Erro: "ModuleNotFoundError"
```bash
pip install -r requirements.txt --upgrade
```

### Performance lenta
- Desabilite a análise via IA (checkbox na interface)
- Use análise estática apenas (mais rápida)

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

## 🙏 Agradecimentos

- [Groq](https://groq.com/) pela API de IA rápida e eficiente
- [CodeMirror](https://codemirror.net/) pelo editor de código
- Comunidade open-source de análise estática de código

---

## 📧 Contato

**Energisa Inovações**  
Desenvolvido com 💚 para Green IT e Performance Optimization

---

⭐ **Se este projeto foi útil, considere dar uma estrela no GitHub!**
