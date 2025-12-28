"""
Terraform Plugin - FASE 3
Análise específica para Terraform
"""
from typing import List, Dict
import re

from review_engine.plugins.base_plugin import BasePlugin
from review_engine.core.dto import ReviewResult, Issue, Metrics, SeverityLevel


class TerraformPlugin(BasePlugin):
    """Plugin para análise de código Terraform"""
    
    def get_supported_languages(self) -> List[str]:
        return ["terraform", "tf", "hcl"]
    
    def get_rules(self) -> Dict[str, dict]:
        return {
            "TF_001": {
                "name": "Versão não especificada",
                "description": "required_version não definida",
                "severity": "high",
                "category": "reproducibility",
                "impact": "high"
            },
            "TF_002": {
                "name": "Secrets em variáveis",
                "description": "Secrets hardcoded no código",
                "severity": "critical",
                "category": "security",
                "impact": "critical"
            },
            "TF_003": {
                "name": "Recurso sem tags",
                "description": "Recursos sem tags de organização",
                "severity": "low",
                "category": "maintainability",
                "impact": "low"
            },
            "TF_004": {
                "name": "Backend não configurado",
                "description": "State local em vez de remoto",
                "severity": "high",
                "category": "collaboration",
                "impact": "high"
            }
        }
    
    def analyze(self, code: str, language: str) -> ReviewResult:
        issues = []
        
        # TF_001: Versão não especificada
        if 'required_version' not in code and 'terraform {' in code:
            issues.append(Issue(
                title="Versão do Terraform não especificada",
                description=self.get_rules()["TF_001"]["description"],
                severity=SeverityLevel.HIGH,
                category="reproducibility",
                impact="Incompatibilidades entre ambientes",
                recommendation="Adicionar required_version = '>= 1.0' no bloco terraform"
            ))
        
        # TF_002: Secrets hardcoded
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
            r'key\s*=\s*["\'][\w-]{20,}["\']'
        ]
        for pattern in secret_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append(Issue(
                    title="Secret hardcoded detectado",
                    description=self.get_rules()["TF_002"]["description"],
                    severity=SeverityLevel.CRITICAL,
                    category="security",
                    impact="Exposição de credenciais no código",
                    recommendation="Usar var.senha ou data.aws_secretsmanager_secret"
                ))
                break
        
        # TF_003: Recursos sem tags
        resources = re.findall(r'resource\s+"[^"]+"\s+"[^"]+"', code)
        resources_with_tags = code.count('tags = {')
        if len(resources) > 2 and resources_with_tags < len(resources) // 2:
            issues.append(Issue(
                title="Recursos sem tags adequadas",
                description=self.get_rules()["TF_003"]["description"],
                severity=SeverityLevel.LOW,
                category="maintainability",
                impact="Dificulta organização e billing",
                recommendation="Adicionar tags (Environment, Project, Owner) em todos recursos"
            ))
        
        # TF_004: Backend não configurado
        if 'backend' not in code and 'terraform {' in code:
            issues.append(Issue(
                title="Backend remoto não configurado",
                description=self.get_rules()["TF_004"]["description"],
                severity=SeverityLevel.HIGH,
                category="collaboration",
                impact="State não compartilhado entre time",
                recommendation="Configurar backend S3/Azure/GCS no bloco terraform"
            ))
        
        quality_score = self.calculate_quality_score(issues)
        
        metrics = Metrics(
            readability=max(0, 85 - len(issues) * 5),
            performance="high",
            eco_impact="low",
            maintainability=max(0, 90 - len(issues) * 10)
        )
        
        return ReviewResult(
            language=language,
            quality_score=quality_score,
            issues=issues,
            metrics=metrics,
            recommendations=[f"Corrigir {len(issues)} problema(s) de Terraform"] if issues else []
        )
