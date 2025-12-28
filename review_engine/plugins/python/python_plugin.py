"""
Python Plugin - Exemplo de Implementação
FASE 3: Plugin específico com regras customizadas
"""
from typing import List, Dict
import re

from review_engine.plugins.base_plugin import BasePlugin
from review_engine.core.dto import ReviewResult, Issue, Metrics, SeverityLevel, ImpactLevel


class PythonPlugin(BasePlugin):
    """
    Plugin especializado para análise de código Python
    Implementa regras específicas da linguagem
    """
    
    def __init__(self):
        super().__init__()
        self.name = "PythonPlugin"
        self.version = "2.0.0"
    
    def get_supported_languages(self) -> List[str]:
        return ["python"]
    
    def get_rules(self) -> Dict[str, dict]:
        return {
            "PY_001": {
                "name": "Loop com range(len())",
                "severity": "medium",
                "category": "eco-code",
                "description": "Usar enumerate() ao invés de range(len())"
            },
            "PY_002": {
                "name": "Compreensão de lista ineficiente",
                "severity": "low",
                "category": "performance",
                "description": "List comprehension pode ser otimizada"
            },
            "PY_003": {
                "name": "Concatenação de strings em loop",
                "severity": "high",
                "category": "performance",
                "description": "Usar join() ao invés de concatenação repetida"
            },
            "PY_004": {
                "name": "Importações não utilizadas",
                "severity": "low",
                "category": "maintainability",
                "description": "Imports desnecessários aumentam tempo de carga"
            },
            "PY_005": {
                "name": "Exceções genéricas",
                "severity": "medium",
                "category": "readability",
                "description": "Capturar Exception genérica oculta erros"
            }
        }
    
    def analyze(self, code: str, language: str) -> ReviewResult:
        """Análise específica para Python"""
        issues = []
        
        # PY_001: range(len()) anti-pattern
        if re.search(r'for\s+\w+\s+in\s+range\s*\(\s*len\s*\(', code):
            issues.append(Issue(
                title="Uso de range(len()) detectado",
                description="É mais Pythônico usar enumerate() para iterar com índice",
                severity=SeverityLevel.MEDIUM,
                impact="Reduz legibilidade e pode impactar performance em listas grandes",
                rule_id="PY_001"
            ))
        
        # PY_003: String concatenation in loop
        if re.search(r'for\s+.*:\s*\n\s*\w+\s*\+=\s*["\']', code):
            issues.append(Issue(
                title="Concatenação de strings em loop",
                description="Concatenar strings repetidamente é ineficiente",
                severity=SeverityLevel.HIGH,
                impact="Alto impacto em performance. Usar ''.join() pode ser 10x mais rápido",
                rule_id="PY_003"
            ))
        
        # PY_005: Generic exception handling
        if "except Exception:" in code or "except:" in code:
            issues.append(Issue(
                title="Captura de exceção genérica",
                description="Capturar 'Exception' ou usar 'except:' sem tipo específico",
                severity=SeverityLevel.MEDIUM,
                impact="Dificulta debugging e pode ocultar erros críticos",
                rule_id="PY_005"
            ))
        
        # Calcular métricas
        metrics = self._calculate_python_metrics(code, issues)
        
        # Calcular quality score
        quality_score = self.calculate_quality_score(issues)
        
        return ReviewResult(
            language="python",
            quality_score=quality_score,
            issues=issues,
            metrics=metrics,
            has_issues=len(issues) > 0
        )
    
    def _calculate_python_metrics(self, code: str, issues: List[Issue]) -> Metrics:
        """Calcula métricas específicas para Python"""
        
        # Readability baseado em issues de legibilidade
        readability = 100
        for issue in issues:
            if "readability" in issue.impact.lower():
                readability -= 10
        
        # Performance impact
        perf_issues = [i for i in issues if i.severity == SeverityLevel.HIGH]
        if len(perf_issues) >= 2:
            performance = ImpactLevel.ALTO
        elif len(perf_issues) == 1:
            performance = ImpactLevel.MEDIO
        else:
            performance = ImpactLevel.BAIXO
        
        # Eco-code impact (baseado em regras eco-code)
        eco_issues = [i for i in issues if "PY_001" in str(i.rule_id) or "PY_003" in str(i.rule_id)]
        if len(eco_issues) >= 2:
            eco_impact = ImpactLevel.ALTO
        elif len(eco_issues) == 1:
            eco_impact = ImpactLevel.MEDIO
        else:
            eco_impact = ImpactLevel.BAIXO
        
        return Metrics(
            readability=max(0, readability),
            performance=performance,
            eco_impact=eco_impact,
            maintainability=max(0, 100 - len(issues) * 5),
            complexity_reduction="15%" if len(eco_issues) > 0 else "N/A",
            memory_impact="-10% memória" if "PY_003" in [i.rule_id for i in issues] else "N/A",
            estimated_speedup="2-10x" if len(perf_issues) > 0 else "N/A",
            energy_savings="-15% CPU" if eco_impact != ImpactLevel.BAIXO else "N/A"
        )
