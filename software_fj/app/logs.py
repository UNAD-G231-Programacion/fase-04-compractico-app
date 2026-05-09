# ── MÓDULO 5: SISTEMA DE LOGS Y SIMULACIÓN INTEGRAL ─────────────
# Autor: Leonel Pantoja

# Descripción:
# Este módulo realiza una simulación integral del sistema de gestión
# de clientes, servicios y reservas. Incluye manejo de errores,
# registro en archivo de logs y pruebas con operaciones válidas e inválidas.
#
# Nota:
# Las clases auxiliares incluidas en este archivo permiten ejecutar
# la simulación de forma independiente. En la integración final del proyecto,
# estas clases pueden reemplazarse por las clases oficiales desarrolladas
# en los demás módulos del grupo.
# ────────────────────────────────────────────────────────────────

import logging
import os

# Importación de las clases oficiales del sistema
from entidades_base import Cliente
from servicios import (Servicio, AdminServicios, admin_servicios,
                       ReservaSala, AlquilerEquipo, AsesoriaEspecializada)
from calculos import CalculadoraCostos, ErrorCalculo
from reservas import Reserva, ReservaError, EstadoReservaError

# ── CONFIGURACIÓN DEL SISTEMA DE LOGS ───────────────────────────

# Crear carpeta 'logs' si no existe
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/sistema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# ── FUNCIONES DE REGISTRO ───────────────────────────────────────


def registrar_error(mensaje, error):
    """Muestra el error en consola y lo guarda en el archivo de logs."""
    print(mensaje, error)
    logging.error(f"{mensaje} {error}")


def registrar_evento(mensaje):
    """Muestra un evento en consola y lo guarda en el archivo de logs."""
    print(mensaje)
    logging.info(mensaje)


# ── SIMULACIÓN INTEGRAL DEL SISTEMA ─────────────────────────────
def simulacion_integral():
    """
    Ejecuta la simulación integral del sistema con las clases oficiales.
    Demuestra el registro de clientes, servicios y reservas válidas e inválidas,
    garantizando la estabilidad del programa ante errores.
    """
    print("\n" + "=" * 60)
    print("SIMULACIÓN INTEGRAL DEL SISTEMA")
    print("=" * 60)

    # Para manejar IDs de servicios (se usará el repositorio global)
    servicios_dict = admin_servicios.servicios

    # ── 1. REGISTRO DE SERVICIOS VÁLIDOS ────────────────────────
    try:
        registrar_evento("\n>> Registrando servicios válidos...")
        s1 = ReservaSala(150000, 19, 10, servicios_dict)
        s2 = AlquilerEquipo(80000, 19, 5, servicios_dict)
        s3 = AsesoriaEspecializada(250000, 0, 15, servicios_dict)

        admin_servicios.agregar_servicio(s1)
        admin_servicios.agregar_servicio(s2)
        admin_servicios.agregar_servicio(s3)

        print(s1.mostrar_info())
        print(
            f"Costo final (IVA+Desc): ${s1.calcular_costo_servicio(iva_ok=True, disc_ok=True)}\n")

        print(s2.mostrar_info())
        print(
            f"Costo final (IVA+Desc): ${s2.calcular_costo_servicio(iva_ok=True, disc_ok=True)}\n")

        print(s3.mostrar_info())
        print(
            f"Costo final (IVA+Desc): ${s3.calcular_costo_servicio(iva_ok=True, disc_ok=True)}\n")

    except Exception as e:
        registrar_error("Error al registrar servicios:", e)
    else:
        registrar_evento("Servicios registrados correctamente.")
    finally:
        registrar_evento("Finalizó la simulación de servicios válidos.")

    # ── 2. SERVICIO INVÁLIDO (COSTO NEGATIVO) ───────────────────
    try:
        registrar_evento("\n>> Probando servicio con costo negativo...")
        s_err = ReservaSala(-50000, 19, 10, servicios_dict)
    except Exception as e:
        registrar_error("Servicio inválido detectado:", e)

    # ── 3. CLIENTES VÁLIDOS ─────────────────────────────────────
    try:
        registrar_evento("\n>> Registrando clientes válidos...")
        c1 = Cliente("1", "Carlos Pérez", "carlos@mail.com", "3001112233")
        c2 = Cliente("2", "Laura Gómez", "laura@mail.com", "3104445566")
        Cliente.agregar_cliente(c1)
        Cliente.agregar_cliente(c2)
        print(c1.describir())
        print(c2.describir())
    except Exception as e:
        registrar_error("Error al registrar clientes:", e)
    else:
        registrar_evento("Clientes registrados correctamente.")
    finally:
        registrar_evento("Finalizó la simulación de clientes válidos.")

    # ── 4. CLIENTE INVÁLIDO (NOMBRE CORTO) ──────────────────────
    try:
        registrar_evento("\n>> Probando cliente con nombre inválido...")
        c_err = Cliente("3", "AB", "mal@mail.com", "1234567")
    except Exception as e:
        registrar_error("Cliente inválido detectado:", e)

    # ── 5. RESERVAS VÁLIDAS ─────────────────────────────────────
    try:
        registrar_evento("\n>> Creando reservas válidas...")
        # Asegurar clientes registrados previamente
        c1 = Cliente.buscar_cliente("1")
        c2 = Cliente.buscar_cliente("2")

        r1 = Reserva(c1, s1, 2)
        r2 = Reserva(c2, s2, 1)

        r1.confirmar()
        r2.confirmar()
        r1.procesar()
        r2.cancelar()
    except Exception as e:
        registrar_error("Error en reservas:", e)
    else:
        registrar_evento("Reservas procesadas correctamente.")
    finally:
        registrar_evento("Finalizó la simulación de reservas válidas.")

    # ── 6. RESERVA INVÁLIDA POR CLIENTE NULO ────────────────────
    try:
        registrar_evento("\n>> Probando reserva con cliente nulo...")
        r_err = Reserva(None, s1, 2)
    except Exception as e:
        registrar_error("Reserva inválida (cliente nulo):", e)

    # ── 7. RESERVA INVÁLIDA POR DURACIÓN NEGATIVA ───────────────
    try:
        registrar_evento("\n>> Probando reserva con duración negativa...")
        c_temp = Cliente("10", "Pedro Ruiz", "pedro@mail.com", "3009988776")
        Cliente.agregar_cliente(c_temp)
        r_err = Reserva(c_temp, s1, -5)
    except Exception as e:
        registrar_error("Reserva inválida (duración negativa):", e)

    # ── 8. RESERVA INVÁLIDA POR SERVICIO NULO ───────────────────
    try:
        registrar_evento("\n>> Probando reserva con servicio nulo...")
        c_temp2 = Cliente("11", "Ana León", "ana@mail.com", "3116655443")
        Cliente.agregar_cliente(c_temp2)
        r_err = Reserva(c_temp2, None, 3)
    except Exception as e:
        registrar_error("Reserva inválida (servicio nulo):", e)

    # ── 9. CANCELACIÓN NO PERMITIDA (RESERVA YA PROCESADA) ──────
    try:
        registrar_evento(
            "\n>> Probando cancelación de reserva ya procesada...")
        c3 = Cliente("3", "Miguel Torres", "miguel@mail.com", "3204455667")
        Cliente.agregar_cliente(c3)
        r3 = Reserva(c3, s3, 4)
        r3.confirmar()
        r3.procesar()
        r3.cancelar()   # Esto debe lanzar EstadoReservaError
    except Exception as e:
        registrar_error("Cancelación no permitida detectada:", e)
    finally:
        registrar_evento("Finalizó prueba de cancelación inválida.")

    # ── 10. MOSTRAR TODAS LAS RESERVAS ──────────────────────────
    try:
        registrar_evento("\n>> Lista final de reservas registradas:")
        Reserva.mostrar_reservas()
    except Exception as e:
        registrar_error("Error al mostrar reservas:", e)

    print("\n" + "=" * 60)
    print("EL SISTEMA CONTINÚA FUNCIONANDO CORRECTAMENTE")
    print("=" * 60)


# ── EJECUCIÓN DEL PROGRAMA ──────────────────────────────────────

if __name__ == "__main__":
    simulacion_integral()
