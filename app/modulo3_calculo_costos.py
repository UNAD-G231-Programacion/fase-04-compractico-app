"""
MÓDULO 3 - CÁLCULO DE COSTOS (Software FJ)
===========================================
Implementa los métodos de cálculo de costo en sus cuatro variantes:
  - Costo base
  - Costo con impuestos
  - Costo con descuentos
  - Costo combinado (impuestos + descuentos)

Cada variante tiene su propio método, facilitando la integración
con los módulos de servicios y reservas.
Incluye validaciones y excepción personalizada.
"""

# ---------- EXCEPCIÓN PERSONALIZADA ----------
class ErrorCalculo(Exception):
    """Se lanza cuando los datos de entrada para el cálculo son inválidos."""
    pass


# ---------- CLASE CALCULADORA ----------
class CalculadoraCostos:
    """
    Ofrece las cuatro variantes de cálculo mediante métodos independientes.
    """

    @staticmethod
    def costo_base(costo):
        """
        Retorna el costo sin impuestos ni descuentos.
        Parámetro:
            costo (float): Costo base > 0.
        Lanza:
            ErrorCalculo si costo <= 0.
        """
        if costo <= 0:
            raise ErrorCalculo("El costo base debe ser mayor que cero.")
        return costo

    @staticmethod
    def costo_con_impuesto(costo, tasa_impuesto):
        """
        Retorna el costo sumándole el impuesto.
        Parámetros:
            costo (float): Costo base > 0.
            tasa_impuesto (float): Tasa en tanto por uno (0 < tasa <= 1).
        Lanza:
            ErrorCalculo si los parámetros son inválidos.
        """
        if costo <= 0:
            raise ErrorCalculo("El costo base debe ser mayor que cero.")
        if not (0 < tasa_impuesto <= 1):
            raise ErrorCalculo("La tasa de impuesto debe estar entre 0 y 1 (excluyendo 0).")
        return round(costo + costo * tasa_impuesto, 2)

    @staticmethod
    def costo_con_descuento(costo, tasa_descuento):
        """
        Retorna el costo restando el descuento.
        Parámetros:
            costo (float): Costo base > 0.
            tasa_descuento (float): Tasa en tanto por uno (0 < tasa <= 1).
        Lanza:
            ErrorCalculo si los parámetros son inválidos o el resultado es negativo.
        """
        if costo <= 0:
            raise ErrorCalculo("El costo base debe ser mayor que cero.")
        if not (0 < tasa_descuento <= 1):
            raise ErrorCalculo("La tasa de descuento debe estar entre 0 y 1 (excluyendo 0).")
        resultado = costo - costo * tasa_descuento
        if resultado < 0:
            raise ErrorCalculo("El descuento aplicado supera el costo total, resultado negativo.")
        return round(resultado, 2)

    @staticmethod
    def costo_combinado(costo, tasa_impuesto, tasa_descuento):
        """
        Aplica primero el descuento y luego el impuesto sobre el costo base.
        Parámetros:
            costo (float): Costo base > 0.
            tasa_impuesto (float): 0 < tasa <= 1.
            tasa_descuento (float): 0 < tasa <= 1.
        Lanza:
            ErrorCalculo si parámetros inválidos o resultado negativo.
        """
        if costo <= 0:
            raise ErrorCalculo("El costo base debe ser mayor que cero.")
        if not (0 < tasa_impuesto <= 1):
            raise ErrorCalculo("La tasa de impuesto debe estar entre 0 y 1 (excluyendo 0).")
        if not (0 < tasa_descuento <= 1):
            raise ErrorCalculo("La tasa de descuento debe estar entre 0 y 1 (excluyendo 0).")

        # Orden lógico de negocio: descuento primero, luego impuesto
        costo_con_descuento = costo - costo * tasa_descuento
        if costo_con_descuento < 0:
            raise ErrorCalculo("El descuento aplicado supera el costo total.")
        resultado = costo_con_descuento + costo_con_descuento * tasa_impuesto
        return round(resultado, 2)


# ---------- DEMOSTRACIÓN ----------
if __name__ == "__main__":
    print("=" * 60)
    print("MÓDULO DE CÁLCULO DE COSTOS (métodos independientes)\n")

    calc = CalculadoraCostos()

    # 1. Costo base
    try:
        print(f"1. Costo base 100: ${calc.costo_base(100)}")
    except ErrorCalculo as e:
        print(f"1. ERROR: {e}")

    # 2. Costo con impuesto (19%)
    try:
        print(f"2. Costo con impuesto 19%: ${calc.costo_con_impuesto(100, 0.19)}")
    except ErrorCalculo as e:
        print(f"2. ERROR: {e}")

    # 3. Costo con descuento (10%)
    try:
        print(f"3. Costo con descuento 10%: ${calc.costo_con_descuento(100, 0.10)}")
    except ErrorCalculo as e:
        print(f"3. ERROR: {e}")

    # 4. Costo combinado (descuento 10% + impuesto 19%)
    try:
        print(f"4. Costo combinado (10% dto. + 19% IVA): ${calc.costo_combinado(100, 0.19, 0.10)}")
    except ErrorCalculo as e:
        print(f"4. ERROR: {e}")

    # --- Validaciones ---
    print("\n--- Manejo de excepciones ---")
    # Costo base inválido
    try:
        calc.costo_base(-50)
    except ErrorCalculo as e:
        print(f"5. Error esperado: {e}")

    # Tasa de impuesto inválida
    try:
        calc.costo_con_impuesto(100, 1.5)
    except ErrorCalculo as e:
        print(f"6. Error esperado: {e}")

    # Tasa de descuento inválida
    try:
        calc.costo_con_descuento(100, 0)
    except ErrorCalculo as e:
        print(f"7. Error esperado: {e}")

    # Descuento excesivo
    try:
        calc.costo_con_descuento(50, 1.2)
    except ErrorCalculo as e:
        print(f"8. Error esperado: {e}")

    # Combinado con descuento excesivo
    try:
        calc.costo_combinado(100, 0.19, 1.5)
    except ErrorCalculo as e:
        print(f"9. Error esperado: {e}")

    print("\n" + "=" * 60)
    print("El sistema permanece estable. Todas las variantes listas para integración.")