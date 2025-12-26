// TESTE 3: Java - Dead Code / Variável Inútil
// Expectativa: Deve detectar variável intermediária desnecessária

public class Calculator {
    public int soma(int a, int b) {
        int resultado = a + b;
        return resultado;
    }
    
    public double divide(double x, double y) {
        double divisao = x / y;
        return divisao;
    }
    
    public String concatena(String s1, String s2) {
        String juncao = s1 + s2;
        return juncao;
    }
}
