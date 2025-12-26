# TESTE 1B: Python - Loop Manual com range(len()) vs sum()
# Caso reportado pelo usuário
# Expectativa: Deve detectar e otimizar para sum()

lista = [10, 20, 30, 40, 50]

soma = 0
for i in range(0, len(lista)):
    soma += lista[i]

print(soma)
