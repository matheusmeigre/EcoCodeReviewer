"""
Eco-Code Reviewer v4.0 - Análise Semântica Real via Groq API
===============================================================

Paradigma: Inteligência Artificial substituindo Regex limitado
Motor: Groq LLaMA 3.3 70B (100% GRATUITO!)
Foco: Green IT, Performance e Clean Code

Autor: Open Source Community
Data: Dezembro 2025
"""

import os
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv
import markdown2

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar Flask
app = Flask(__name__)
CORS(app)

# Configurações
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
GROQ_TEMPERATURE = float(os.getenv('GROQ_TEMPERATURE', '0.3'))
GROQ_MAX_TOKENS = int(os.getenv('GROQ_MAX_TOKENS', '2000'))
GROQ_TIMEOUT = int(os.getenv('GROQ_TIMEOUT', '30'))

# Inicializar cliente Groq (GRATUITO!)
client = None
if GROQ_API_KEY and GROQ_API_KEY != 'gsk_your-api-key-here':
    try:
        client = Groq(api_key=GROQ_API_KEY)
    except Exception as e:
        print(f"⚠️ Erro ao inicializar Groq: {e}")
else:
    print("⚠️ GROQ_API_KEY não configurada! Configure o arquivo .env")
    print("   Obtenha sua chave GRATUITA em: https://console.groq.com/keys")


class AICodeAnalyzer:
    """
    Analisador de código usando IA generativa.
    Remove completamente a dependência de Regex e análise estática.
    """
    
    LANGUAGE_DOCS = {
        'python': 'PEP 8, PEP 20 (Zen of Python), Python 3.12+ best practices',
        'java': 'Oracle Java Style Guide, Java 17+ Streams API, JEP standards',
        'csharp': 'Microsoft C# Coding Conventions, .NET 8+ guidelines, LINQ best practices',
        'delphi': 'Embarcadero Object Pascal Style Guide, Modern Delphi (10.4+) memory management',
        'javascript': 'ECMAScript 2024, Airbnb JavaScript Style Guide, V8 optimization patterns',
        'typescript': 'TypeScript 5.0+ Handbook, strict mode best practices',
        'react': 'React 18.2+ Official Docs, Hooks patterns, Performance optimization (useMemo, useCallback)',
        'sql': 'ANSI SQL standards, PostgreSQL/MySQL optimization, index strategies',
        'nosql': 'MongoDB 7.0+ best practices, aggregation pipeline optimization, indexing strategies'
    }
    
    SYSTEM_PROMPT_TEMPLATE = """Você é um Engenheiro de Software Sênior e Especialista em Green IT com 15+ anos de experiência.

**CONTEXTO DA ANÁLISE:**
- Linguagem: {language}
- Documentação de Referência: {docs}
- Foco Principal: GREEN IT (redução de consumo energético via otimização de código)

**SUA MISSÃO:**
1. Analisar o código fornecido com olhar crítico e profissional
2. Identificar TODOS os problemas de performance, memória e complexidade
3. Basear-se em documentação oficial e benchmarks reais
4. Priorizar otimizações que reduzam ciclos de CPU e alocação de memória

**ÁREAS DE ANÁLISE OBRIGATÓRIAS:**
- Complexidade Ciclomática (CC): Identifique O(n²), O(n³) desnecessários
- Alocação de Memória: String concatenation em loops, objetos temporários
- Padrões Anti-Idiomáticos: Código que vai contra as best practices da linguagem
- Problemas Específicos da Linguagem:
  * Python: Use built-ins (sum, map, filter), evite loops manuais
  * Java: Prefira Streams API, evite ArrayList.add(0,x)
  * C#: Use StringBuilder, LINQ eficiente, cache properties em loops
  * React: Evite re-renders, use useMemo/useCallback, prefira Functional Components
  * SQL: Detecte N+1 queries, falta de índices, SELECT *
  * Delphi: TStringList.Sorted, TDictionary vs loops, gerenciamento de interfaces

**FORMATO DE RESPOSTA (JSON ESTRITO):**
{{
  "hasIssues": true/false,
  "optimizedCode": "// Código otimizado aqui (se aplicável)",
  "issues": [
    {{
      "type": "complexity|memory|idiom|green_it",
      "severity": "critical|high|medium|low",
      "title": "Título conciso do problema",
      "description": "Explicação técnica com referência à documentação",
      "originalCode": "Trecho do código problemático",
      "impact": "Impacto em performance/memória/energia"
    }}
  ],
  "metrics": {{
    "complexityReduction": "Alta|Média|Baixa|Nenhuma",
    "memoryImpact": "Descrição do impacto (ex: -40% allocations)",
    "estimatedSpeedup": "Descrição (ex: O(n²) -> O(n), 3.5x faster)",
    "energySavings": "Estimativa de economia energética (ex: -25% CPU cycles)"
  }},
  "explanation": "Explicação didática em Markdown sobre as otimizações aplicadas, citando documentação oficial e conceitos técnicos. Use code blocks para exemplos.",
  "qualityScore": 0-100
}}

**IMPORTANTE:**
- Se o código estiver perfeito: hasIssues=false, qualityScore=100, explanation="✅ Código excelente!"
- Seja RIGOROSO mas CONSTRUTIVO
- Cite documentação oficial quando aplicável
- Foque em impacto REAL (não teórico)
- Use terminologia técnica precisa
"""

    def __init__(self, code: str, language: str):
        self.code = code
        self.language = language.lower()
        self.docs = self.LANGUAGE_DOCS.get(self.language, 'General programming best practices')
    
    def analyze(self) -> dict:
        """
        Envia o código para análise via Groq API.
        Retorna análise estruturada em JSON.
        """
        
        if not client:
            return self._fallback_response("API Groq não configurada. Configure GROQ_API_KEY no arquivo .env")
        
        try:
            system_prompt = self.SYSTEM_PROMPT_TEMPLATE.format(
                language=self.language.upper(),
                docs=self.docs
            )
            
            user_prompt = f"""Analise este código {self.language.upper()} focando em Green IT:

```{self.language}
{self.code}
```

Retorne APENAS o JSON estruturado (sem texto adicional antes ou depois)."""

            response = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=GROQ_TEMPERATURE,
                max_tokens=GROQ_MAX_TOKENS,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Validar estrutura
            if not all(k in result for k in ['hasIssues', 'metrics', 'explanation', 'qualityScore']):
                return self._fallback_response("Resposta da IA em formato inválido")
            
            # Converter explanation para HTML (Markdown)
            if 'explanation' in result:
                result['explanationHtml'] = markdown2.markdown(
                    result['explanation'],
                    extras=['fenced-code-blocks', 'tables', 'code-friendly']
                )
            
            return {
                'success': True,
                'data': result,
                'model': GROQ_MODEL,
                'tokens': response.usage.total_tokens
            }
            
        except json.JSONDecodeError as e:
            return self._fallback_response(f"Erro ao parsear resposta JSON da IA: {str(e)}")
        except Exception as e:
            return self._fallback_response(f"Erro na análise: {str(e)}")
    
    def _fallback_response(self, error_message: str) -> dict:
        """Resposta de fallback quando a API falha."""
        return {
            'success': False,
            'error': error_message,
            'data': {
                'hasIssues': False,
                'optimizedCode': self.code,
                'issues': [],
                'metrics': {
                    'complexityReduction': 'N/A',
                    'memoryImpact': 'N/A',
                    'estimatedSpeedup': 'N/A',
                    'energySavings': 'N/A'
                },
                'explanation': f"⚠️ **Erro:** {error_message}\n\n**Configure sua API Key:**\n1. Obtenha chave GRATUITA em: https://console.groq.com/keys\n2. Adicione no arquivo `.env`: `GROQ_API_KEY=sua-chave`\n3. Reinicie o servidor",
                'explanationHtml': f'<p>⚠️ <strong>Erro:</strong> {error_message}</p><p><strong>Configure sua API Key:</strong><br>1. Obtenha chave GRATUITA em: <a href="https://console.groq.com/keys" target="_blank">https://console.groq.com/keys</a><br>2. Adicione no arquivo <code>.env</code>: <code>GROQ_API_KEY=sua-chave</code><br>3. Reinicie o servidor</p>',
                'qualityScore': 0
            }
        }


# ========== ROTAS FLASK ==========

@app.route('/')
def index():
    """Renderiza a interface principal."""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze_code():
    """
    Endpoint v4.0: Análise Semântica via Groq API
    
    Request Body:
    {
        "code": "string",
        "language": "python|java|csharp|..."
    }
    
    Response:
    {
        "success": true/false,
        "data": {
            "hasIssues": bool,
            "optimizedCode": "string",
            "issues": [...],
            "metrics": {...},
            "explanation": "markdown",
            "explanationHtml": "html",
            "qualityScore": 0-100
        },
        "model": "gpt-4o-mini",
        "tokens": 1234
    }
    """
    
    try:
        data = request.get_json()
        code = data.get('code', '').strip()
        language = data.get('language', 'python').lower()
        
        if not code:
            return jsonify({
                'success': False,
                'error': 'Código vazio. Por favor, insira um trecho de código para análise.'
            }), 400
        
        if len(code) > 10000:
            return jsonify({
                'success': False,
                'error': 'Código muito longo. Limite: 10.000 caracteres.'
            }), 400
        
        # Análise via IA
        analyzer = AICodeAnalyzer(code, language)
        result = analyzer.analyze()
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Erro no servidor: {str(e)}'
        }), 500


@app.route('/health')
def health():
    """Verifica o status da aplicação e da API."""
    api_status = 'configured' if client else 'not_configured'
    
    return jsonify({
        'status': 'healthy',
        'version': '4.0',
        'service': 'Eco-Code Reviewer',
        'engine': 'Groq API (FREE)',
        'model': GROQ_MODEL,
        'api_status': api_status
    })


@app.route('/config')
def config():
    """Retorna configuração atual (sem expor API key)."""
    return jsonify({
        'model': GROQ_MODEL,
        'temperature': GROQ_TEMPERATURE,
        'max_tokens': GROQ_MAX_TOKENS,
        'api_configured': bool(client),
        'supported_languages': list(AICodeAnalyzer.LANGUAGE_DOCS.keys())
    })


if __name__ == '__main__':
    print("=" * 70)
    print("🚀 Eco-Code Reviewer v4.0 - SEMANTIC ANALYSIS ENGINE")
    print("=" * 70)
    print(f"📊 URL: http://localhost:{os.getenv('FLASK_PORT', 5000)}")
    print(f"🤖 Motor: Groq {GROQ_MODEL} (100% GRATUITO!)")
    print(f"🔑 API Status: {'✅ Configured' if client else '❌ NOT CONFIGURED'}")
    print(f"🎯 Idiomas: {', '.join(AICodeAnalyzer.LANGUAGE_DOCS.keys())}")
    print(f"🌱 Foco: Green IT + Performance Optimization")
    
    if not client:
        print("\n⚠️  ATENÇÃO: Configure GROQ_API_KEY no arquivo .env")
        print("   1. Obtenha chave GRATUITA em: https://console.groq.com/keys")
        print("   2. Copie .env.example para .env")
        print("   3. Adicione sua chave: GROQ_API_KEY=gsk_...")
        print("   4. Reinicie o servidor\n")
    
    print("=" * 70)
    
    app.run(
        debug=os.getenv('FLASK_DEBUG', 'True') == 'True',
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000))
    )
