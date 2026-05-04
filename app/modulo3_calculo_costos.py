"""
MÓDULO 3 - CÁLCULO DE COSTOS (Software FJ)
===========================================
Implementa los métodos sobrecargados de cálculo de costo en sus cuatro variantes:
  1. Costo base
  2. Costo con impuestos
  3. Costo con descuentos
  4. Costo combinado (impuestos + descuentos)

Incluye validaciones y excepciones personalizadas del módulo.
"""

# ---------- EXCEPCIÓN PERSONALIZADA ----------
class ErrorCalculo(Exception):
    """Excepción lanzada cuando ocurre un error en los cálculos de costo."""
    pass


# ---------- CLASE CALCULADORA ----------
class CalculadoraCostos:
    """
    Calcula el costo de un servicio según variantes de parámetros.
    La sobrecarga se simula mediante parámetros con valores por defecto.
    """

    def calcular_costo(self, costo_base, *,
                       aplicar_impuesto=False, tasa_impuesto=0.0,
                       aplicar_descuento=False, tasa_descuento=0.0):
        """
        Calcula el costo final según los flags activados.

        Parámetros:
            costo_base (float): Costo inicial > 0.
            aplicar_impuesto (bool): Si se suma el impuesto.
            tasa_impuesto (float): Tasa en tanto por uno (ej. 0.19).
            aplicar_descuento (bool): Si se resta el descuento.
            tasa_descuento (float): Tasa en tanto por uno (ej. 0.10).

        Retorna:
            float: Costo redondeado a dos decimales.

        Lanza:
            ErrorCalculo: Datos inválidos o cálculo inconsistente.
        """
        # --- Validaciones de parámetros ---
        if costo_base <= 0:
            raise ErrorCalculo("El costo base debe ser mayor que cero.")

        if aplicar_impuesto:
            if tasa_impuesto <= 0:
                raise ErrorCalculo("La tasa de impuesto debe ser > 0 si se aplica.")
            if tasa_impuesto > 1:
                raise ErrorCalculo("La tasa de impuesto no puede superar el 100%.")

        if aplicar_descuento:
            if tasa_descuento <= 0:
                raise ErrorCalculo("La tasa de descuento debe ser > 0 si se aplica.")
            if tasa_descuento > 1:
                raise ErrorCalculo("La tasa de descuento no puede superar el 100%.")

        # --- Cálculo ---
        costo = costo_base
        if aplicar_impuesto:
            costo += costo_base * tasa_impuesto
        if aplicar_descuento:
            costo -= costo_base * tasa_descuento

        if costo < 0:
            raise ErrorCalculo("El descuento aplicado supera el costo total, resultado negativo.")

        return round(costo, 2)


# ---------- DEMOSTRACIÓN DE USO ----------
if __name__ == "__main__":
    calc = CalculadoraCostos()
    print("=" * 60)
    print("DEMOSTRACIÓN DEL MÓDULO DE CÁLCULO DE COSTOS\n")

    # 1. COSTO BASE (sin impuestos ni descuentos)
    try:
        resultado = calc.calcular_costo(100)
        print(f"1. Costo base (100): ${resultado}")
    except ErrorCalculo as e:
        print(f"1. ERROR: {e}")

    # 2. COSTO CON IMPUESTOS (19% IVA)
    try:
        resultado = calc.calcular_costo(100, aplicar_impuesto=True, tasa_impuesto=0.19)
        print(f"2. Costo con impuesto 19%: ${resultado}")
    except ErrorCalculo as e:
        print(f"2. ERROR: {e}")

    # 3. COSTO CON DESCUENTO (10%)
    try:
        resultado = calc.calcular_costo(100, aplicar_descuento=True, tasa_descuento=0.10)
        print(f"3. Costo con descuento 10%: ${resultado}")
    except ErrorCalculo as e:
        print(f"3. ERROR: {e}")

    # 4. COSTO COMBINADO (impuesto 19% + descuento 10%)
    try:
        resultado = calc.calcular_costo(100,
                                        aplicar_impuesto=True, tasa_impuesto=0.19,
                                        aplicar_descuento=True, tasa_descuento=0.10)
        print(f"4. Costo combinado (19% IVA + 10% dto.): ${resultado}")
    except ErrorCalculo as e:
        print(f"4. ERROR: {e}")

    # --- PRUEBAS DE MANEJO DE ERRORES ---
    print("\n--- Validaciones y excepciones ---")

    # Error: costo base negativo
    try:
        calc.calcular_costo(-50)
    except ErrorCalculo as e:
        print(f"5. Error esperado: {e}")

    # Error: aplicar impuesto con tasa 0
    try:
        calc.calcular_costo(100, aplicar_impuesto=True, tasa_impuesto=0)
    except ErrorCalculo as e:
        print(f"6. Error esperado: {e}")

    # Error: tasa de impuesto > 100%
    try:
        calc.calcular_costo(100, aplicar_impuesto=True, tasa_impuesto=1.5)
    except ErrorCalculo as e:
        print(f"7. Error esperado: {e}")

    # Error: tasa de descuento > 100%
    try:
        calc.calcular_costo(100, aplicar_descuento=True, tasa_descuento=2.0)
    except ErrorCalculo as e:
        print(f"8. Error esperado: {e}")

    # Error: descuento hace el costo negativo
    try:
        calc.calcular_costo(50, aplicar_descuento=True, tasa_descuento=1.2)
    except ErrorCalculo as e:
        print(f"9. Error esperado: {e}")

    # Operación válida extra con valores grandes
    try:
        resultado = calc.calcular_costo(2500, aplicar_impuesto=True, tasa_impuesto=0.08)
        print(f"10. Válido: base 2500 + impuesto 8% = ${resultado}")
    except ErrorCalculo as e:
        print(f"10. ERROR: {e}")

    print("\n" + "=" * 60)
    print("El sistema continúa funcionando sin interrupciones.")