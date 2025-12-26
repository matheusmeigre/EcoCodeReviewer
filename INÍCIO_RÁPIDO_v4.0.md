# ⚡ INÍCIO RÁPIDO - Eco-Code Reviewer v4.0

## ✅ STATUS ATUAL

✅ **Backend v4.0**: Instalado e rodando em http://localhost:5000  
✅ **Frontend v4.0**: Atualizado com Prism.js e Markdown rendering  
✅ **Dependências**: `openai`, `python-dotenv`, `markdown2` instaladas  
⚠️ **API Key**: **NÃO CONFIGURADA** (esperado - você precisa adicionar)

---

## 🚀 CONFIGURAR API KEY (3 PASSOS)

### 1. Obter Chave da OpenAI
Acesse: **https://platform.openai.com/api-keys**
- Faça login/crie conta
- Clique "Create new secret key"
- Copie a chave (começa com `sk-proj-...`)

### 2. Configurar .env
```bash
# No diretório do projeto
cd "c:\Users\Matheus Meigre\Documents\Ferramentas e Estudos\Energisa Inovacoes\EcoCoder Review"

# Copiar template
Copy-Item .env.example .env

# Editar com Notepad
notepad .env
```

Cole sua chave:
```bash
OPENAI_API_KEY=sk-proj-SUA-CHAVE-AQUI
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.3
OPENAI_MAX_TOKENS=2000
OPENAI_TIMEOUT=30
```

### 3. Reiniciar Servidor
```powershell
# Parar servidor atual (Ctrl+C no terminal ou:)
Stop-Process -Name python -Force

# Iniciar novamente
python app.py
```

Você verá:
```
🔑 API Status: ✅ Configured  # <- Deve mudar de ❌ para ✅
```

---

## 🧪 TESTE IMEDIATO

### Com API Configurada (Análise REAL):
1. Abra http://localhost:5000
2. Cole este código Python:
```python
lista = [10, 20, 30, 40, 50]

soma = 0
for i in range(0, len(lista)):
    soma += lista[i]

print(soma)
```
3. Clique **Analisar Eficiência**
4. **Aguarde 3-5 segundos** (chamada à API)

**Resultado Esperado:**
- ✅ Quality Score < 100 (IA detectou problema!)
- ✅ Issues: "Loop manual desnecessário"
- ✅ Código otimizado: `soma = sum(lista)`
- ✅ Explicação citando **PEP 20** e docs oficiais
- ✅ Métricas: Speedup ~3.5x, Energy Savings ~35%

### Sem API (Modo Fallback):
Se não configurar a API, a aplicação exibe:
```
⚠️ Erro: API OpenAI não configurada. Configure OPENAI_API_KEY no arquivo .env
```

Mas **NÃO quebra** - continua funcionando com mensagem de erro gracioso.

---

## 💡 DIFERENÇA v3.0 → v4.0

| Teste | v3.0 (Regex) | v4.0 (IA) |
|-------|--------------|-----------|
| **Python loop manual** | ✅ Detecta (após correção) | ✅ Detecta + Explica PEP |
| **React Class Component** | ❌ Não entende contexto | ✅ Sugere Hooks |
| **Java Streams API** | ❌ Não sabe Java 17+ | ✅ Recomenda Streams |
| **SQL N+1 queries** | ❌ Regex limitado | ✅ Detecta padrão real |
| **Explicação** | ❌ Genérica | ✅ Cita documentação |

---

## 📊 CUSTO DA API

### Modelo: `gpt-4o-mini` (Recomendado)
- **Preço**: ~$0.15 por 1M tokens input
- **Análise média**: 500 tokens (input + output)
- **Custo por análise**: ~**$0.00008** (0,008 centavos)

**Exemplo de uso:**
- 100 análises/dia = **$0,24/mês**
- 1.000 análises/dia = **$2,40/mês**
- 10.000 análises/dia = **$24/mês**

---

## 🔧 ARQUIVOS MODIFICADOS

### ✅ Criados/Atualizados:
- `app.py` - Backend v4.0 com OpenAI integration
- `requirements.txt` - Adicionadas dependências IA
- `.env.example` - Template de configuração
- `templates/index.html` - Atualizado para v4.0 + Prism.js
- `static/js/script.js` - Novo handler para resposta IA
- `README_v4.0.md` - Documentação completa

### 📦 Backups Criados:
- `app_v3_backup.py` - Backup do backend v3.0 (Regex)
- `static/js/script_v3_backup.js` - Backup do frontend v3.0

---

## 🎯 PRÓXIMOS PASSOS

1. **AGORA**: Configure API key e teste
2. **Depois**: Teste com diferentes linguagens (Java, React, SQL)
3. **Avançado**: Ajuste `OPENAI_TEMPERATURE` para análises mais criativas
4. **Produção**: Adicione rate limiting e cache de respostas

---

## 📞 SUPORTE

**Problema?** Verifique:
- ✅ Arquivo `.env` existe e tem chave válida?
- ✅ Servidor reiniciou após configurar `.env`?
- ✅ Status no terminal mostra `✅ Configured`?
- ✅ Tem créditos na conta OpenAI?

**Logs de Debug:**
- Terminal mostra `⚠️ Erro ao inicializar OpenAI: {erro}` se chave inválida
- Frontend exibe toast de erro se API falhar

---

**🎉 BEM-VINDO À ERA DA ANÁLISE SEMÂNTICA INTELIGENTE!**

Você acabou de migrar de Regex "burro" para **IA que pensa como Engenheiro Sênior**. 🚀
