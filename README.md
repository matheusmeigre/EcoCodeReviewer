# 🌱 Eco-Code Reviewer v2.0

**Otimização de Código Multi-Linguagem para Data Centers Sustentáveis**

Uma ferramenta corporativa avançada desenvolvida para o Grupo Energisa que analisa código em **múltiplas linguagens** e identifica oportunidades de otimização visando redução de consumo energético, eficiência algorítmica e melhor performance em Data Centers.

---

## ✨ Novidades da Versão 2.0

### 🔥 Suporte Multi-Linguagem
- **Python** - Loops aninhados, list comprehensions, generators
- **C#** - LINQ ineficiente, StringBuilder, estruturas de dados
- **Java** - StringBuilder, coleções adequadas, complexidade
- **Delphi** - TStringBuilder, TDictionary, busca ordenada
- **JavaScript** - ES6 otimizações, Map/Set, array methods
- **TypeScript** - Tipagem forte para otimizações
- **React/ReactJS** - useCallback, useMemo, reconciliação
- **SQL** - SELECT *, JOINs, índices, subqueries
- **NoSQL/MongoDB** - Projeções, índices, agregações

### 🎨 Novo Design: Split View para Produtividade Máxima
- **Layout Lado-a-Lado**: Código original à esquerda, otimizado à direita
- **Sem Scroll Desnecessário**: Veja as sugestões imediatamente
- **Design Minimalista**: Foco na legibilidade do código
- **Clean Corporate**: Paleta reduzida (Branco, Cinza, Laranja para ações, Verde para sucesso)

### 📊 Resumo Didático de Otimizações
- Explicação clara do que foi mudado
- Por que isso economiza energia/processamento
- Benefícios estimados em milissegundos e carga de CPU

---

## 🎯 Objetivo

Alinhar código limpo com metas de descarbonização e eficiência energética, fornecendo:
- **Score de Sustentabilidade** (0-100)
- **Análise de Complexidade** (Big O Notation)
- **Estimativa de Economia Energética**
- **Sugestões de Refatoração Específicas por Linguagem**
- **Resumo Didático das Otimizações**

---

## 🚀 Tecnologias

### Backend
- **Python 3.8+**
- **Flask 3.0.0** - Framework web
- **Flask-CORS 4.0.0** - Gerenciamento de CORS
- **Analisador Multi-Linguagem** - Heurísticas específicas por linguagem

### Frontend
- **HTML5** - Estrutura semântica split view
- **CSS3** - Grid layout, design minimalista
- **Bootstrap 5** (via CDN) - Componentes base
- **JavaScript ES6+** - Fetch API, async/await
- **Font Awesome** - Ícones
- **Fira Code** - Fonte monospace para código

---

## � Instalação e Configuração

### 1. Clone ou baixe o projeto

```powershell
# Navegue até o diretório do projeto
cd "c:\Users\Matheus Meigre\Documents\Ferramentas e Estudos\Energisa Inovacoes\EcoCoder Review"
```

### 2. Crie um ambiente virtual (recomendado)

```powershell
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual no Windows
.\venv\Scripts\Activate.ps1
```

**Nota:** Se encontrar erro de execução de scripts, execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 3. Instale as dependências

```powershell
pip install -r requirements.txt
```

### 4. Execute a aplicação

```powershell
python app.py
```

Você verá a mensagem:
```
🌱 Eco-Code Reviewer v2.0 iniciado!
📊 Acesse: http://localhost:5000
🔋 Suporte multi-linguagem: Python, C#, Java, Delphi, JS, TS, React, SQL
🚀 Novo layout Split View para produtividade máxima!
```

### 5. Acesse no navegador

Abra seu navegador e acesse:
```
http://localhost:5000
```

---

## 📖 Como Usar

1. **Selecione a Linguagem**: Use o dropdown para indicar a linguagem do código
2. **Cole o Código**: No painel esquerdo, insira o código que deseja analisar
3. **Clique em "Analisar Eficiência"**: Aguarde a análise (ou pressione Ctrl+Enter)
4. **Visualize os Resultados**: No painel direito você verá:
   - Score de sustentabilidade
   - Complexidade atual vs otimizada
   - Economia estimada de processamento
   - Resumo didático da otimização
   - Problemas detectados
   - Código refatorado (pronto para copiar)

### Atalhos
- **Ctrl + Enter**: Executar análise
- **Botão Copiar**: Copia o código otimizado para clipboard

---

## 💡 Exemplos de Código para Teste

### Python - Loops Aninhados
```python
resultado = []
for i in range(len(dados)):
    for j in range(len(dados)):
        if dados[i] == dados[j]:
            resultado.append(dados[i])
```

### C# - LINQ Ineficiente
```csharp
var users = GetUsers().ToList();
var count = users.Where(u => u.Active).Count();
```

### SQL - SELECT * e Subquery
```sql
SELECT * FROM users
WHERE user_id IN (SELECT user_id FROM orders WHERE status = 'pending')
```

### React - Re-renders Desnecessários
```jsx
function Component() {
  const [data, setData] = useState([]);
  return (
    <div>
      {data.map((item, index) => (
        <Item key={index} onClick={() => handleClick(item)} />
      ))}
    </div>
  );
}
```

### JavaScript - Array Methods Encadeados
```javascript
const result = data
  .map(x => x * 2)
  .filter(x => x > 10)
  .map(x => x + 1);
```

---

## 🔍 Padrões Detectados por Linguagem

### Python
- ✅ Loops aninhados (O(n²))
- ✅ List comprehension vs append em loop
- ✅ Concatenação de strings com +=
- ✅ Cálculos repetidos (len() em loop)
- ✅ Generators vs listas completas

### C#
- ✅ ToList() desnecessário antes de Count()
- ✅ String concatenation vs StringBuilder
- ✅ Loops aninhados
- ✅ Estruturas de dados inadequadas

### Java
- ✅ String concatenation em loop
- ✅ ArrayList vs LinkedList para inserções
- ✅ Loops aninhados
- ✅ HashMap/HashSet para buscas

### Delphi
- ✅ String concatenation vs TStringBuilder
- ✅ TStringList sem Sorted
- ✅ Loops aninhados
- ✅ TDictionary para lookups

### JavaScript/TypeScript
- ✅ Loops aninhados
- ✅ Array methods encadeados (múltiplas iterações)
- ✅ var vs const/let
- ✅ Tipagem any (TypeScript)

### React
- ✅ Funções inline sem useCallback
- ✅ Cálculos complexos sem useMemo
- ✅ Index como key em map
- ✅ Re-renders desnecessários

### SQL
- ✅ SELECT * (transferência desnecessária)
- ✅ JOIN sem WHERE (full table scan)
- ✅ Subquery em IN (use JOIN/EXISTS)
- ✅ LIKE iniciando com % (impede índices)

### NoSQL (MongoDB)
- ✅ Query sem projeção
- ✅ Queries sem índices
- ✅ $lookup excessivo (desnormalização)

---

## 🔮 Integração Futura com LLM/OpenAI

O código está preparado para integração com APIs de IA. No arquivo `app.py`, localize o comentário:

```python
# NOTA PARA INTEGRAÇÃO FUTURA:
# Aqui você pode substituir a lógica heurística pela chamada à API OpenAI/LLM
```

### Exemplo de Integração OpenAI:

```python
import openai

openai.api_key = 'sua-chave-api'

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {
            "role": "system", 
            "content": "Você é um especialista em otimização de código Python com foco em eficiência energética..."
        },
        {
            "role": "user", 
            "content": f"Analise este código e forneça score, complexidade e sugestões: {code}"
        }
    ]
)

# Extrair dados do response
```

---

## 📁 Estrutura do Projeto

```
EcoCoder Review/
│
├── app.py                 # Backend Flask com lógica heurística
├── requirements.txt       # Dependências Python
├── README.md             # Este arquivo
│
├── templates/
│   └── index.html        # Interface principal
│
└── static/
    ├── css/
    │   └── style.css     # Estilos customizados (paleta Energisa)
    └── js/
        └── script.js     # Lógica frontend (Fetch API)
```

---

## 🛠️ Solução de Problemas

### Erro: "Não foi possível conectar ao servidor"
- Verifique se o backend está rodando (`python app.py`)
- Confirme que a porta 5000 não está em uso

### Erro: "ModuleNotFoundError: No module named 'flask'"
- Ative o ambiente virtual
- Execute `pip install -r requirements.txt`

### Erro de Política de Execução (PowerShell)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Layout não aparece corretamente
- Limpe o cache do navegador (Ctrl+F5)
- Verifique se os arquivos CSS/JS estão sendo carregados (F12 > Network)

---

## 🎨 Design v2.0: Clean Corporate

### Princípios de UX
- **Split View**: Código original e otimizado lado a lado (inspirado em diff viewers)
- **Minimalismo**: Paleta reduzida, foco no conteúdo
- **Sem Scroll Desnecessário**: Informações críticas sempre visíveis
- **Produtividade Máxima**: Menos cliques, mais resultados

### Paleta de Cores
- **Off-White** (`#F8F9FA`) - Background principal
- **Cinza Escuro** (`#2C3E50`) - Texto e headers
- **Laranja Energisa** (`#FF6B00`) - Ações primárias
- **Verde** (`#28A745`) - Validações, scores positivos
- **Code Background** (`#282C34`) - Fundo do editor

---

## 📊 Benefícios da Versão 2.0

### Para Desenvolvedores
- ✅ **Análise em 9+ linguagens** (vs 1 na v1.0)
- ✅ **Split view side-by-side** (sem scroll)
- ✅ **Resumo didático** das otimizações
- ✅ **Seletor de linguagem** intuitivo
- ✅ **Design focado em produtividade**

### Para Gestores de TI
- 📊 **Métricas quantificáveis** (ms economizados)
- 🔋 **Impacto em redução de CPU** (Baixa/Média/Alta)
- 💰 **ROI estimado** em performance
- ♻️ **Alinhamento com ESG** e sustentabilidade

---

## 📊 Métricas de Impacto

Para cada análise, a ferramenta v2.0 estima:
- **Economia de processamento** (em milissegundos por execução)
- **Redução de carga de CPU** (Baixa/Média/Alta)
- **Complexidade algorítmica** (Big O: antes e depois)
- **Resumo explicativo** (o que mudou e por quê)

Essas métricas auxiliam na tomada de decisão para priorizar refatorações com maior impacto energético em operações de larga escala.

---

## 🤝 Roadmap Futuro

Sugestões de melhorias para v3.0:

1. ✨ Integração com OpenAI GPT-4 para análises contextuais profundas
2. 📊 Dashboard com histórico de análises e métricas agregadas
3. 🔄 Integração com CI/CD para análise automática em Pull Requests
4. ⚡ Cálculo real de consumo energético (kWh) baseado em perfil de hardware
5. 🌐 Suporte a mais linguagens (Go, Rust, Kotlin, Swift)
6. 👥 Multi-tenancy e autenticação para times corporativos
7. 📱 Progressive Web App (PWA) para uso offline

---

## 📄 Licença

Desenvolvido para o **Grupo Energisa** - Inovação & Tecnologia  
© 2025 - Todos os direitos reservados

---

## 👨‍💻 Changelog

### v2.0 (Dezembro 2025)
- ✨ **Suporte multi-linguagem** (Python, C#, Java, Delphi, JS, TS, React, SQL, NoSQL)
- 🎨 **Novo layout Split View** para produtividade máxima
- 📝 **Resumo didático** das otimizações
- 🎯 **Design minimalista** Clean Corporate
- 🚀 **Análises específicas** por linguagem

### v1.0 (Dezembro 2025)
- Lançamento inicial com suporte Python
- Análise heurística básica
- Interface vertical tradicional

---

## 🌍 Impacto Ambiental

> "Código eficiente não é apenas mais rápido - é mais sustentável."

Cada otimização de código contribui para:
- ⚡ **Menor consumo energético** dos Data Centers
- 🌡️ **Redução de emissões de CO₂**
- 💰 **Economia em infraestrutura** e refrigeração
- ♻️ **Sustentabilidade digital** e alinhamento com metas ESG

---

**Desenvolvido com 💚 para um futuro mais sustentável**  
*Eco-Code Reviewer v2.0 - Onde Performance encontra Sustentabilidade*
