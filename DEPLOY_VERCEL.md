# 🚀 Deploy do Eco-Code Reviewer na Vercel

## ✅ Arquivos Criados para Deploy

- **`vercel.json`**: Configuração de build e rotas
- **`api/index.py`**: Backend adaptado para serverless functions
- **`static/js/script.js`**: Frontend com URL relativa (funciona local e na Vercel)

---

## 📋 Passo a Passo

### 1️⃣ Configurar Variáveis de Ambiente na Vercel

No Dashboard da Vercel:

1. Acesse: **Settings** → **Environment Variables**
2. Adicione as seguintes variáveis:

| **Nome**            | **Valor**                      |
|---------------------|--------------------------------|
| `GROQ_API_KEY`      | `gsk_***SuaChaveAqui***`       |
| `GROQ_MODEL`        | `llama-3.3-70b-versatile`      |
| `GROQ_TEMPERATURE`  | `0.3`                          |
| `GROQ_MAX_TOKENS`   | `2000`                         |
| `GROQ_TIMEOUT`      | `30`                           |

3. Certifique-se de aplicar para **todos os ambientes** (Production, Preview, Development)

---

### 2️⃣ Fazer Deploy

#### Opção A: Via Git (Recomendado)

```bash
# Commitar as mudanças
git add .
git commit -m "Adaptado para Vercel Serverless"
git push origin master

# Vercel irá detectar automaticamente e fazer deploy
```

#### Opção B: Via CLI da Vercel

```bash
# Instalar CLI (se ainda não tiver)
npm install -g vercel

# Fazer deploy
vercel

# Deploy em produção
vercel --prod
```

---

### 3️⃣ Verificar Status

Após o deploy, teste os endpoints:

- **Interface**: `https://seu-projeto.vercel.app/`
- **Health Check**: `https://seu-projeto.vercel.app/health`
- **Config**: `https://seu-projeto.vercel.app/config`

---

## 🔧 Estrutura de Diretórios (Vercel)

```
EcoCoder Review/
├── api/
│   └── index.py          ← Backend serverless (Vercel Python Runtime)
├── static/
│   ├── css/
│   └── js/
│       └── script.js     ← Frontend (API_URL relativa)
├── templates/
│   └── index.html
├── vercel.json           ← Configuração de build/rotas
├── requirements.txt      ← Dependências Python
└── .env                  ← NÃO VAI PARA VERCEL (use Environment Variables)
```

---

## ⚠️ Problemas Comuns e Soluções

### ❌ Erro: "Failed to fetch"

**Causa**: Frontend tentando acessar `localhost:5000` (não funciona na Vercel)

**Solução**: Já corrigido! Agora usa `window.location.origin`

---

### ❌ Erro: "Groq API não configurada"

**Causa**: Variáveis de ambiente não configuradas na Vercel

**Solução**:
1. Dashboard Vercel → Settings → Environment Variables
2. Adicione `GROQ_API_KEY` com sua chave
3. Redeploy o projeto

---

### ❌ Erro: "Module not found"

**Causa**: Dependência faltando no `requirements.txt`

**Solução**: Verifique se todas as dependências estão listadas:
```
Flask==3.0.0
Flask-CORS==4.0.0
groq==0.11.0
markdown2==2.4.10
```

---

## 📊 Diferenças: Local vs Vercel

| **Aspecto**          | **Local (app.py)**        | **Vercel (api/index.py)** |
|----------------------|---------------------------|---------------------------|
| **Execução**         | `python app.py`           | Serverless function       |
| **Ambiente**         | `.env` file               | Environment Variables     |
| **URL**              | `localhost:5000`          | `seu-projeto.vercel.app`  |
| **Templates**        | `./templates/`            | `../templates/`           |
| **Static Files**     | `./static/`               | `../static/`              |
| **CORS**             | Configurado manualmente   | Vercel adiciona headers   |

---

## 🧪 Testar Localmente (Simulando Vercel)

```bash
# Instalar Vercel CLI
npm install -g vercel

# Rodar localmente (simula serverless)
vercel dev

# Acesse: http://localhost:3000
```

---

## 🎯 Checklist Final

- [x] `vercel.json` criado
- [x] `api/index.py` criado (paths relativos para templates/static)
- [x] `script.js` atualizado (URL relativa)
- [x] Variáveis de ambiente configuradas na Vercel
- [x] `.gitignore` protegendo `.env`
- [ ] Deploy realizado
- [ ] Teste na URL de produção

---

## 🔗 Links Úteis

- **Vercel Dashboard**: https://vercel.com/dashboard
- **Groq Console**: https://console.groq.com/keys
- **Vercel Python Docs**: https://vercel.com/docs/functions/runtimes/python
- **Vercel Environment Variables**: https://vercel.com/docs/projects/environment-variables

---

## 📝 Notas

1. **O arquivo `.env` local NÃO será enviado para Vercel** (protegido pelo `.gitignore`)
2. **Use Environment Variables na Vercel** para configurar a API key
3. **Paths relativos** (`../templates`, `../static`) são essenciais no serverless
4. **Flask funciona normalmente** como serverless function
5. **Groq API é 100% GRATUITA** - sem limite de custo!

---

**Pronto para deploy! 🚀**
