"""
Eco-Code Reviewer v4.0 → v2.0 Engine Integration
========================================================
Arquitetura Modular com Sistema de Plugins (Roadmap FASE 1-6)

Nova estrutura:
- review-engine/: Motor modular de análise
- Sistema de plugins por linguagem
- Auto-detecção refinada com níveis de confiança
- Auditoria e rastreabilidade completa

Mantém compatibilidade total com frontend existente
"""

import os
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

# Importar novo Review Engine v2.0
from review_engine.core import ReviewEngine

# Configuração de logging estruturado
logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"}',
    datefmt='%Y-%m-%dT%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

# Inicializar Flask
app = Flask(__name__)
CORS(app)

# Configurações
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# Inicializar Review Engine v2.0
review_engine = ReviewEngine(groq_api_key=GROQ_API_KEY)

# Banner de inicialização
print("=" * 70)
print("🚀 Eco-Code Reviewer v2.0 - MODULAR ARCHITECTURE ENGINE")
print("=" * 70)
print(f"📊 URL: http://localhost:{PORT}")
print(f"🤖 Motor: Review Engine v2.0 (Plugin-based)")
print(f"🔑 API Status: {'✅ Configured' if GROQ_API_KEY else '❌ Not configured'}")
print(f"🎯 Plugins Registrados: {list(review_engine.plugins.keys())}")
print(f"🌍 Linguagens Suportadas: {len(review_engine.get_supported_languages())}")
print(f"🌱 Foco: Green IT + Performance Optimization")
print("=" * 70)


@app.route('/')
def index():
    """Renderiza frontend"""
    return render_template('index.html')


@app.route('/health', methods=['GET'])
def health_check():
    """
    Healthcheck com informações do engine
    Compatível com frontend existente
    """
    return jsonify({
        'status': 'healthy',
        'version': '2.0.0',
        'engine': 'review-engine-modular',
        'model': 'llama-3.3-70b-versatile',
        'api_status': 'configured' if GROQ_API_KEY else 'not_configured',
        'plugins': list(review_engine.plugins.keys()),
        'supported_languages': review_engine.get_supported_languages()
    })


@app.route('/analyze', methods=['POST'])
def analyze_code():
    """
    Endpoint principal de análise
    INTEGRADO com novo Review Engine v2.0
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'JSON inválido'
            }), 400
        
        code = data.get('code', '').strip()
        language = data.get('language', 'auto').lower()
        filename = data.get('filename')  # Novo: ajuda na detecção
        
        if not code:
            return jsonify({
                'success': False,
                'error': 'Código não fornecido'
            }), 400
        
        logger.info(f"Análise iniciada - Linguagem: {language}, Tamanho: {len(code)} chars")
        
        # Executar análise usando Review Engine v2.0
        result = review_engine.analyze(
            code=code,
            language=language,
            filename=filename,
            use_ai=True
        )
        
        # Converter ReviewResult para formato compatível com frontend
        response = {
            'success': True,
            'data': result.to_dict(),
            'model': 'review-engine-v2.0',
            'tokens': 0  # Placeholder - pode ser calculado futuramente
        }
        
        # Log estruturado para auditoria
        logger.info(f"Análise concluída - Score: {result.quality_score}, "
                   f"Issues: {len(result.issues)}, "
                   f"Confiança: {result.confidence_level}%")
        
        return jsonify(response)
    
    except Exception as e:
        logger.error(f"Erro na análise: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500


@app.route('/detect', methods=['POST'])
def detect_language():
    """
    Novo endpoint: Detecção isolada de linguagem
    Expõe nível de confiança para o frontend
    """
    try:
        data = request.get_json()
        code = data.get('code', '').strip()
        filename = data.get('filename')
        
        if not code:
            return jsonify({
                'success': False,
                'error': 'Código não fornecido'
            }), 400
        
        detection = review_engine.detector.detect(code, filename)
        
        return jsonify({
            'success': True,
            'data': detection.to_dict()
        })
    
    except Exception as e:
        logger.error(f"Erro na detecção: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/plugins', methods=['GET'])
def list_plugins():
    """
    Novo endpoint: Lista plugins registrados
    Útil para debugging e dashboard
    """
    try:
        plugins_info = review_engine.get_plugin_info()
        
        return jsonify({
            'success': True,
            'plugins': plugins_info,
            'total': len(plugins_info)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/audit/export', methods=['GET'])
def export_audit_log():
    """
    Novo endpoint: Exporta log de auditoria (FASE 6)
    Formato JSON para análise de uso
    """
    try:
        audit_log = review_engine.export_audit_log()
        
        return jsonify({
            'success': True,
            'total_analyses': len(audit_log),
            'log': audit_log
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint não encontrado'}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Erro 500: {error}")
    return jsonify({'error': 'Erro interno do servidor'}), 500


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=DEBUG
    )
