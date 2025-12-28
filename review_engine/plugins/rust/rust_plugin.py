"""
Rust Plugin - FASE 3
Análise específica para linguagem Rust
"""
from typing import List, Dict
import re

from review_engine.plugins.base_plugin import BasePlugin
from review_engine.core.dto import ReviewResult, Issue, Metrics, SeverityLevel


class RustPlugin(BasePlugin):
    """Plugin para análise de código Rust"""
    
    def get_supported_languages(self) -> List[str]:
        return ["rust"]
    
    def get_rules(self) -> Dict[str, dict]:
        return {
            "RUST_001": {
                "name": "Unsafe block sem justificativa",
                "description": "Código unsafe deve ter comentário explicativo",
                "severity": "critical",
                "category": "safety",
                "impact": "critical"
            },
            "RUST_002": {
                "name": "Clone desnecessário",
                "description": "Uso excessivo de .clone() pode impactar performance",
                "severity": "medium",
                "category": "performance",
                "impact": "medium"
            },
            "RUST_003": {
                "name": "Unwrap sem tratamento",
                "description": "Uso de .unwrap() pode causar panic em runtime",
                "severity": "high",
                "category": "error-handling",
                "impact": "high"
            }
        }
    
    def analyze(self, code: str, language: str) -> ReviewResult:
        issues = []
        
        # RUST_001: Unsafe sem documentação
        unsafe_matches = re.finditer(r'unsafe\s*\{', code)
        for match in unsafe_matches:
            line_start = code.rfind('\n', 0, match.start()) + 1
            prev_line = code[line_start:match.start()].strip()
            if not prev_line.startswith('//'):
                issues.append(Issue(
                    title="Unsafe block sem comentário",
                    description=self.get_rules()["RUST_001"]["description"],
                    severity=SeverityLevel.CRITICAL,
                    category="safety",
                    impact="Undefined behavior possível",
                    recommendation="Adicionar comentário explicando necessidade do unsafe"
                ))
        
        # RUST_002: Clone excessivo
        clone_count = code.count('.clone()')
        if clone_count > 3:
            issues.append(Issue(
                title=f"Uso excessivo de .clone() ({clone_count}x)",
                description=self.get_rules()["RUST_002"]["description"],
                severity=SeverityLevel.MEDIUM,
                category="performance",
                impact="Alocações desnecessárias em heap",
                recommendation="Considerar usar referências (&) em vez de clones"
            ))
        
        # RUST_003: Unwrap perigoso
        if '.unwrap()' in code:
            issues.append(Issue(
                title="Uso de .unwrap() detectado",
                description=self.get_rules()["RUST_003"]["description"],
                severity=SeverityLevel.HIGH,
                category="error-handling",
                impact="Pode causar panic em produção",
                recommendation="Usar .expect() com mensagem ou match para tratar Result/Option"
            ))
        
        quality_score = self.calculate_quality_score(issues)
        
        metrics = Metrics(
            readability=max(0, 90 - len(issues) * 5),
            performance="high" if clone_count <= 2 else "medium",
            eco_impact="low" if clone_count <= 2 else "medium",
            maintainability=max(0, 95 - len(issues) * 10)
        )
        
        return ReviewResult(
            language=language,
            quality_score=quality_score,
            issues=issues,
            metrics=metrics,
            recommendations=[f"Corrigir {len(issues)} problema(s) de Rust"] if issues else []
        )
