"""
Svelte Plugin - FASE 3
Análise específica para Svelte
"""
from typing import List, Dict
import re

from review_engine.plugins.base_plugin import BasePlugin
from review_engine.core.dto import ReviewResult, Issue, Metrics, SeverityLevel


class SveltePlugin(BasePlugin):
    """Plugin para análise de código Svelte"""
    
    def get_supported_languages(self) -> List[str]:
        return ["svelte"]
    
    def get_rules(self) -> Dict[str, dict]:
        return {
            "SVELTE_001": {
                "name": "Reatividade quebrada",
                "description": "Mutação de array/objeto sem reatribuição",
                "severity": "high",
                "category": "reactivity",
                "impact": "high"
            },
            "SVELTE_002": {
                "name": "Store sem unsubscribe",
                "description": "Subscribe manual sem unsubscribe",
                "severity": "medium",
                "category": "memory",
                "impact": "medium"
            },
            "SVELTE_003": {
                "name": "Binding bidirecional desnecessário",
                "description": "bind: usado onde on: seria suficiente",
                "severity": "low",
                "category": "best-practice",
                "impact": "low"
            }
        }
    
    def analyze(self, code: str, language: str) -> ReviewResult:
        issues = []
        
        # SVELTE_001: Reatividade quebrada
        if re.search(r'\w+\.push\(|\w+\.pop\(|\w+\[\w+\]\s*=(?!\s*\w+\s*=)', code):
            issues.append(Issue(
                title="Potencial problema de reatividade",
                description=self.get_rules()["SVELTE_001"]["description"],
                severity=SeverityLevel.HIGH,
                category="reactivity",
                impact="UI não atualiza",
                recommendation="Reatribuir após mutação: array = array"
            ))
        
        # SVELTE_002: Store sem cleanup
        if '.subscribe(' in code and 'onDestroy' not in code:
            issues.append(Issue(
                title="Store subscription sem cleanup",
                description=self.get_rules()["SVELTE_002"]["description"],
                severity=SeverityLevel.MEDIUM,
                category="memory",
                impact="Memory leak possível",
                recommendation="Use $ syntax ou unsubscribe em onDestroy"
            ))
        
        # SVELTE_003: bind desnecessário
        bind_count = code.count('bind:')
        if bind_count > 3:
            issues.append(Issue(
                title=f"Uso excessivo de bind: ({bind_count}x)",
                description=self.get_rules()["SVELTE_003"]["description"],
                severity=SeverityLevel.LOW,
                category="best-practice",
                impact="Complexidade desnecessária",
                recommendation="Considerar on: para eventos unidirecionais"
            ))
        
        quality_score = self.calculate_quality_score(issues)
        
        metrics = Metrics(
            readability=max(0, 90 - len(issues) * 5),
            performance="high",
            eco_impact="low",
            maintainability=max(0, 92 - len(issues) * 8)
        )
        
        return ReviewResult(
            language=language,
            quality_score=quality_score,
            issues=issues,
            metrics=metrics,
            recommendations=[f"Corrigir {len(issues)} problema(s) de Svelte"] if issues else []
        )
