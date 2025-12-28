"""
Swift Plugin - FASE 3
Análise específica para Swift
"""
from typing import List, Dict
import re

from review_engine.plugins.base_plugin import BasePlugin
from review_engine.core.dto import ReviewResult, Issue, Metrics, SeverityLevel


class SwiftPlugin(BasePlugin):
    """Plugin para análise de código Swift"""
    
    def get_supported_languages(self) -> List[str]:
        return ["swift"]
    
    def get_rules(self) -> Dict[str, dict]:
        return {
            "SWIFT_001": {
                "name": "Force unwrap (!)",
                "description": "! pode causar crash em runtime",
                "severity": "critical",
                "category": "safety",
                "impact": "critical"
            },
            "SWIFT_002": {
                "name": "Retain cycle em closure",
                "description": "Closure sem [weak self] ou [unowned self]",
                "severity": "high",
                "category": "memory",
                "impact": "high"
            },
            "SWIFT_003": {
                "name": "NSObject em vez de struct",
                "description": "Classes desnecessárias afetam performance",
                "severity": "medium",
                "category": "performance",
                "impact": "medium"
            },
            "SWIFT_004": {
                "name": "Implicitly unwrapped optional",
                "description": "Uso de ! na declaração",
                "severity": "high",
                "category": "safety",
                "impact": "high"
            }
        }
    
    def analyze(self, code: str, language: str) -> ReviewResult:
        issues = []
        
        # SWIFT_001: Force unwrap
        force_unwrap_count = len(re.findall(r'\w+!(?!\s*=)', code))
        if force_unwrap_count > 3:
            issues.append(Issue(
                title=f"Force unwrap excessivo ({force_unwrap_count}x)",
                description=self.get_rules()["SWIFT_001"]["description"],
                severity=SeverityLevel.CRITICAL,
                category="safety",
                impact="Crash potencial em produção",
                recommendation="Usar if let, guard let ou optional chaining (?)"
            ))
        
        # SWIFT_002: Retain cycle
        closure_with_self = re.findall(r'\{[^}]*\bself\.[^}]*\}', code)
        weak_self_closures = re.findall(r'\[weak self\]|\[unowned self\]', code)
        if len(closure_with_self) > len(weak_self_closures):
            issues.append(Issue(
                title="Possível retain cycle em closure",
                description=self.get_rules()["SWIFT_002"]["description"],
                severity=SeverityLevel.HIGH,
                category="memory",
                impact="Memory leak",
                recommendation="Adicionar [weak self] ou [unowned self] em closures"
            ))
        
        # SWIFT_003: Class vs Struct
        if 'class ' in code and 'struct ' not in code and ': NSObject' not in code:
            issues.append(Issue(
                title="Uso de class quando struct seria adequado",
                description=self.get_rules()["SWIFT_003"]["description"],
                severity=SeverityLevel.MEDIUM,
                category="performance",
                impact="Alocação em heap desnecessária",
                recommendation="Considerar usar struct para value types"
            ))
        
        # SWIFT_004: Implicitly unwrapped
        if re.search(r'var\s+\w+\s*:\s*\w+!', code):
            issues.append(Issue(
                title="Implicitly unwrapped optional detectado",
                description=self.get_rules()["SWIFT_004"]["description"],
                severity=SeverityLevel.HIGH,
                category="safety",
                impact="Crash se valor for nil",
                recommendation="Usar optional regular (?) ou inicializar valor"
            ))
        
        quality_score = self.calculate_quality_score(issues)
        
        metrics = Metrics(
            readability=max(0, 88 - len(issues) * 5),
            performance="high" if len([i for i in issues if i.category == "performance"]) == 0 else "medium",
            eco_impact="low" if len(issues) <= 1 else "medium",
            maintainability=max(0, 90 - len(issues) * 10)
        )
        
        return ReviewResult(
            language=language,
            quality_score=quality_score,
            issues=issues,
            metrics=metrics,
            recommendations=[f"Corrigir {len(issues)} problema(s) de Swift"] if issues else []
        )
