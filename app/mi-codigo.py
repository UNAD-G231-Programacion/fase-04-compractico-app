class CalculadoraBasica:
    """
    Una clase muy básica para realizar operaciones matemáticas simples:
    suma, resta y multiplicación.
    """

    def sumar(self, a, b):
        """
        Suma dos números y devuelve el resultado.
        """
        # Se calcula y se devuelve la suma de a y b
        return a + b

    def restar(self, a, b):
        """
        Resta el segundo número (b) al primero (a) y devuelve el resultado.
        """
        # Se calcula y se devuelve la diferencia entre a y b
        return a - b

    def multiplicar(self, a, b):
        """
        Multiplica dos números y devuelve el resultado.
        """
        # Se calcula y se devuelve el producto de a y b
        return a * b

# ==========================================
# SECCIÓN DE PRUEBAS
# ==========================================


# Este bloque asegura que las pruebas solo se ejecuten si corres este archivo directamente
if __name__ == "__main__":

    # 1. Creamos una instancia (un objeto) de nuestra clase
    mi_calculadora = CalculadoraBasica()

    # 2. Definimos un par de números para hacer las pruebas
    numero_1 = 10
    numero_2 = 5

    print("--- Iniciando pruebas de CalculadoraBasica ---\n")

    # 3. Probamos el método sumar
    resultado_suma = mi_calculadora.sumar(numero_1, numero_2)
    print(f"La suma de {numero_1} y {numero_2} es: {resultado_suma}")

    # 4. Probamos el método restar
    resultado_resta = mi_calculadora.restar(numero_1, numero_2)
    print(f"La resta de {numero_1} menos {numero_2} es: {resultado_resta}")

    # 5. Probamos el método multiplicar
    resultado_multiplicacion = mi_calculadora.multiplicar(numero_1, numero_2)
    print(
        f"La multiplicación de {numero_1} por {numero_2} es: {resultado_multiplicacion}")

    print("\n--- Pruebas finalizadas ---")
