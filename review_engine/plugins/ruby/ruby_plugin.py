"""
Ruby Plugin - FASE 3
Análise específica para Ruby
"""
from typing import List, Dict
import re

from review_engine.plugins.base_plugin import BasePlugin
from review_engine.core.dto import ReviewResult, Issue, Metrics, SeverityLevel


class RubyPlugin(BasePlugin):
    """Plugin para análise de código Ruby"""
    
    def get_supported_languages(self) -> List[str]:
        return ["ruby"]
    
    def get_rules(self) -> Dict[str, dict]:
        return {
            "RUBY_001": {
                "name": "N+1 Query Problem",
                "description": "Loop que faz queries individuais",
                "severity": "high",
                "category": "performance",
                "impact": "high"
            },
            "RUBY_002": {
                "name": "Mass assignment vulnerável",
                "description": "Uso de params sem whitelist",
                "severity": "critical",
                "category": "security",
                "impact": "critical"
            },
            "RUBY_003": {
                "name": "Rescue genérico",
                "description": "Rescue sem especificar exceção",
                "severity": "medium",
                "category": "error-handling",
                "impact": "medium"
            }
        }
    
    def analyze(self, code: str, language: str) -> ReviewResult:
        issues = []
        
        # RUBY_001: N+1 Query
        if re.search(r'\.each\s+do.*?\.find|\.where', code, re.DOTALL):
            issues.append(Issue(
                title="Potencial N+1 Query detectado",
                description=self.get_rules()["RUBY_001"]["description"],
                severity=SeverityLevel.HIGH,
                category="performance",
                impact="Múltiplas queries desnecessárias",
                recommendation="Use .includes() ou .eager_load()"
            ))
        
        # RUBY_002: Mass assignment
        if re.search(r'create\(params\[|\bnew\(params\[', code):
            issues.append(Issue(
                title="Mass assignment sem proteção",
                description=self.get_rules()["RUBY_002"]["description"],
                severity=SeverityLevel.CRITICAL,
                category="security",
                impact="Atributos não autorizados podem ser modificados",
                recommendation="Use strong parameters ou attr_accessible"
            ))
        
        # RUBY_003: Rescue genérico
        if re.search(r'\brescue\s*$', code, re.MULTILINE):
            issues.append(Issue(
                title="Rescue sem especificar exceção",
                description=self.get_rules()["RUBY_003"]["description"],
                severity=SeverityLevel.MEDIUM,
                category="error-handling",
                impact="Pode capturar exceções inesperadas",
                recommendation="Especificar exceção: rescue StandardError"
            ))
        
        quality_score = self.calculate_quality_score(issues)
        
        metrics = Metrics(
            readability=max(0, 85 - len(issues) * 5),
            performance="medium" if any(i.category == "performance" for i in issues) else "high",
            eco_impact="low" if len(issues) <= 1 else "medium",
            maintainability=max(0, 88 - len(issues) * 10)
        )
        
        return ReviewResult(
            language=language,
            quality_score=quality_score,
            issues=issues,
            metrics=metrics,
            recommendations=[f"Corrigir {len(issues)} problema(s) de Ruby"] if issues else []
        )
