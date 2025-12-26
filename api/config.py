"""
Módulo de configuração centralizado.
"""
import os

# Carregar variáveis de ambiente
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '').strip()
GROQ_MODEL = os.environ.get('GROQ_MODEL', 'llama-3.3-70b-versatile')
GROQ_TEMPERATURE = float(os.environ.get('GROQ_TEMPERATURE', '0.3'))
GROQ_MAX_TOKENS = int(os.environ.get('GROQ_MAX_TOKENS', '2000'))

# Debug
print(f"\n{'='*60}")
print("CONFIG MODULE - Variáveis carregadas:")
print(f"  GROQ_API_KEY length: {len(GROQ_API_KEY)}")
print(f"  GROQ_API_KEY empty: {not GROQ_API_KEY}")
if GROQ_API_KEY:
    print(f"  Preview: {GROQ_API_KEY[:10]}...{GROQ_API_KEY[-4:]}")
print(f"  GROQ_MODEL: {GROQ_MODEL}")
print(f"{'='*60}\n")

# Inicializar cliente Groq
client = None
if GROQ_API_KEY and len(GROQ_API_KEY) > 10:
    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)
        print("✓ Cliente Groq inicializado com sucesso!")
    except Exception as e:
        print(f"Erro ao criar cliente Groq: {e}")
        client = None
else:
    print("⚠️ GROQ_API_KEY não configurada!")
