"""
PHP Plugin - FASE 3
Análise específica para PHP
"""
from typing import List, Dict
import re

from review_engine.plugins.base_plugin import BasePlugin
from review_engine.core.dto import ReviewResult, Issue, Metrics, SeverityLevel


class PHPPlugin(BasePlugin):
    """Plugin para análise de código PHP"""
    
    def get_supported_languages(self) -> List[str]:
        return ["php"]
    
    def get_rules(self) -> Dict[str, dict]:
        return {
            "PHP_001": {
                "name": "SQL Injection vulnerável",
                "description": "Concatenação direta em queries SQL",
                "severity": "critical",
                "category": "security",
                "impact": "critical"
            },
            "PHP_002": {
                "name": "Uso de eval()",
                "description": "eval() é extremamente perigoso",
                "severity": "critical",
                "category": "security",
                "impact": "critical"
            },
            "PHP_003": {
                "name": "Error suppression (@)",
                "description": "Operador @ oculta erros importantes",
                "severity": "medium",
                "category": "error-handling",
                "impact": "medium"
            }
        }
    
    def analyze(self, code: str, language: str) -> ReviewResult:
        issues = []
        
        # PHP_001: SQL Injection
        sql_patterns = [
            r'\$.*?SELECT.*?\$',
            r'mysql_query.*?\$',
            r'mysqli_query.*?\$',
            r'"SELECT.*?\"\s*\.\s*\$'
        ]
        for pattern in sql_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append(Issue(
                    title="Potencial SQL Injection detectado",
                    description=self.get_rules()["PHP_001"]["description"],
                    severity=SeverityLevel.CRITICAL,
                    category="security",
                    impact="Vulnerabilidade crítica de segurança",
                    recommendation="Use prepared statements (PDO ou mysqli)"
                ))
                break
        
        # PHP_002: eval()
        if 'eval(' in code:
            issues.append(Issue(
                title="Uso de eval() detectado",
                description=self.get_rules()["PHP_002"]["description"],
                severity=SeverityLevel.CRITICAL,
                category="security",
                impact="Execução arbitrária de código",
                recommendation="Remover eval() e usar alternativas seguras"
            ))
        
        # PHP_003: Error suppression
        if '@' in code and re.search(r'@\s*\w+\s*\(', code):
            issues.append(Issue(
                title="Error suppression (@) encontrado",
                description=self.get_rules()["PHP_003"]["description"],
                severity=SeverityLevel.MEDIUM,
                category="error-handling",
                impact="Dificulta debugging",
                recommendation="Remover @ e tratar erros adequadamente"
            ))
        
        quality_score = self.calculate_quality_score(issues)
        
        metrics = Metrics(
            readability=max(0, 75 - len(issues) * 5),
            performance="medium",
            eco_impact="medium",
            maintainability=max(0, 80 - len(issues) * 15)
        )
        
        return ReviewResult(
            language=language,
            quality_score=quality_score,
            issues=issues,
            metrics=metrics,
            recommendations=[f"Corrigir {len(issues)} problema(s) de PHP"] if issues else []
        )
