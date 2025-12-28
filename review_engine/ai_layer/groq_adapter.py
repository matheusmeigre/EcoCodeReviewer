"""
Groq AI Adapter - AI Layer
Adaptador para integração com API Groq mantendo compatibilidade
"""
import os
import logging
from typing import Optional
import markdown2

from groq import Groq
from review_engine.core.dto import ReviewResult, Issue, Metrics, SeverityLevel, ImpactLevel


logger = logging.getLogger(__name__)


class GroqAdapter:
    """
    Adaptador para API Groq (llama-3.3-70b-versatile)
    Converte análise AI para formato padronizado ReviewResult
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        self.model = "llama-3.3-70b-versatile"
        
        if not self.client:
            logger.warning("Groq API não configurada. Análise AI desabilitada.")
    
    def analyze(self, code: str, language: str) -> ReviewResult:
        """
        Executa análise semântica via AI e converte para ReviewResult
        """
        if not self.client:
            return self._empty_result(language)
        
        try:
            # Prompt otimizado para retornar JSON estruturado
            prompt = self._build_prompt(code, language)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=3000
            )
            
            content = response.choices[0].message.content
            
            # Parser da resposta AI para ReviewResult
            return self._parse_ai_response(content, language)
            
        except Exception as e:
            logger.error(f"Erro na análise Groq: {e}")
            return self._empty_result(language)
    
    def _build_prompt(self, code: str, language: str) -> str:
        """Constrói prompt estruturado para a AI"""
        return f"""Você é um especialista em code review e eco-code (código sustentável).

Analise o código {language.upper()} abaixo e retorne APENAS um JSON válido.

**Código para análise:**
```{language}
{code}
```

**INSTRUÇÕES CRÍTICAS:**
1. Retorne APENAS o JSON, sem texto antes ou depois
2. NO CAMPO "explanation": Use APENAS texto descritivo, SEM blocos de código
3. NO CAMPO "optimizedCode": Coloque o código otimizado (use \\n para quebras de linha)
4. Escape corretamente aspas e caracteres especiais no JSON
5. Máximo 5 issues principais

**Formato EXATO da resposta:**
{{
  "qualityScore": 75,
  "issues": [
    {{
      "title": "Título curto do problema",
      "description": "Descrição detalhada do problema",
      "severity": "high",
      "impact": "Impacto específico no desempenho ou manutenção"
    }}
  ],
  "optimizedCode": "codigo otimizado sem formatação de markdown",
  "explanation": "Análise textual SEM blocos de código. Explique os problemas encontrados e as soluções aplicadas de forma descritiva. Liste os problemas em bullet points. Descreva as vantagens da refatoração.",
  "metrics": {{
    "complexityReduction": "20%",
    "memoryImpact": "-15% memória",
    "estimatedSpeedup": "2x",
    "energySavings": "-10% CPU"
  }}
}}

**PROIBIDO no campo explanation:** Blocos ```code```, trechos de código, exemplos de código.
**PERMITIDO no campo explanation:** Texto descritivo, bullets, títulos markdown (# ## ###).

Retorne APENAS o JSON válido, nada mais.
"""
    
    def _parse_ai_response(self, content: str, language: str) -> ReviewResult:
        """
        Converte resposta AI (texto/JSON) para ReviewResult padronizado
        """
        import json
        import re
        
        try:
            # Extrair JSON da resposta
            json_match = re.search(r'\{[\s\S]*\}', content)
            if not json_match:
                logger.warning("JSON não encontrado na resposta AI")
                return self._fallback_parse(content, language)
            
            json_str = json_match.group()
            
            # LIMPEZA AGRESSIVA DE CARACTERES PROBLEMÁTICOS
            # 1. Remover caracteres de controle exceto \n, \t, \r
            json_str = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', json_str)
            
            # 2. Normalizar quebras de linha dentro de strings JSON
            # Substituir quebras de linha literais por \\n
            def escape_newlines_in_strings(match):
                field_name = match.group(1)
                field_value = match.group(2)
                # Escapar caracteres especiais
                field_value = field_value.replace('\\', '\\\\')  # \\ -> \\\\
                field_value = field_value.replace('\n', '\\n')    # newline -> \\n
                field_value = field_value.replace('\r', '\\r')    # carriage return -> \\r
                field_value = field_value.replace('\t', '\\t')    # tab -> \\t
                field_value = field_value.replace('"', '\\"')    # quote -> \\"
                return f'"{field_name}": "{field_value}"'
            
            # Aplicar escape em campos de texto
            json_str = re.sub(r'"(explanation|optimizedCode|description|impact|title)":\s*"([^"]*(?:"[^"]*)*?)"(?=\s*[,}])', 
                             escape_newlines_in_strings, 
                             json_str, 
                             flags=re.DOTALL)
            
            # Tentar parsear JSON
            data = None
            try:
                data = json.loads(json_str)
            except json.JSONDecodeError as je:
                logger.error(f"Erro ao parsear JSON: {je}")
                # Última tentativa: extração manual de campos
                logger.info("Tentando extração manual de campos...")
                data = self._extract_fields_manually(content)
                if not data:
                    logger.error("Falha na extração manual. Usando fallback.")
                    return self._fallback_parse(content, language)
            
            # Converter issues para objetos Issue
            issues = []
            for issue_data in data.get("issues", []):
                severity_map = {
                    "critical": SeverityLevel.CRITICAL,
                    "high": SeverityLevel.HIGH,
                    "medium": SeverityLevel.MEDIUM,
                    "low": SeverityLevel.LOW
                }
                issues.append(Issue(
                    title=issue_data.get("title", "Problema identificado"),
                    description=issue_data.get("description", ""),
                    severity=severity_map.get(issue_data.get("severity", "medium"), SeverityLevel.MEDIUM),
                    impact=issue_data.get("impact", ""),
                    rule_id="AI_RULE"
                ))
            
            # Converter métricas
            metrics_data = data.get("metrics", {})
            metrics = Metrics(
                readability=80,  # Fixo por enquanto
                performance=ImpactLevel.MEDIO,
                eco_impact=ImpactLevel.MEDIO,
                maintainability=85,
                complexity_reduction=metrics_data.get("complexityReduction", "N/A"),
                memory_impact=metrics_data.get("memoryImpact", "N/A"),
                estimated_speedup=metrics_data.get("estimatedSpeedup", "N/A"),
                energy_savings=metrics_data.get("energySavings", "N/A")
            )
            
            # Obter explanation e remover blocos de código se houver
            explanation = data.get("explanation", "")
            # Remover blocos de código markdown (```...```)
            explanation = re.sub(r'```[\s\S]*?```', '[Bloco de código removido]', explanation)
            # Remover código inline (`...`)
            explanation = re.sub(r'`[^`\n]{50,}`', '[código removido]', explanation)
            
            # Converter explanation para HTML
            explanation_html = markdown2.markdown(
                explanation,
                extras=["fenced-code-blocks", "tables"]
            )
            
            # Obter código otimizado
            optimized_code = data.get("optimizedCode", "")
            # Decodificar \n para quebras de linha reais
            optimized_code = optimized_code.replace('\\n', '\n').replace('\\t', '\t')
            
            return ReviewResult(
                language=language,
                quality_score=data.get("qualityScore", 70),
                issues=issues,
                optimized_code=optimized_code if optimized_code else None,
                explanation=explanation,
                explanation_html=explanation_html,
                metrics=metrics,
                has_issues=len(issues) > 0
            )
            
        except Exception as e:
            logger.error(f"Erro ao parsear resposta AI: {e}")
            return self._fallback_parse(content, language)
    
    def _extract_fields_manually(self, content: str) -> dict:
        """Extrai campos manualmente quando JSON está malformado"""
        import re
        try:
            data = {}
            
            # Extrair qualityScore
            score_match = re.search(r'"qualityScore"\s*:\s*(\d+)', content)
            if score_match:
                data['qualityScore'] = int(score_match.group(1))
            
            # Extrair explanation (campo mais importante)
            explanation_match = re.search(r'"explanation"\s*:\s*"([^"]+(?:\\.[^"]*)*?)"', content, re.DOTALL)
            if explanation_match:
                explanation = explanation_match.group(1)
                # Decodificar escapes
                explanation = explanation.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"')
                data['explanation'] = explanation
            
            # Extrair issues (simplificado)
            issues = []
            issue_pattern = r'\{\s*"title"\s*:\s*"([^"]+)"\s*,\s*"description"\s*:\s*"([^"]+)"\s*,\s*"severity"\s*:\s*"([^"]+)"\s*,\s*"impact"\s*:\s*"([^"]+)"\s*\}'
            for match in re.finditer(issue_pattern, content):
                issues.append({
                    'title': match.group(1),
                    'description': match.group(2),
                    'severity': match.group(3),
                    'impact': match.group(4)
                })
            if issues:
                data['issues'] = issues
            
            return data if data else None
        except Exception as e:
            logger.error(f"Erro na extração manual: {e}")
            return None
    
    def _fallback_parse(self, content: str, language: str) -> ReviewResult:
        """Parser fallback quando JSON não está disponível"""
        import re
        
        # Tentar extrair texto útil do JSON bruto
        explanation_text = ""
        
        # Extrair campo explanation se existir
        explanation_match = re.search(r'"explanation"\s*:\s*"([^"]+(?:\\.[^"]*)*?)"', content, re.DOTALL)
        if explanation_match:
            explanation_text = explanation_match.group(1)
            # Limpar escapes
            explanation_text = explanation_text.replace('\\n', '\n')
            explanation_text = explanation_text.replace('\\t', '\t')
            explanation_text = explanation_text.replace('\\"', '"')
            explanation_text = re.sub(r'\\(.)', r'\1', explanation_text)
        else:
            # Criar explicação genérica
            explanation_text = """# Análise de Código

A IA detectou alguns pontos de melhoria no código analisado.

## Recomendações Gerais:
- Revise variáveis globais e escopo
- Otimize loops e estruturas de repetição
- Considere uso de const/let em vez de var
- Melhore a eficiência de renderização

Para análise detalhada, verifique os issues específicos listados."""
        
        return ReviewResult(
            language=language,
            quality_score=70,
            explanation=explanation_text,
            explanation_html=markdown2.markdown(explanation_text),
            issues=[Issue(
                title="Análise via IA",
                description="A análise detectou pontos de melhoria. Verifique o código manualmente.",
                severity=SeverityLevel.MEDIUM,
                impact="Manutenibilidade e performance",
                rule_id="AI_FALLBACK"
            )],
            has_issues=True
        )
    
    def _empty_result(self, language: str) -> ReviewResult:
        """Resultado vazio quando AI não está disponível"""
        return ReviewResult(
            language=language,
            quality_score=100,
            has_issues=False
        )
