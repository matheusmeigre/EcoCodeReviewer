"""
JavaScript Plugin - FASE 3
Análise específica para JavaScript/ECMAScript
"""
from typing import List, Dict
import re

from review_engine.plugins.base_plugin import BasePlugin
from review_engine.core.dto import ReviewResult, Issue, Metrics, SeverityLevel, ImpactLevel


class JavaScriptPlugin(BasePlugin):
    """Plugin para análise de código JavaScript"""
    
    def __init__(self):
        super().__init__()
        self.name = "JavaScriptPlugin"
        self.version = "2.0.0"
    
    def get_supported_languages(self) -> List[str]:
        return ["javascript", "typescript", "react"]
    
    def get_rules(self) -> Dict[str, dict]:
        return {
            "JS_001": {
                "name": "Var ao invés de let/const",
                "severity": "medium",
                "category": "readability",
                "description": "Usar let/const (ES6+) ao invés de var"
            },
            "JS_002": {
                "name": "Loop ineficiente",
                "severity": "medium",
                "category": "performance",
                "description": "Usar forEach/map/filter ao invés de for loops"
            },
            "JS_003": {
                "name": "Promise sem tratamento de erro",
                "severity": "high",
                "category": "reliability",
                "description": "Promise sem .catch() ou try/catch"
            }
        }
    
    def analyze(self, code: str, language: str) -> ReviewResult:
        """Análise JavaScript"""
        issues = []
        
        # JS_001: Uso de var
        if re.search(r'\bvar\s+\w+', code):
            issues.append(Issue(
                title="Uso de 'var' detectado",
                description="Usar 'let' ou 'const' (ES6+) melhora escopo e previne bugs",
                severity=SeverityLevel.MEDIUM,
                impact="Pode causar bugs de escopo e hoisting",
                rule_id="JS_001"
            ))
        
        quality_score = self.calculate_quality_score(issues)
        
        return ReviewResult(
            language=language,
            quality_score=quality_score,
            issues=issues,
            has_issues=len(issues) > 0
        )
