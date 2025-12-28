"""
Angular Plugin - FASE 3
Análise específica para Angular
"""
from typing import List, Dict
import re

from review_engine.plugins.base_plugin import BasePlugin
from review_engine.core.dto import ReviewResult, Issue, Metrics, SeverityLevel


class AngularPlugin(BasePlugin):
    """Plugin para análise de código Angular"""
    
    def get_supported_languages(self) -> List[str]:
        return ["angular"]
    
    def get_rules(self) -> Dict[str, dict]:
        return {
            "NG_001": {
                "name": "Subscription sem unsubscribe",
                "description": "Observable sem unsubscribe causa memory leak",
                "severity": "high",
                "category": "memory",
                "impact": "high"
            },
            "NG_002": {
                "name": "ChangeDetectionStrategy ausente",
                "description": "Componente sem OnPush strategy",
                "severity": "medium",
                "category": "performance",
                "impact": "medium"
            },
            "NG_003": {
                "name": "Lógica no template",
                "description": "Chamada de função no template",
                "severity": "medium",
                "category": "performance",
                "impact": "medium"
            }
        }
    
    def analyze(self, code: str, language: str) -> ReviewResult:
        issues = []
        
        # NG_001: Subscription sem unsubscribe
        if '.subscribe(' in code and 'unsubscribe' not in code and 'takeUntil' not in code:
            issues.append(Issue(
                title="Subscription sem unsubscribe",
                description=self.get_rules()["NG_001"]["description"],
                severity=SeverityLevel.HIGH,
                category="memory",
                impact="Memory leak em componente",
                recommendation="Use takeUntil() ou async pipe"
            ))
        
        # NG_002: ChangeDetectionStrategy
        if '@Component' in code and 'OnPush' not in code:
            issues.append(Issue(
                title="ChangeDetectionStrategy não otimizado",
                description=self.get_rules()["NG_002"]["description"],
                severity=SeverityLevel.MEDIUM,
                category="performance",
                impact="Change detection desnecessário",
                recommendation="Adicionar changeDetection: ChangeDetectionStrategy.OnPush"
            ))
        
        # NG_003: Função no template
        if re.search(r'\{\{.*?\(.*?\).*?\}\}', code):
            issues.append(Issue(
                title="Função chamada no template",
                description=self.get_rules()["NG_003"]["description"],
                severity=SeverityLevel.MEDIUM,
                category="performance",
                impact="Re-execução a cada change detection",
                recommendation="Usar pipe ou computed property"
            ))
        
        quality_score = self.calculate_quality_score(issues)
        
        metrics = Metrics(
            readability=max(0, 80 - len(issues) * 5),
            performance="high" if len([i for i in issues if i.category == "performance"]) == 0 else "medium",
            eco_impact="low" if len(issues) <= 1 else "medium",
            maintainability=max(0, 85 - len(issues) * 10)
        )
        
        return ReviewResult(
            language=language,
            quality_score=quality_score,
            issues=issues,
            metrics=metrics,
            recommendations=[f"Corrigir {len(issues)} problema(s) de Angular"] if issues else []
        )
