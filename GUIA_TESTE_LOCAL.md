# 🧪 Guia de Teste Local - Eco-Code Reviewer v4.0

## 📋 PRÉ-REQUISITOS

Antes de testar localmente, configure a variável de ambiente `GROQ_API_KEY`:

### Windows (PowerShell):
```powershell
$env:GROQ_API_KEY = "sua-chave-aqui"
```

### Windows (CMD):
```cmd
set GROQ_API_KEY=sua-chave-aqui
```

### Linux/Mac:
```bash
export GROQ_API_KEY="sua-chave-aqui"
```

---

## 🚀 EXECUTAR LOCALMENTE

### 1. Instalar Dependências (se necessário)
```bash
pip install -r requirements.txt
```

### 2. Iniciar Servidor Flask
```bash
python app.py
```

### 3. Abrir no Navegador
```
http://localhost:5000
```

---

## 📱 TESTES DE RESPONSIVIDADE (DevTools)

### Chrome/Edge DevTools:
1. Pressione `F12` ou `Ctrl+Shift+I`
2. Clique no ícone de dispositivo móvel (Ctrl+Shift+M)
3. Teste os seguintes dispositivos:

#### Desktop (≥ 992px)
- **1920x1080**: Deve mostrar Split View (lado a lado)
- Painel esquerdo: Código
- Painel direito: Resultado

#### Tablet (768px - 991px)
- **iPad (768x1024)**: Deve empilhar verticalmente
- Input no topo
- Output embaixo
- Scroll vertical funcional

#### Smartphone (< 576px)
- **iPhone SE (375x667)**
- **Galaxy S20 (360x800)**
- Verificar:
  - [ ] Pills de linguagem visíveis e tocáveis
  - [ ] Botões com tamanho adequado (min 44x44px)
  - [ ] Sem scroll horizontal
  - [ ] Fonte legível (12px mínimo)
  - [ ] Métricas em coluna única

---

## 🎨 TESTES DE UI/UX

### Seletor de Linguagem (Pills):

#### Teste 1: Seleção Básica
1. Clique em "Python" → Deve ficar laranja (active)
2. Clique em "JavaScript" → Python desativa, JS ativa
3. Clique em "Auto" → Volta para modo automático

#### Teste 2: Dropdown "Mais Linguagens"
1. Clique no botão "..." (ellipsis)
2. Dropdown deve abrir com:
   - TypeScript
   - React/ReactJS
   - SQL
   - NoSQL/MongoDB
   - Delphi
3. Clique em "TypeScript" → Dropdown fecha, linguagem selecionada

#### Teste 3: Visual Feedback
- **Hover**: Pills devem ter efeito hover (cor + elevação)
- **Active**: Pill selecionado deve ter cor laranja
- **Transition**: Animações suaves (0.2s)

---

## 🔍 TESTES DE AUTO-DETECÇÃO

### Código Python (deve detectar):
```python
def calcular_soma(numeros):
    resultado = 0
    for i in range(len(numeros)):
        resultado += numeros[i]
    return resultado

print(calcular_soma([1, 2, 3, 4, 5]))
```

**Esperado:**
- Após ~500ms digitando, feedback aparece: "Detectado: Python"
- Ícone de check verde ao lado

### Código JavaScript (deve detectar):
```javascript
function calcularSoma(numeros) {
    let resultado = 0;
    for (let i = 0; i < numeros.length; i++) {
        resultado += numeros[i];
    }
    return resultado;
}

console.log(calcularSoma([1, 2, 3, 4, 5]));
```

**Esperado:**
- Feedback: "Detectado: JavaScript"

### Código SQL (deve detectar):
```sql
SELECT u.nome, COUNT(p.id) as total_pedidos
FROM usuarios u
INNER JOIN pedidos p ON u.id = p.usuario_id
WHERE p.data > '2025-01-01'
GROUP BY u.nome
HAVING COUNT(p.id) > 5
```

**Esperado:**
- Feedback: "Detectado: SQL"

### Código Ambíguo (não deve detectar):
```
hello world
teste
123
```

**Esperado:**
- Feedback: "Linguagem não identificada"

---

## 🔄 TESTES DE FLUXO COMPLETO

### Fluxo 1: Auto-detecção + Análise
1. **Passo 1**: Cole código Python no textarea
2. **Passo 2**: Aguarde 500ms → Feedback "Detectado: Python" aparece
3. **Passo 3**: Clique "Analisar"
4. **Passo 4**: Botão muda para "Analisando..." com spinner
5. **Passo 5**: Loading state aparece
6. **Passo 6**: Resultado exibido com:
   - Quality Score
   - Métricas (complexidade, memória, speedup, energia)
   - Explicação da IA
   - Código otimizado

### Fluxo 2: Seleção Manual + Análise
1. **Passo 1**: Clique em "JavaScript" (pill laranja)
2. **Passo 2**: Cole código JS
3. **Passo 3**: Clique "Analisar"
4. **Passo 4**: Verificar se análise processa corretamente

### Fluxo 3: Limpar Interface
1. **Passo 1**: Com resultado exibido, clique "Limpar"
2. **Passo 2**: Verificar:
   - [ ] Textarea limpo
   - [ ] Pills resetados para "Auto"
   - [ ] Empty state visível
   - [ ] Score mini oculto
   - [ ] Feedback de detecção limpo

---

## 📊 TESTES DE PERFORMANCE

### Debounce da Auto-detecção:
1. Digite código Python **rapidamente**
2. A detecção deve esperar 500ms após **parar de digitar**
3. Não deve executar a cada tecla pressionada

### Loading States:
1. Clique "Analisar"
2. Loading state deve aparecer **instantaneamente**
3. Botão deve ficar desabilitado
4. Spinner deve girar

### Transições:
- Empty → Loading: Suave (fade)
- Loading → Results: Suave (fade + slide up)

---

## 🐛 TESTES DE EDGE CASES

### Caso 1: Análise sem código
1. Deixe textarea vazio
2. Clique "Analisar"
3. **Esperado**: Toast de alerta "Por favor, insira um código para análise."

### Caso 2: Auto-detecção falha + Análise forçada
1. Selecione "Auto"
2. Cole código ambíguo: `hello world`
3. Clique "Analisar"
4. **Esperado**: Toast "Linguagem não identificada localmente. A IA tentará detectar..."
5. Backend recebe `language: "auto"` e LLM tenta detectar

### Caso 3: Múltiplas análises rápidas
1. Analisar código Python
2. **Imediatamente** clicar "Analisar" novamente
3. **Esperado**: Botão desabilitado durante análise anterior

### Caso 4: Copiar código otimizado
1. Após análise, clique "Copiar" no código otimizado
2. **Esperado**: Toast "Código copiado para a área de transferência!"
3. Cole em editor externo para verificar

---

## 🎯 CHECKLIST DE QUALIDADE FINAL

### Visual:
- [ ] Todas as pills têm ícones corretos (FontAwesome)
- [ ] Cores seguem paleta definida (Laranja: #FF6B00, Verde: #28A745)
- [ ] Espaçamentos consistentes (8px, 16px, 24px)
- [ ] Fonte legível em todos os tamanhos

### Funcional:
- [ ] Auto-detecção funciona para 9 linguagens
- [ ] Pills ativam/desativam corretamente
- [ ] Dropdown abre/fecha sem bugs
- [ ] Análise envia linguagem correta para backend
- [ ] Toast aparece e desaparece automaticamente

### Responsivo:
- [ ] Desktop: Split view perfeita
- [ ] Tablet: Stack view funcional
- [ ] Mobile: Tudo tocável e legível
- [ ] Sem scroll horizontal em nenhum dispositivo
- [ ] Landscape mobile funciona

### Acessibilidade:
- [ ] Botões têm atributos `title` para tooltip
- [ ] Contraste de cores adequado (WCAG AA)
- [ ] Elementos focáveis com teclado (Tab)
- [ ] Labels descritivos para screen readers

---

## 🚨 PROBLEMAS COMUNS E SOLUÇÕES

### Problema: "Dropdown não abre"
**Solução**: Verificar se `position: relative` está em `.language-selector-wrapper`

### Problema: "Auto-detecção não funciona"
**Solução**: 
1. Verificar se está em modo "Auto" (pill laranja)
2. Digitar mais de 30 caracteres
3. Aguardar 500ms após parar de digitar

### Problema: "Layout não empilha no mobile"
**Solução**: Abrir DevTools e testar em width < 992px

### Problema: "Análise retorna erro 500"
**Solução**: Configurar `GROQ_API_KEY` nas variáveis de ambiente

---

## 📸 CAPTURAS ESPERADAS

### Desktop (Split View):
```
+----------------------------------+----------------------------------+
|  CÓDIGO ORIGINAL                 |  RESULTADO / OTIMIZAÇÃO          |
|  [Textarea grande]               |  [Métricas + Explicação + Code]  |
|                                  |                                  |
|                                  |                                  |
+----------------------------------+----------------------------------+
```

### Mobile (Stack View):
```
+----------------------------------+
|  CÓDIGO ORIGINAL                 |
|  [Textarea]                      |
|                                  |
+----------------------------------+
|  RESULTADO / OTIMIZAÇÃO          |
|  [Scroll vertical]               |
|  - Métricas                      |
|  - Explicação                    |
|  - Código otimizado              |
+----------------------------------+
```

---

## ✅ APROVAÇÃO FINAL

Após todos os testes, a aplicação deve:
- ✅ Funcionar perfeitamente em desktop
- ✅ Funcionar perfeitamente em tablets
- ✅ Funcionar perfeitamente em smartphones
- ✅ Auto-detectar 9 linguagens corretamente
- ✅ Ter UI moderna e profissional
- ✅ Sem bugs ou comportamentos estranhos

**Data do Teste**: __________  
**Testado por**: __________  
**Status**: ⬜ Aprovado | ⬜ Necessita ajustes
