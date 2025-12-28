"""
Dockerfile Plugin - FASE 3
Análise específica para Dockerfiles
"""
from typing import List, Dict
import re

from review_engine.plugins.base_plugin import BasePlugin
from review_engine.core.dto import ReviewResult, Issue, Metrics, SeverityLevel


class DockerfilePlugin(BasePlugin):
    """Plugin para análise de Dockerfiles"""
    
    def get_supported_languages(self) -> List[str]:
        return ["dockerfile", "docker"]
    
    def get_rules(self) -> Dict[str, dict]:
        return {
            "DOCKER_001": {
                "name": "Tag :latest",
                "description": "Usar tag específica em vez de :latest",
                "severity": "high",
                "category": "reproducibility",
                "impact": "high"
            },
            "DOCKER_002": {
                "name": "Múltiplos RUN",
                "description": "RUN separados criam layers desnecessários",
                "severity": "medium",
                "category": "performance",
                "impact": "medium"
            },
            "DOCKER_003": {
                "name": "Cache não otimizado",
                "description": "COPY antes de instalar dependências",
                "severity": "medium",
                "category": "build-time",
                "impact": "medium"
            },
            "DOCKER_004": {
                "name": "Execução como root",
                "description": "Container sem USER não-root",
                "severity": "high",
                "category": "security",
                "impact": "high"
            }
        }
    
    def analyze(self, code: str, language: str) -> ReviewResult:
        issues = []
        
        # DOCKER_001: :latest tag
        if re.search(r'FROM\s+\w+:latest', code, re.IGNORECASE):
            issues.append(Issue(
                title="Uso de tag :latest",
                description=self.get_rules()["DOCKER_001"]["description"],
                severity=SeverityLevel.HIGH,
                category="reproducibility",
                impact="Builds não reproduzíveis",
                recommendation="Especificar versão exata: FROM node:18.16.0"
            ))
        
        # DOCKER_002: Múltiplos RUN
        run_count = len(re.findall(r'^RUN\s+', code, re.MULTILINE))
        if run_count > 3:
            issues.append(Issue(
                title=f"Múltiplos comandos RUN ({run_count}x)",
                description=self.get_rules()["DOCKER_002"]["description"],
                severity=SeverityLevel.MEDIUM,
                category="performance",
                impact="Imagem maior e build mais lento",
                recommendation="Combinar RUN com && para reduzir layers"
            ))
        
        # DOCKER_003: COPY antes de dependências
        lines = code.split('\n')
        copy_idx = next((i for i, l in enumerate(lines) if l.strip().startswith('COPY')), None)
        install_idx = next((i for i, l in enumerate(lines) if 'install' in l.lower() or 'apt' in l.lower()), None)
        
        if copy_idx and install_idx and copy_idx < install_idx:
            issues.append(Issue(
                title="COPY antes de instalar dependências",
                description=self.get_rules()["DOCKER_003"]["description"],
                severity=SeverityLevel.MEDIUM,
                category="build-time",
                impact="Cache invalidado desnecessariamente",
                recommendation="Copiar package.json primeiro, instalar deps, depois COPY código"
            ))
        
        # DOCKER_004: Sem USER
        if 'USER ' not in code:
            issues.append(Issue(
                title="Container executa como root",
                description=self.get_rules()["DOCKER_004"]["description"],
                severity=SeverityLevel.HIGH,
                category="security",
                impact="Risco de segurança",
                recommendation="Adicionar USER não-root antes de CMD/ENTRYPOINT"
            ))
        
        quality_score = self.calculate_quality_score(issues)
        
        metrics = Metrics(
            readability=max(0, 80 - len(issues) * 5),
            performance="high" if run_count <= 3 else "medium",
            eco_impact="medium" if run_count > 5 else "low",
            maintainability=max(0, 85 - len(issues) * 10)
        )
        
        return ReviewResult(
            language=language,
            quality_score=quality_score,
            issues=issues,
            metrics=metrics,
            recommendations=[f"Corrigir {len(issues)} problema(s) de Dockerfile"] if issues else []
        )
