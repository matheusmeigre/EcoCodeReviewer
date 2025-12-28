"""
Core Review Engine - FASE 2
Orquestrador central do sistema de análise
"""
import logging
from typing import Dict, List, Optional, Type
from datetime import datetime
import json

from review_engine.core.dto import ReviewResult, DetectionResult
from review_engine.detectors.language_detector import LanguageDetector
from review_engine.plugins.base_plugin import BasePlugin, UniversalPlugin
from review_engine.ai_layer.groq_adapter import GroqAdapter


logger = logging.getLogger(__name__)


class ReviewEngine:
    """
    Motor de análise modular baseado em plugins
    Segue padrão Strategy Pattern para seleção de analisadores
    """
    
    def __init__(self, groq_api_key: Optional[str] = None):
        self.detector = LanguageDetector()
        self.plugins: Dict[str, BasePlugin] = {}
        self.universal_plugin = UniversalPlugin()
        self.ai_adapter = GroqAdapter(groq_api_key) if groq_api_key else None
        
        # Sistema de auditabilidade (FASE 6)
        self.audit_log = []
        
        # Registrar plugins automaticamente
        self._register_plugins()
        
        logger.info(f"ReviewEngine inicializado com {len(self.plugins)} plugins")
    
    def _register_plugins(self):
        """
        Carrega e registra todos os plugins disponíveis
        Auto-discovery via importação dinâmica
        """
        # Importação manual dos plugins implementados
        try:
            from ..plugins.python.python_plugin import PythonPlugin
            self.register_plugin(PythonPlugin())
        except ImportError:
            logger.warning("PythonPlugin não encontrado")
        
        try:
            from ..plugins.javascript.javascript_plugin import JavaScriptPlugin
            self.register_plugin(JavaScriptPlugin())
        except ImportError:
            logger.warning("JavaScriptPlugin não encontrado")
        
        # Novos plugins - FASE 3 expansão
        try:
            from ..plugins.go.go_plugin import GoPlugin
            self.register_plugin(GoPlugin())
        except ImportError:
            logger.warning("GoPlugin não encontrado")
        
        try:
            from ..plugins.rust.rust_plugin import RustPlugin
            self.register_plugin(RustPlugin())
        except ImportError:
            logger.warning("RustPlugin não encontrado")
        
        try:
            from ..plugins.php.php_plugin import PHPPlugin
            self.register_plugin(PHPPlugin())
        except ImportError:
            logger.warning("PHPPlugin não encontrado")
        
        try:
            from ..plugins.ruby.ruby_plugin import RubyPlugin
            self.register_plugin(RubyPlugin())
        except ImportError:
            logger.warning("RubyPlugin não encontrado")
        
        try:
            from ..plugins.frontend.vue_plugin import VuePlugin
            self.register_plugin(VuePlugin())
        except ImportError:
            logger.warning("VuePlugin não encontrado")
        
        try:
            from ..plugins.frontend.angular_plugin import AngularPlugin
            self.register_plugin(AngularPlugin())
        except ImportError:
            logger.warning("AngularPlugin não encontrado")
        
        try:
            from ..plugins.frontend.svelte_plugin import SveltePlugin
            self.register_plugin(SveltePlugin())
        except ImportError:
            logger.warning("SveltePlugin não encontrado")
        
        # Plugins mobile - FASE 3 expansão
        try:
            from ..plugins.kotlin.kotlin_plugin import KotlinPlugin
            self.register_plugin(KotlinPlugin())
        except ImportError:
            logger.warning("KotlinPlugin não encontrado")
        
        try:
            from ..plugins.swift.swift_plugin import SwiftPlugin
            self.register_plugin(SwiftPlugin())
        except ImportError:
            logger.warning("SwiftPlugin não encontrado")
        
        # Plugins infraestrutura - FASE 3 expansão
        try:
            from ..plugins.infra.bash_plugin import BashPlugin
            self.register_plugin(BashPlugin())
        except ImportError:
            logger.warning("BashPlugin não encontrado")
        
        try:
            from ..plugins.infra.yaml_plugin import YAMLPlugin
            self.register_plugin(YAMLPlugin())
        except ImportError:
            logger.warning("YAMLPlugin não encontrado")
        
        try:
            from ..plugins.infra.dockerfile_plugin import DockerfilePlugin
            self.register_plugin(DockerfilePlugin())
        except ImportError:
            logger.warning("DockerfilePlugin não encontrado")
        
        try:
            from ..plugins.infra.terraform_plugin import TerraformPlugin
            self.register_plugin(TerraformPlugin())
        except ImportError:
            logger.warning("TerraformPlugin não encontrado")
        
        # Registrar plugin universal
        self.register_plugin(self.universal_plugin)
    
    def register_plugin(self, plugin: BasePlugin):
        """Registra um plugin no engine"""
        for language in plugin.get_supported_languages():
            self.plugins[language] = plugin
            logger.info(f"Plugin {plugin.name} registrado para {language}")
    
    def analyze(self, 
                code: str, 
                language: str = "auto",
                filename: Optional[str] = None,
                use_ai: bool = True) -> ReviewResult:
        """
        Executa análise completa do código
        
        Args:
            code: Código-fonte a ser analisado
            language: Linguagem (ou 'auto' para detecção)
            filename: Nome do arquivo (ajuda na detecção)
            use_ai: Se True, usa AI para análise semântica
        
        Returns:
            ReviewResult padronizado
        """
        start_time = datetime.now()
        
        # Auto-detecção se necessário
        detection_result = None
        if language == "auto":
            detection_result = self.detector.detect(code, filename)
            language = detection_result.language
            
            logger.info(f"Linguagem detectada: {language} "
                       f"(confiança: {detection_result.confidence}%)")
            
            # Fallback manual se confiança baixa
            if detection_result.fallback_required:
                logger.warning("Confiança baixa na detecção. Requer seleção manual.")
                return ReviewResult(
                    language="unknown",
                    quality_score=0,
                    confidence_level=detection_result.confidence,
                    explanation="Não foi possível detectar a linguagem com confiança. "
                               "Por favor, selecione manualmente."
                )
        
        # Selecionar plugin apropriado
        plugin = self.plugins.get(language)
        if not plugin and language != "*":
            # Fallback para plugin universal
            plugin = self.universal_plugin
            logger.info(f"Plugin específico não encontrado para {language}. "
                       f"Usando UniversalPlugin.")
        
        # Executar análise do plugin
        result = plugin.analyze(code, language) if plugin else None
        
        # Análise com AI (se habilitada e disponível)
        if use_ai and self.ai_adapter:
            try:
                ai_result = self.ai_adapter.analyze(code, language)
                # Mesclar resultados AI com análise do plugin
                result = self._merge_results(result, ai_result)
            except Exception as e:
                logger.error(f"Erro na análise AI: {e}")
        
        # Adicionar informações de detecção
        if detection_result:
            result.confidence_level = detection_result.confidence
        
        # Auditoria (FASE 6)
        self._log_analysis(
            code=code,
            language=language,
            result=result,
            duration=(datetime.now() - start_time).total_seconds()
        )
        
        return result
    
    def _merge_results(self, plugin_result: ReviewResult, 
                       ai_result: ReviewResult) -> ReviewResult:
        """
        Mescla resultados da análise de plugin com análise AI
        Plugin fornece regras estruturadas, AI fornece contexto semântico
        """
        if not plugin_result:
            return ai_result
        
        if not ai_result:
            return plugin_result
        
        # Priorizar código otimizado da AI
        plugin_result.optimized_code = ai_result.optimized_code or plugin_result.optimized_code
        plugin_result.explanation = ai_result.explanation or plugin_result.explanation
        plugin_result.explanation_html = ai_result.explanation_html
        
        # Combinar issues (sem duplicatas)
        all_issues = plugin_result.issues + ai_result.issues
        plugin_result.issues = all_issues
        
        # Recalcular quality score
        if ai_result.quality_score:
            plugin_result.quality_score = (plugin_result.quality_score + ai_result.quality_score) // 2
        
        # Priorizar métricas da AI (mais detalhadas)
        if ai_result.metrics:
            plugin_result.metrics = ai_result.metrics
        
        plugin_result.has_issues = len(plugin_result.issues) > 0
        
        return plugin_result
    
    def _log_analysis(self, code: str, language: str, 
                      result: ReviewResult, duration: float):
        """
        Sistema de auditabilidade (FASE 6)
        Registra decisões e resultados para rastreabilidade
        """
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "language": language,
            "code_length": len(code),
            "quality_score": result.quality_score,
            "issues_count": len(result.issues),
            "confidence_level": result.confidence_level,
            "duration_seconds": duration,
            "plugin_used": result.language,
            "version": "2.0.0"
        }
        
        self.audit_log.append(audit_entry)
        logger.debug(f"Análise auditada: {json.dumps(audit_entry)}")
    
    def get_supported_languages(self) -> List[str]:
        """Retorna todas as linguagens suportadas"""
        return self.detector.get_supported_languages()
    
    def get_plugin_info(self) -> Dict[str, dict]:
        """Retorna informações de todos os plugins registrados"""
        return {
            lang: plugin.get_plugin_info()
            for lang, plugin in self.plugins.items()
        }
    
    def export_audit_log(self, filepath: Optional[str] = None) -> List[dict]:
        """
        Exporta log de auditoria (FASE 6)
        Útil para análise de uso e feedback
        """
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.audit_log, f, indent=2, ensure_ascii=False)
        
        return self.audit_log
