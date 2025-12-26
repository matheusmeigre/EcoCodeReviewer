# TESTE EXTRA: Código Python PERFEITO
# Expectativa: Score 100, mensagem "Parabéns! Nenhuma ineficiência detectada"

def processar_dados(dados):
    """Função otimizada usando built-ins e list comprehension"""
    # Usa sum() ao invés de loop manual
    total = sum(dados)
    
    # List comprehension ao invés de append em loop
    pares = [x for x in dados if x % 2 == 0]
    
    # Usa set para busca O(1) ao invés de 'in' em lista
    unicos = set(dados)
    
    return {
        'total': total,
        'pares': pares,
        'quantidade_unicos': len(unicos)
    }

# Uso
resultado = processar_dados([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(resultado)
