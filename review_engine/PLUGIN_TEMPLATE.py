# 🔌 Template de Plugin - Review Engine v2.0

Este template facilita a criação de novos plugins para análise de código.

## 📋 Estrutura Básica

```python
"""
Plugin para análise de código [NOME_DA_LINGUAGEM].

Implementa regras específicas de:
- Performance
- Segurança
- Eco-eficiência
- Boas práticas

Autor: [SEU_NOME]
Data: [DATA]
Versão: 1.0.0
"""

import re
from typing import List, Dict
from review_engine.plugins.base_plugin import BasePlugin
from review_engine.core.dto import (
    ReviewResult, Issue, Metrics,
    SeverityLevel, ImpactLevel
)


class [NomeDaLinguagem]Plugin(BasePlugin):
    """
    Plugin para análise de código [NOME_DA_LINGUAGEM].
    
    Linguagens suportadas:
    - [linguagem1]
    - [linguagem2] (opcional)
    
    Regras implementadas:
    - [CÓDIGO_001]: [Descrição da regra]
    - [CÓDIGO_002]: [Descrição da regra]
    """
    
    def get_supported_languages(self) -> List[str]:
        """
        Define quais linguagens este plugin analisa.
        
        Returns:
            List[str]: Lista de linguagens (lowercase).
        """
        return ["linguagem1", "linguagem2"]
    
    def get_rules(self) -> Dict[str, dict]:
        """
        Define regras de análise específicas da linguagem.
        
        Returns:
            Dict[str, dict]: Dicionário com código da regra como chave.
        """
        return {
            "LANG_001": {
                "name": "Nome da regra",
                "description": "Descrição detalhada do problema",
                "severity": "medium",  # low, medium, high, critical
                "category": "performance",  # performance, security, style, eco-code
                "impact": "medium",  # low, medium, high
                "recommendation": "Como corrigir o problema"
            },
            
            "LANG_002": {
                "name": "Segunda regra",
                "description": "Outra verificação importante",
                "severity": "high",
                "category": "security",
                "impact": "high",
                "recommendation": "Sugestão de correção"
            }
        }
    
    def analyze(self, code: str, language: str) -> ReviewResult:
        """
        Método principal de análise.
        
        Args:
            code (str): Código-fonte a ser analisado
            language (str): Linguagem detectada
        
        Returns:
            ReviewResult: Resultado estruturado da análise
        """
        issues = []
        
        # ==============================================================
        # REGRA 1: [DESCRIÇÃO]
        # ==============================================================
        issues.extend(self._check_rule_001(code))
        
        # ==============================================================
        # REGRA 2: [DESCRIÇÃO]
        # ==============================================================
        issues.extend(self._check_rule_002(code))
        
        # Calcular métricas específicas
        metrics = self._calculate_metrics(code, issues)
        
        # Gerar recomendações
        recommendations = self._generate_recommendations(issues)
        
        # Calcular quality score (herdado de BasePlugin)
        quality_score = self.calculate_quality_score(issues)
        
        return ReviewResult(
            language=language,
            quality_score=quality_score,
            issues=issues,
            metrics=metrics,
            recommendations=recommendations,
            html_output=self._generate_html_output(issues, metrics)
        )
    
    # =================================================================
    # MÉTODOS PRIVADOS - IMPLEMENTAÇÃO DAS REGRAS
    # =================================================================
    
    def _check_rule_001(self, code: str) -> List[Issue]:
        """
        Verifica [DESCRIÇÃO DA REGRA 001].
        
        Exemplo de padrão problemático:
        ```[linguagem]
        // Código ruim
        ```
        
        Recomendação:
        ```[linguagem]
        // Código bom
        ```
        
        Args:
            code (str): Código a analisar
        
        Returns:
            List[Issue]: Lista de problemas encontrados
        """
        issues = []
        
        # Padrão regex para detectar o problema
        pattern = r'padrão_regex_aqui'
        matches = re.finditer(pattern, code, re.MULTILINE)
        
        for match in matches:
            # Calcular linha onde ocorre o problema
            line_number = code[:match.start()].count('\n') + 1
            
            rule = self.get_rules()["LANG_001"]
            
            issues.append(Issue(
                id="LANG_001",
                title=rule["name"],
                description=rule["description"],
                severity=SeverityLevel.from_string(rule["severity"]),
                category=rule["category"],
                line_number=line_number,
                code_snippet=match.group(0),
                impact=rule["impact"],
                recommendation=rule["recommendation"]
            ))
        
        return issues
    
    def _check_rule_002(self, code: str) -> List[Issue]:
        """
        Verifica [DESCRIÇÃO DA REGRA 002].
        
        Args:
            code (str): Código a analisar
        
        Returns:
            List[Issue]: Lista de problemas encontrados
        """
        issues = []
        
        # Implementar lógica de verificação
        # Similar ao _check_rule_001
        
        return issues
    
    # =================================================================
    # CÁLCULO DE MÉTRICAS
    # =================================================================
    
    def _calculate_metrics(self, code: str, issues: List[Issue]) -> Metrics:
        """
        Calcula métricas específicas da linguagem.
        
        Args:
            code (str): Código analisado
            issues (List[Issue]): Problemas encontrados
        
        Returns:
            Metrics: Métricas calculadas
        """
        # Contadores básicos
        lines = len(code.split('\n'))
        functions = len(re.findall(r'function|def|method', code))
        
        # Cálculo de readability (0-100)
        readability = 100
        if len(issues) > 0:
            readability -= len([i for i in issues if i.category == "style"]) * 5
            readability = max(0, readability)
        
        # Avaliação de performance
        perf_issues = [i for i in issues if i.category == "performance"]
        if len(perf_issues) == 0:
            performance = "high"
        elif len(perf_issues) <= 2:
            performance = "medium"
        else:
            performance = "low"
        
        # Impacto ecológico
        eco_issues = [i for i in issues if "eco" in i.category.lower()]
        if len(eco_issues) == 0:
            eco_impact = "low"
        elif len(eco_issues) <= 2:
            eco_impact = "medium"
        else:
            eco_impact = "high"
        
        return Metrics(
            readability=readability,
            performance=performance,
            eco_impact=eco_impact,
            maintainability=max(0, 100 - len(issues) * 5),
            complexity_reduction=self._calculate_complexity_reduction(issues),
            memory_impact=self._calculate_memory_impact(issues),
            estimated_speedup=self._estimate_speedup(perf_issues),
            energy_savings=self._estimate_energy_savings(eco_issues)
        )
    
    def _calculate_complexity_reduction(self, issues: List[Issue]) -> str:
        """Calcula redução de complexidade se issues forem corrigidos."""
        complexity_issues = len([i for i in issues if "complex" in i.description.lower()])
        
        if complexity_issues == 0:
            return "Nenhuma redução prevista"
        elif complexity_issues <= 2:
            return f"Redução de {complexity_issues * 10}% em complexidade"
        else:
            return f"Redução significativa de {complexity_issues * 15}% em complexidade"
    
    def _calculate_memory_impact(self, issues: List[Issue]) -> str:
        """Estima impacto em memória."""
        memory_issues = [i for i in issues if "memory" in i.description.lower() or "cache" in i.description.lower()]
        
        if len(memory_issues) == 0:
            return "Sem impacto significativo"
        else:
            return f"Redução estimada de {len(memory_issues) * 5}% no uso de memória"
    
    def _estimate_speedup(self, perf_issues: List[Issue]) -> str:
        """Estima ganho de velocidade."""
        if len(perf_issues) == 0:
            return "Nenhum speedup esperado"
        elif len(perf_issues) <= 2:
            return "Speedup de 1.5-2x possível"
        else:
            return "Speedup de 2-5x possível"
    
    def _estimate_energy_savings(self, eco_issues: List[Issue]) -> str:
        """Estima economia energética."""
        if len(eco_issues) == 0:
            return "Nenhuma economia detectada"
        elif len(eco_issues) <= 2:
            return "Economia de ~10% em CPU"
        else:
            return "Economia de ~20% em CPU/memória"
    
    # =================================================================
    # GERAÇÃO DE RECOMENDAÇÕES
    # =================================================================
    
    def _generate_recommendations(self, issues: List[Issue]) -> List[str]:
        """
        Gera recomendações gerais baseadas nos issues encontrados.
        
        Args:
            issues (List[Issue]): Problemas detectados
        
        Returns:
            List[str]: Lista de recomendações
        """
        recommendations = []
        
        # Agrupar por categoria
        by_category = {}
        for issue in issues:
            if issue.category not in by_category:
                by_category[issue.category] = []
            by_category[issue.category].append(issue)
        
        # Gerar recomendações por categoria
        if "performance" in by_category:
            count = len(by_category["performance"])
            recommendations.append(
                f"Otimizar {count} problema(s) de performance para reduzir tempo de execução"
            )
        
        if "security" in by_category:
            count = len(by_category["security"])
            recommendations.append(
                f"Corrigir {count} vulnerabilidade(s) de segurança identificada(s)"
            )
        
        if "eco-code" in by_category:
            count = len(by_category["eco-code"])
            recommendations.append(
                f"Aplicar {count} otimização(ões) de eco-eficiência para reduzir consumo energético"
            )
        
        return recommendations
    
    # =================================================================
    # GERAÇÃO DE HTML
    # =================================================================
    
    def _generate_html_output(self, issues: List[Issue], metrics: Metrics) -> str:
        """
        Gera saída HTML formatada.
        
        Args:
            issues (List[Issue]): Problemas encontrados
            metrics (Metrics): Métricas calculadas
        
        Returns:
            str: HTML formatado
        """
        html = "<div class='review-result'>"
        
        # Seção de métricas
        html += "<div class='metrics-section'>"
        html += f"<p><strong>Readability:</strong> {metrics.readability}/100</p>"
        html += f"<p><strong>Performance:</strong> {metrics.performance}</p>"
        html += f"<p><strong>Eco-Impact:</strong> {metrics.eco_impact}</p>"
        html += "</div>"
        
        # Seção de issues
        if issues:
            html += "<div class='issues-section'>"
            html += f"<h3>Problemas Encontrados ({len(issues)})</h3>"
            html += "<ul>"
            for issue in issues:
                severity_class = issue.severity.value
                html += f"<li class='issue-{severity_class}'>"
                html += f"<strong>[{issue.id}]</strong> {issue.title}"
                html += f"<p>{issue.description}</p>"
                if issue.line_number:
                    html += f"<small>Linha: {issue.line_number}</small>"
                html += "</li>"
            html += "</ul>"
            html += "</div>"
        
        html += "</div>"
        return html


# =================================================================
# EXEMPLO DE USO (TESTES)
# =================================================================

if __name__ == "__main__":
    # Teste básico do plugin
    plugin = [NomeDaLinguagem]Plugin()
    
    # Código de exemplo
    test_code = """
    // Código de teste aqui
    """
    
    # Executar análise
    result = plugin.analyze(test_code, "linguagem1")
    
    # Imprimir resultados
    print(f"Quality Score: {result.quality_score}")
    print(f"Issues: {len(result.issues)}")
    print(f"Readability: {result.metrics.readability}")
    print(f"\nRecomendações:")
    for rec in result.recommendations:
        print(f"- {rec}")
