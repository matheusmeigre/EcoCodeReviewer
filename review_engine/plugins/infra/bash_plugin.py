"""
Bash Plugin - FASE 3
Análise específica para scripts Bash
"""
from typing import List, Dict
import re

from review_engine.plugins.base_plugin import BasePlugin
from review_engine.core.dto import ReviewResult, Issue, Metrics, SeverityLevel


class BashPlugin(BasePlugin):
    """Plugin para análise de scripts Bash"""
    
    def get_supported_languages(self) -> List[str]:
        return ["bash", "shell", "sh"]
    
    def get_rules(self) -> Dict[str, dict]:
        return {
            "BASH_001": {
                "name": "Variável sem aspas",
                "description": "Variáveis devem estar entre aspas",
                "severity": "high",
                "category": "safety",
                "impact": "high"
            },
            "BASH_002": {
                "name": "Sem set -e",
                "description": "Script sem tratamento de erros",
                "severity": "medium",
                "category": "error-handling",
                "impact": "medium"
            },
            "BASH_003": {
                "name": "Uso de eval",
                "description": "eval é perigoso e deve ser evitado",
                "severity": "critical",
                "category": "security",
                "impact": "critical"
            },
            "BASH_004": {
                "name": "Pipe para while sem <()",
                "description": "Pipe cria subshell e variáveis não persistem",
                "severity": "medium",
                "category": "logic",
                "impact": "medium"
            }
        }
    
    def analyze(self, code: str, language: str) -> ReviewResult:
        issues = []
        
        # BASH_001: Variáveis sem aspas
        unquoted_vars = re.findall(r'(?<!")(\$\w+|\$\{\w+\})(?!")', code)
        if len(unquoted_vars) > 5:
            issues.append(Issue(
                title=f"Variáveis sem aspas ({len(unquoted_vars)}x)",
                description=self.get_rules()["BASH_001"]["description"],
                severity=SeverityLevel.HIGH,
                category="safety",
                impact="Word splitting pode causar bugs",
                recommendation='Usar "$VAR" em vez de $VAR'
            ))
        
        # BASH_002: Sem set -e
        if 'set -e' not in code and 'set -o errexit' not in code:
            issues.append(Issue(
                title="Script sem set -e",
                description=self.get_rules()["BASH_002"]["description"],
                severity=SeverityLevel.MEDIUM,
                category="error-handling",
                impact="Erros silenciosos",
                recommendation="Adicionar 'set -euo pipefail' no início"
            ))
        
        # BASH_003: eval perigoso
        if 'eval' in code:
            issues.append(Issue(
                title="Uso de eval detectado",
                description=self.get_rules()["BASH_003"]["description"],
                severity=SeverityLevel.CRITICAL,
                category="security",
                impact="Code injection possível",
                recommendation="Evitar eval ou sanitizar input cuidadosamente"
            ))
        
        # BASH_004: Pipe para while
        if re.search(r'\|\s*while\s+read', code):
            issues.append(Issue(
                title="Pipe para while read",
                description=self.get_rules()["BASH_004"]["description"],
                severity=SeverityLevel.MEDIUM,
                category="logic",
                impact="Variáveis definidas no loop não persistem",
                recommendation="Usar while read < <(command) ou process substitution"
            ))
        
        quality_score = self.calculate_quality_score(issues)
        
        metrics = Metrics(
            readability=max(0, 75 - len(issues) * 5),
            performance="medium",
            eco_impact="low",
            maintainability=max(0, 70 - len(issues) * 10)
        )
        
        return ReviewResult(
            language=language,
            quality_score=quality_score,
            issues=issues,
            metrics=metrics,
            recommendations=[f"Corrigir {len(issues)} problema(s) de Bash"] if issues else []
        )
