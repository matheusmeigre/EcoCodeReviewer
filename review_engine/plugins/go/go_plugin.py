"""
Go Plugin - FASE 3
Análise específica para linguagem Go
"""
from typing import List, Dict
import re

from review_engine.plugins.base_plugin import BasePlugin
from review_engine.core.dto import ReviewResult, Issue, Metrics, SeverityLevel


class GoPlugin(BasePlugin):
    """Plugin para análise de código Go"""
    
    def get_supported_languages(self) -> List[str]:
        return ["go"]
    
    def get_rules(self) -> Dict[str, dict]:
        return {
            "GO_001": {
                "name": "Error sem verificação",
                "description": "Retorno de erro não está sendo verificado",
                "severity": "high",
                "category": "error-handling",
                "impact": "high"
            },
            "GO_002": {
                "name": "Goroutine leak potencial",
                "description": "Goroutine sem mecanismo de cancelamento",
                "severity": "medium",
                "category": "concurrency",
                "impact": "medium"
            },
            "GO_003": {
                "name": "Defer em loop",
                "description": "Uso de defer dentro de loop pode causar memory leak",
                "severity": "high",
                "category": "memory",
                "impact": "high"
            }
        }
    
    def analyze(self, code: str, language: str) -> ReviewResult:
        issues = []
        
        # GO_001: Error não verificado
        if re.search(r'(?<!if\s)(?<!,\s)err\s*:?=\s*\w+\(.*?\)\s*\n', code):
            issues.append(Issue(
                title="Error sem verificação detectado",
                description=self.get_rules()["GO_001"]["description"],
                severity=SeverityLevel.HIGH,
                category="error-handling",
                impact="Pode ocultar falhas críticas",
                recommendation="Sempre verificar: if err != nil { return err }"
            ))
        
        # GO_002: Goroutine leak
        if 'go func()' in code and 'context.Context' not in code:
            issues.append(Issue(
                title="Goroutine sem context detectada",
                description=self.get_rules()["GO_002"]["description"],
                severity=SeverityLevel.MEDIUM,
                category="concurrency",
                impact="Pode causar goroutine leak",
                recommendation="Use context.Context para cancelamento"
            ))
        
        # GO_003: Defer em loop
        if re.search(r'for\s+.*?\{[^}]*defer\s+', code, re.DOTALL):
            issues.append(Issue(
                title="Defer dentro de loop",
                description=self.get_rules()["GO_003"]["description"],
                severity=SeverityLevel.HIGH,
                category="memory",
                impact="Memory leak até fim do loop",
                recommendation="Extrair lógica para função separada"
            ))
        
        quality_score = self.calculate_quality_score(issues)
        
        metrics = Metrics(
            readability=max(0, 85 - len(issues) * 5),
            performance="high" if len(issues) == 0 else "medium",
            eco_impact="low" if len(issues) <= 1 else "medium",
            maintainability=max(0, 90 - len(issues) * 10)
        )
        
        return ReviewResult(
            language=language,
            quality_score=quality_score,
            issues=issues,
            metrics=metrics,
            recommendations=[f"Corrigir {len(issues)} problema(s) de Go"] if issues else []
        )
