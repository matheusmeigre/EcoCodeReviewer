# 🔧 Troubleshooting: "Failed to fetch" na Vercel

## ✅ Correções Aplicadas

1. **Removido `env` do `vercel.json`** - As variáveis devem ser configuradas no Dashboard
2. **CORS explícito** - Headers configurados para aceitar requisições da mesma origem
3. **Endpoint de teste** - `/api/test` para verificar se o backend responde

---

## 📋 Checklist de Solução

### 1️⃣ Aguardar Redeploy Automático
A Vercel detecta automaticamente mudanças no GitHub e faz redeploy. Aguarde 1-2 minutos.

Verifique em: `https://vercel.com/seu-usuario/eco-code-reviewer/deployments`

---

### 2️⃣ Configurar Variáveis de Ambiente

**CRÍTICO**: Sem isso, a aplicação não funciona!

1. Acesse: `https://vercel.com/seu-usuario/eco-code-reviewer/settings/environment-variables`

2. Adicione **UMA POR UMA**:
   - **Nome**: `GROQ_API_KEY` | **Valor**: `(cole sua chave Groq aqui)`
   - **Nome**: `GROQ_MODEL` | **Valor**: `llama-3.3-70b-versatile`
   - **Nome**: `GROQ_TEMPERATURE` | **Valor**: `0.3`
   - **Nome**: `GROQ_MAX_TOKENS` | **Valor**: `2000`
   - **Nome**: `GROQ_TIMEOUT` | **Valor**: `30`

3. **Marque TODAS as caixas**: Production ✅ Preview ✅ Development ✅

4. Clique em **Save**

---

### 3️⃣ Forçar Redeploy

Após adicionar as variáveis:

1. Vá em: **Deployments**
2. Encontre o último deployment (topo da lista)
3. Clique nos **3 pontinhos** → **Redeploy**
4. Marque: **Use existing Build Cache** ✅
5. Clique em **Redeploy**

---

### 4️⃣ Testar Endpoints

Abra no navegador (substitua pela sua URL):

1. **Teste da API** (deve retornar JSON):
   ```
   https://eco-code-reviewer-f53y5q1c0-matheus-meigres-projects.vercel.app/api/test
   ```
   ✅ Esperado: `{"status":"ok","message":"Backend está funcionando!"}`

2. **Health Check**:
   ```
   https://eco-code-reviewer-f53y5q1c0-matheus-meigres-projects.vercel.app/health
   ```
   ✅ Esperado: `{"status":"healthy","api_status":"configured"}`

3. **Config**:
   ```
   https://eco-code-reviewer-f53y5q1c0-matheus-meigres-projects.vercel.app/config
   ```
   ✅ Esperado: `{"api_configured":true}`

---

### 5️⃣ Testar Interface

Abra: `https://eco-code-reviewer-f53y5q1c0-matheus-meigres-projects.vercel.app/`

1. Cole um código de exemplo:
   ```javascript
   if (flag == true) {
       return true;
   } else {
       return false;
   }
   ```

2. Clique em **Analisar Eficiência**

3. **Deve funcionar sem erro "Failed to fetch"**

---

## ❌ Se AINDA der erro:

### Verificar Logs da Vercel

1. Dashboard → **Deployments** → Clique no último deploy
2. Vá em **Functions** → **api/index.py**
3. Veja se há erros de importação ou inicialização

### Erros Comuns nos Logs:

**Erro**: `ModuleNotFoundError: No module named 'groq'`
**Solução**: Verifique se `groq==0.11.0` está no `requirements.txt`

**Erro**: `GROQ_API_KEY não configurada`
**Solução**: Variáveis de ambiente não foram adicionadas (volte ao passo 2)

**Erro**: `Invalid API key`
**Solução**: Chave Groq inválida. Gere uma nova em: https://console.groq.com/keys

---

## 🔍 Debug Avançado (Console do Navegador)

1. Abra a aplicação na Vercel
2. Pressione **F12** (DevTools)
3. Vá em **Console**
4. Clique em **Analisar Eficiência**
5. Veja o erro exato:

**Se ver**: `POST https://...vercel.app/analyze net::ERR_FAILED`
→ Backend não está respondendo (variáveis de ambiente faltando)

**Se ver**: `CORS policy blocked`
→ Já corrigido no último commit, aguarde redeploy

**Se ver**: `500 Internal Server Error`
→ Verifique logs da Vercel (função com erro)

---

## 📝 Resumo da Solução

| Problema | Causa | Solução |
|----------|-------|---------|
| Failed to fetch | Backend não inicializado | Adicionar variáveis de ambiente na Vercel |
| CORS blocked | Headers faltando | ✅ Corrigido no código |
| 500 error | Groq API key inválida | Verificar chave em https://console.groq.com/keys |
| Página em branco | Rotas incorretas | ✅ Corrigido no vercel.json |

---

## ✅ Status Atual

- [x] `vercel.json` corrigido (sem `env` hardcoded)
- [x] CORS configurado explicitamente
- [x] Endpoint `/api/test` adicionado
- [x] Push para GitHub realizado
- [ ] **Aguardando**: Vercel redeploy (automático, ~1-2 min)
- [ ] **Aguardando**: Você adicionar variáveis de ambiente no Dashboard
- [ ] **Aguardando**: Redeploy manual após adicionar variáveis

---

## 🔗 Links Úteis

- **Seu Projeto**: https://vercel.com/matheus-meigres-projects/eco-code-reviewer
- **Groq Console**: https://console.groq.com/keys
- **Vercel Env Vars**: https://vercel.com/docs/projects/environment-variables
- **Vercel Logs**: Dashboard → Deployments → [Último Deploy] → Runtime Logs

---

**Próximo passo**: Adicionar variáveis de ambiente no Dashboard da Vercel e fazer redeploy!
