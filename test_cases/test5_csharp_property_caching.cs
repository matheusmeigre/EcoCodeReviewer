// TESTE 5: C# - Property Caching (acesso repetido em loop)
// Expectativa: Deve detectar acesso a .Count em condição de loop

public class DataProcessor {
    public void ProcessData(List<int> lista) {
        for (int i = 0; i < lista.Count; i++) {
            Console.WriteLine(lista[i]);
        }
    }
    
    public int SomaElementos(List<int> numeros) {
        int soma = 0;
        for (int i = 0; i < numeros.Count; i++) {
            soma += numeros[i];
        }
        return soma;
    }
    
    public void FiltraLista(List<string> items) {
        for (int j = 0; j < items.Count; j++) {
            if (items[j].Length > 10) {
                Console.WriteLine(items[j]);
            }
        }
    }
}
