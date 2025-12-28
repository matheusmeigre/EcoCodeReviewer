"""
YAML Plugin - FASE 3
Análise específica para arquivos YAML
"""
from typing import List, Dict
import re

from review_engine.plugins.base_plugin import BasePlugin
from review_engine.core.dto import ReviewResult, Issue, Metrics, SeverityLevel


class YAMLPlugin(BasePlugin):
    """Plugin para análise de arquivos YAML"""
    
    def get_supported_languages(self) -> List[str]:
        return ["yaml", "yml"]
    
    def get_rules(self) -> Dict[str, dict]:
        return {
            "YAML_001": {
                "name": "Tabs em vez de espaços",
                "description": "YAML não aceita tabs para indentação",
                "severity": "critical",
                "category": "syntax",
                "impact": "critical"
            },
            "YAML_002": {
                "name": "Indentação inconsistente",
                "description": "Mix de 2 e 4 espaços",
                "severity": "high",
                "category": "readability",
                "impact": "high"
            },
            "YAML_003": {
                "name": "Anchor sem referência",
                "description": "Anchor (&) definido mas nunca usado",
                "severity": "low",
                "category": "maintainability",
                "impact": "low"
            },
            "YAML_004": {
                "name": "Secrets em plaintext",
                "description": "Possível senha ou token exposto",
                "severity": "critical",
                "category": "security",
                "impact": "critical"
            }
        }
    
    def analyze(self, code: str, language: str) -> ReviewResult:
        issues = []
        
        # YAML_001: Tabs
        if '\t' in code:
            issues.append(Issue(
                title="Tabs detectados no YAML",
                description=self.get_rules()["YAML_001"]["description"],
                severity=SeverityLevel.CRITICAL,
                category="syntax",
                impact="YAML inválido",
                recommendation="Substituir todos os tabs por espaços"
            ))
        
        # YAML_002: Indentação inconsistente
        indents = re.findall(r'^( +)\S', code, re.MULTILINE)
        indent_sizes = set(len(i) for i in indents)
        if len(indent_sizes) > 1 and not all(i % 2 == 0 for i in indent_sizes):
            issues.append(Issue(
                title="Indentação inconsistente",
                description=self.get_rules()["YAML_002"]["description"],
                severity=SeverityLevel.HIGH,
                category="readability",
                impact="Dificulta leitura e parsing",
                recommendation="Usar consistentemente 2 ou 4 espaços"
            ))
        
        # YAML_003: Anchor não usado
        anchors = set(re.findall(r'&(\w+)', code))
        aliases = set(re.findall(r'\*(\w+)', code))
        unused_anchors = anchors - aliases
        if unused_anchors:
            issues.append(Issue(
                title=f"Anchors não utilizados: {', '.join(unused_anchors)}",
                description=self.get_rules()["YAML_003"]["description"],
                severity=SeverityLevel.LOW,
                category="maintainability",
                impact="Código morto",
                recommendation="Remover anchors não utilizados"
            ))
        
        # YAML_004: Secrets em plaintext
        secret_patterns = [
            r'password\s*:\s*["\']?\w+',
            r'api[_-]?key\s*:\s*["\']?\w+',
            r'secret\s*:\s*["\']?\w+',
            r'token\s*:\s*["\']?\w+'
        ]
        for pattern in secret_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append(Issue(
                    title="Possível secret em plaintext",
                    description=self.get_rules()["YAML_004"]["description"],
                    severity=SeverityLevel.CRITICAL,
                    category="security",
                    impact="Exposição de credenciais",
                    recommendation="Usar variáveis de ambiente ou secrets manager"
                ))
                break
        
        quality_score = self.calculate_quality_score(issues)
        
        metrics = Metrics(
            readability=max(0, 85 - len(issues) * 10),
            performance="high",
            eco_impact="low",
            maintainability=max(0, 90 - len(issues) * 15)
        )
        
        return ReviewResult(
            language=language,
            quality_score=quality_score,
            issues=issues,
            metrics=metrics,
            recommendations=[f"Corrigir {len(issues)} problema(s) de YAML"] if issues else []
        )
