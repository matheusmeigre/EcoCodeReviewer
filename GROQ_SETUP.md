# 🚀 CONFIGURAÇÃO RÁPIDA - Groq API (100% GRATUITO!)

## ✅ Por que Groq?

- ✅ **100% GRATUITO** (sem cartão de crédito)
- ✅ **Ultra-rápido** (mais rápido que OpenAI)
- ✅ **Modelos poderosos**: LLaMA 3.3 70B, Mixtral 8x7B
- ✅ **Sem limites abusivos** (rate limits generosos)

---

## 📋 PASSO A PASSO (3 minutos)

### 1️⃣ Obter API Key (GRÁTIS)

1. Acesse: **https://console.groq.com/keys**
2. Faça login com Google/GitHub (rápido)
3. Clique "Create API Key"
4. Copie a chave (começa com `gsk_...`)

### 2️⃣ Configurar .env

Se o arquivo `.env` não existe, copie o exemplo:
```powershell
Copy-Item .env.example .env
```

Abra o arquivo `.env` e cole sua chave:
```bash
GROQ_API_KEY=gsk_SUA_CHAVE_AQUI
GROQ_MODEL=llama-3.3-70b-versatile
GROQ_TEMPERATURE=0.3
GROQ_MAX_TOKENS=2000
GROQ_TIMEOUT=30
```

### 3️⃣ Iniciar Servidor

```powershell
python app.py
```

Você verá:
```
🚀 Eco-Code Reviewer v4.0 - SEMANTIC ANALYSIS ENGINE
======================================================================
📊 URL: http://localhost:5000
🤖 Motor: Groq llama-3.3-70b-versatile (100% GRATUITO!)
🔑 API Status: ✅ Configured  # <- Deve aparecer ✅
🎯 Idiomas: python, java, csharp, delphi, javascript, typescript, react, sql, nosql
🌱 Foco: Green IT + Performance Optimization
```

---

## 🧪 TESTAR AGORA

1. Abra: **http://localhost:5000**
2. Cole este código Python:
```python
lista = [10, 20, 30, 40, 50]

soma = 0
for i in range(0, len(lista)):
    soma += lista[i]

print(soma)
```
3. Clique **"Analisar Eficiência"**
4. Aguarde 2-3 segundos

**Resultado Esperado:**
- ✅ IA detecta loop manual ineficiente
- ✅ Sugere: `soma = sum(lista)`
- ✅ Explica: Cita PEP 20 e performance 3.5x
- ✅ Métricas: Speedup, CPU reduction, Energy savings

---

## 🔥 MODELOS DISPONÍVEIS (TODOS GRÁTIS)

### Recomendado: `llama-3.3-70b-versatile`
- ✅ **Melhor custo-benefício**
- ✅ Balanceado (rápido + preciso)
- ✅ Contexto: 128K tokens
- ✅ Velocidade: Ultra-rápido

### Alternativas:
```bash
# Mais rápido
GROQ_MODEL=llama-3.1-70b-versatile

# Contexto longo (32K tokens)
GROQ_MODEL=mixtral-8x7b-32768

# Leve e rápido
GROQ_MODEL=gemma2-9b-it
```

---

## 💰 LIMITES GRATUITOS

### Groq Free Tier:
- **Requests/minuto**: 30
- **Tokens/minuto**: 14.400
- **Requests/dia**: 14.400

**Para este app:**
- Análise média: ~1.000 tokens
- **Você pode fazer ~14 análises/minuto GRÁTIS!**

---

## ❓ TROUBLESHOOTING

### ❌ "API Status: NOT CONFIGURED"
**Solução:**
1. Verifique se `.env` existe
2. Confirme que `GROQ_API_KEY` começa com `gsk_`
3. Reinicie o servidor (`python app.py`)

### ❌ "Rate limit exceeded"
**Solução:**
Aguarde 1 minuto. Limite: 30 requests/min (generoso!)

### ❌ "Invalid API key"
**Solução:**
1. Gere nova chave em: https://console.groq.com/keys
2. Copie novamente (sem espaços)
3. Salve `.env` e reinicie

---

## 🆚 COMPARAÇÃO: OpenAI vs Groq

| Aspecto | OpenAI | Groq |
|---------|--------|------|
| **Custo** | 💰 $0.15/1M tokens | ✅ **GRÁTIS** |
| **Velocidade** | 🟡 Médio | ✅ **Ultra-rápido** |
| **Limites** | 🔴 Baixos no free | ✅ **Generosos** |
| **Cartão** | ❌ Obrigatório | ✅ **Não precisa** |
| **Qualidade** | 🟢 Excelente | 🟢 **Excelente** |

---

## 📊 EXEMPLO DE RESPOSTA

Quando você enviar código ineficiente, Groq retorna:

```json
{
  "hasIssues": true,
  "qualityScore": 65,
  "optimizedCode": "soma = sum(lista)",
  "issues": [
    {
      "type": "complexity",
      "severity": "high",
      "title": "Loop manual desnecessário",
      "description": "Conforme PEP 20: 'Simple is better than complex'. O built-in sum() é 3x mais rápido.",
      "impact": "Economia de ~35% CPU cycles"
    }
  ],
  "metrics": {
    "complexityReduction": "Média",
    "memoryImpact": "-20% allocations",
    "estimatedSpeedup": "3.5x faster",
    "energySavings": "-35% CPU cycles"
  }
}
```

---

## 🎓 DICAS PROFISSIONAIS

### 1. Ajustar Temperature
```bash
# Mais determinístico (análise consistente)
GROQ_TEMPERATURE=0.1

# Mais criativo (análise variada)
GROQ_TEMPERATURE=0.5
```

### 2. Aumentar Max Tokens (para explicações longas)
```bash
GROQ_MAX_TOKENS=3000
```

### 3. Testar diferentes modelos
Cada modelo tem características únicas. Teste e escolha o melhor para seu caso!

---

## 🚀 PRONTO!

Agora você tem um **Analisador de Código com IA 100% GRATUITO** que:
- ✅ Entende contexto semântico
- ✅ Baseia-se em docs oficiais
- ✅ Detecta problemas sutis
- ✅ Explica com profundidade técnica
- ✅ Sugere otimizações reais

**🎉 Aproveite a análise profissional sem pagar nada!**
