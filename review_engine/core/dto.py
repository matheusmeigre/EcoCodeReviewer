"""
Data Transfer Objects (DTOs) - Contratos Padronizados
FASE 1: Normalização de Saída
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum


class SeverityLevel(Enum):
    """Níveis de severidade dos problemas"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ImpactLevel(Enum):
    """Níveis de impacto (eco-code)"""
    BAIXO = "Baixo"
    MEDIO = "Médio"
    ALTO = "Alto"


@dataclass
class Issue:
    """Representa um problema identificado no código"""
    title: str
    description: str
    severity: SeverityLevel
    impact: str
    original_code: Optional[str] = None
    line_number: Optional[int] = None
    rule_id: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "severity": self.severity.value,
            "impact": self.impact,
            "originalCode": self.original_code,
            "lineNumber": self.line_number,
            "ruleId": self.rule_id
        }


@dataclass
class Metrics:
    """Métricas de qualidade e eco-code"""
    readability: int  # 0-100
    performance: ImpactLevel
    eco_impact: ImpactLevel
    maintainability: int  # 0-100
    complexity_reduction: str = "N/A"
    memory_impact: str = "N/A"
    estimated_speedup: str = "N/A"
    energy_savings: str = "N/A"
    
    def to_dict(self) -> dict:
        return {
            "readability": self.readability,
            "performance": self.performance.value,
            "ecoImpact": self.eco_impact.value,
            "maintainability": self.maintainability,
            "complexityReduction": self.complexity_reduction,
            "memoryImpact": self.memory_impact,
            "estimatedSpeedup": self.estimated_speedup,
            "energySavings": self.energy_savings
        }


@dataclass
class ReviewResult:
    """Contrato único de saída do code review"""
    language: str
    quality_score: int  # 0-100
    issues: List[Issue] = field(default_factory=list)
    optimized_code: Optional[str] = None
    explanation: Optional[str] = None
    explanation_html: Optional[str] = None
    metrics: Optional[Metrics] = None
    has_issues: bool = False
    confidence_level: Optional[int] = None  # Para auto-detecção
    
    def to_dict(self) -> dict:
        return {
            "language": self.language,
            "qualityScore": self.quality_score,
            "issues": [issue.to_dict() for issue in self.issues],
            "optimizedCode": self.optimized_code,
            "explanation": self.explanation,
            "explanationHtml": self.explanation_html,
            "metrics": self.metrics.to_dict() if self.metrics else None,
            "hasIssues": self.has_issues,
            "confidenceLevel": self.confidence_level
        }


@dataclass
class DetectionResult:
    """Resultado da detecção automática de linguagem"""
    language: str
    confidence: int  # 0-100
    detected_by: str  # "extension", "keywords", "syntax", "ai"
    fallback_required: bool = False
    
    def to_dict(self) -> dict:
        return {
            "language": self.language,
            "confidence": self.confidence,
            "detectedBy": self.detected_by,
            "fallbackRequired": self.fallback_required
        }
