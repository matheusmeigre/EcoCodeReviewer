#!/usr/bin/env python3
"""
Script para injetar variáveis de ambiente na Vercel.
Executado antes do build.
"""
import os
import sys

print("=" * 60)
print("🔍 VERCEL ENV VARS CHECK")
print("=" * 60)

# Verificar todas as variáveis GROQ
groq_vars = {k: v for k, v in os.environ.items() if 'GROQ' in k}

if groq_vars:
    print("✓ Variáveis GROQ encontradas:")
    for key, value in groq_vars.items():
        preview = f"{value[:10]}...{value[-4:]}" if len(value) > 14 else "***"
        print(f"  - {key}: {preview}")
else:
    print("✗ NENHUMA variável GROQ encontrada!")
    print(f"✗ Todas as env vars: {list(os.environ.keys())}")
    sys.exit(1)

print("=" * 60)
