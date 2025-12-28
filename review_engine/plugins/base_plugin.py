"""
Base Plugin Interface - FASE 2
Define o contrato que todos os plugins devem seguir
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from review_engine.core.dto import ReviewResult, Issue, Metrics


class BasePlugin(ABC):
    """Interface abstrata para plugins de análise de código"""
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.version = "1.0.0"
    
    @abstractmethod
    def get_supported_languages(self) -> List[str]:
        """Retorna lista de linguagens suportadas pelo plugin"""
        pass
    
    @abstractmethod
    def get_rules(self) -> Dict[str, dict]:
        """
        Retorna dicionário de regras específicas do plugin
        Formato: {
            "rule_id": {
                "name": "Nome da regra",
                "severity": "critical|high|medium|low",
                "category": "performance|readability|eco-code",
                "description": "Descrição da regra"
            }
        }
        """
        pass
    
    @abstractmethod
    def analyze(self, code: str, language: str) -> ReviewResult:
        """
        Executa análise completa do código
        Args:
            code: Código-fonte a ser analisado
            language: Linguagem identificada
        Returns:
            ReviewResult com issues, métricas e código otimizado
        """
        pass
    
    def calculate_quality_score(self, issues: List[Issue]) -> int:
        """
        Calcula score de qualidade baseado nos issues encontrados
        Score base: 100
        - Critical: -20 pontos
        - High: -15 pontos
        - Medium: -10 pontos
        - Low: -5 pontos
        """
        score = 100
        for issue in issues:
            if issue.severity.value == "critical":
                score -= 20
            elif issue.severity.value == "high":
                score -= 15
            elif issue.severity.value == "medium":
                score -= 10
            elif issue.severity.value == "low":
                score -= 5
        return max(0, min(100, score))
    
    def get_plugin_info(self) -> Dict[str, str]:
        """Retorna informações do plugin"""
        return {
            "name": self.name,
            "version": self.version,
            "languages": self.get_supported_languages()
        }


class UniversalPlugin(BasePlugin):
    """
    Plugin com regras universais aplicáveis a todas as linguagens
    - Código morto
    - Complexidade excessiva
    - Nomes não descritivos
    - Duplicação
    """
    
    def get_supported_languages(self) -> List[str]:
        return ["*"]  # Aplica-se a todas
    
    def get_rules(self) -> Dict[str, dict]:
        return {
            "UNIVERSAL_001": {
                "name": "Código Morto",
                "severity": "medium",
                "category": "maintainability",
                "description": "Código não utilizado identificado"
            },
            "UNIVERSAL_002": {
                "name": "Complexidade Ciclomática Alta",
                "severity": "high",
                "category": "readability",
                "description": "Função com complexidade > 10"
            },
            "UNIVERSAL_003": {
                "name": "Nomenclatura Inadequada",
                "severity": "low",
                "category": "readability",
                "description": "Nomes de variáveis/funções não descritivos"
            },
            "UNIVERSAL_004": {
                "name": "Código Duplicado",
                "severity": "medium",
                "category": "maintainability",
                "description": "Blocos de código idênticos detectados"
            }
        }
    
    def analyze(self, code: str, language: str) -> ReviewResult:
        """Análise universal básica"""
        issues = []
        
        # Implementação simplificada - será expandida
        # Análise de nomes curtos (< 2 caracteres)
        import re
        short_vars = re.findall(r'\b[a-z]\b', code)
        if len(short_vars) > 3:
            issues.append(Issue(
                title="Variáveis com nomes muito curtos",
                description=f"Encontradas {len(short_vars)} variáveis com apenas 1 caractere",
                severity="low",
                impact="Dificulta legibilidade e manutenção",
                rule_id="UNIVERSAL_003"
            ))
        
        quality_score = self.calculate_quality_score(issues)
        
        return ReviewResult(
            language=language,
            quality_score=quality_score,
            issues=issues,
            has_issues=len(issues) > 0
        )
