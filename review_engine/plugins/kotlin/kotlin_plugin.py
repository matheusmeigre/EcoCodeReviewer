"""
Kotlin Plugin - FASE 3
Análise específica para Kotlin
"""
from typing import List, Dict
import re

from review_engine.plugins.base_plugin import BasePlugin
from review_engine.core.dto import ReviewResult, Issue, Metrics, SeverityLevel


class KotlinPlugin(BasePlugin):
    """Plugin para análise de código Kotlin"""
    
    def get_supported_languages(self) -> List[str]:
        return ["kotlin"]
    
    def get_rules(self) -> Dict[str, dict]:
        return {
            "KOTLIN_001": {
                "name": "Uso de !! (not-null assertion)",
                "description": "!! pode causar NullPointerException",
                "severity": "high",
                "category": "null-safety",
                "impact": "high"
            },
            "KOTLIN_002": {
                "name": "Suspend function sem coroutine scope",
                "description": "Função suspensa precisa de escopo adequado",
                "severity": "medium",
                "category": "concurrency",
                "impact": "medium"
            },
            "KOTLIN_003": {
                "name": "Data class sem copy",
                "description": "Mutação direta de data class",
                "severity": "low",
                "category": "immutability",
                "impact": "low"
            },
            "KOTLIN_004": {
                "name": "forEach em vez de for",
                "description": "forEach menos eficiente que for clássico",
                "severity": "low",
                "category": "performance",
                "impact": "low"
            }
        }
    
    def analyze(self, code: str, language: str) -> ReviewResult:
        issues = []
        
        # KOTLIN_001: !! assertion
        not_null_count = code.count('!!')
        if not_null_count > 2:
            issues.append(Issue(
                title=f"Uso excessivo de !! ({not_null_count}x)",
                description=self.get_rules()["KOTLIN_001"]["description"],
                severity=SeverityLevel.HIGH,
                category="null-safety",
                impact="Pode causar crashes em runtime",
                recommendation="Usar ?.let, ?: ou safe calls"
            ))
        
        # KOTLIN_002: Suspend sem scope
        if 'suspend fun' in code and 'CoroutineScope' not in code and 'viewModelScope' not in code:
            issues.append(Issue(
                title="Suspend function sem scope detectada",
                description=self.get_rules()["KOTLIN_002"]["description"],
                severity=SeverityLevel.MEDIUM,
                category="concurrency",
                impact="Lifecycle de coroutine mal gerenciado",
                recommendation="Usar viewModelScope, lifecycleScope ou CoroutineScope"
            ))
        
        # KOTLIN_003: Data class mutation
        if re.search(r'data class.*var\s+\w+', code):
            issues.append(Issue(
                title="Data class com propriedades mutáveis",
                description=self.get_rules()["KOTLIN_003"]["description"],
                severity=SeverityLevel.LOW,
                category="immutability",
                impact="Dificulta rastreamento de mudanças",
                recommendation="Usar val e método .copy() para mutações"
            ))
        
        # KOTLIN_004: forEach performance
        if '.forEach' in code and 'large' in code.lower():
            issues.append(Issue(
                title="forEach em coleção grande",
                description=self.get_rules()["KOTLIN_004"]["description"],
                severity=SeverityLevel.LOW,
                category="performance",
                impact="Overhead de lambda",
                recommendation="Usar for loop clássico para melhor performance"
            ))
        
        quality_score = self.calculate_quality_score(issues)
        
        metrics = Metrics(
            readability=max(0, 90 - len(issues) * 5),
            performance="high" if len([i for i in issues if i.category == "performance"]) == 0 else "medium",
            eco_impact="low",
            maintainability=max(0, 92 - len(issues) * 8)
        )
        
        return ReviewResult(
            language=language,
            quality_score=quality_score,
            issues=issues,
            metrics=metrics,
            recommendations=[f"Corrigir {len(issues)} problema(s) de Kotlin"] if issues else []
        )
