"""
Vue.js Plugin - FASE 3
Análise específica para Vue.js
"""
from typing import List, Dict
import re

from review_engine.plugins.base_plugin import BasePlugin
from review_engine.core.dto import ReviewResult, Issue, Metrics, SeverityLevel


class VuePlugin(BasePlugin):
    """Plugin para análise de código Vue.js"""
    
    def get_supported_languages(self) -> List[str]:
        return ["vue"]
    
    def get_rules(self) -> Dict[str, dict]:
        return {
            "VUE_001": {
                "name": "v-if e v-for no mesmo elemento",
                "description": "v-if tem menor prioridade que v-for",
                "severity": "high",
                "category": "performance",
                "impact": "high"
            },
            "VUE_002": {
                "name": "Key ausente em v-for",
                "description": "v-for sem :key pode causar bugs",
                "severity": "medium",
                "category": "best-practice",
                "impact": "medium"
            },
            "VUE_003": {
                "name": "Mutação direta de prop",
                "description": "Props não devem ser mutadas diretamente",
                "severity": "high",
                "category": "best-practice",
                "impact": "high"
            }
        }
    
    def analyze(self, code: str, language: str) -> ReviewResult:
        issues = []
        
        # VUE_001: v-if e v-for juntos
        if re.search(r'v-for.*v-if|v-if.*v-for', code):
            issues.append(Issue(
                title="v-if e v-for no mesmo elemento",
                description=self.get_rules()["VUE_001"]["description"],
                severity=SeverityLevel.HIGH,
                category="performance",
                impact="Re-renderização desnecessária",
                recommendation="Mover v-if para elemento wrapper ou usar computed"
            ))
        
        # VUE_002: v-for sem key
        if re.search(r'v-for=(?!.*:key)', code):
            issues.append(Issue(
                title=":key ausente em v-for",
                description=self.get_rules()["VUE_002"]["description"],
                severity=SeverityLevel.MEDIUM,
                category="best-practice",
                impact="Problemas de reconciliação DOM",
                recommendation="Adicionar :key com valor único"
            ))
        
        # VUE_003: Mutação de prop
        if re.search(r'this\.\w+\s*=.*props\.|props\.\w+\s*=', code):
            issues.append(Issue(
                title="Mutação direta de prop detectada",
                description=self.get_rules()["VUE_003"]["description"],
                severity=SeverityLevel.HIGH,
                category="best-practice",
                impact="Unidirectional data flow quebrado",
                recommendation="Emitir evento ou usar computed com setter"
            ))
        
        quality_score = self.calculate_quality_score(issues)
        
        metrics = Metrics(
            readability=max(0, 85 - len(issues) * 5),
            performance="high" if len([i for i in issues if i.category == "performance"]) == 0 else "medium",
            eco_impact="low",
            maintainability=max(0, 90 - len(issues) * 10)
        )
        
        return ReviewResult(
            language=language,
            quality_score=quality_score,
            issues=issues,
            metrics=metrics,
            recommendations=[f"Corrigir {len(issues)} problema(s) de Vue.js"] if issues else []
        )
