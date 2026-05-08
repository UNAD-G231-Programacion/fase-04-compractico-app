# ── MÓDULO 5: SISTEMA DE LOGS Y SIMULACIÓN INTEGRAL ─────────────
# Autor: Leonel Pantoja
# Curso: Programación - UNAD
#
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


# ── CONFIGURACIÓN DEL SISTEMA DE LOGS ───────────────────────────

logging.basicConfig(
    filename="logs.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)


# ── CLASE BASE PARA SERVICIOS ───────────────────────────────────

class ServicioBase:
    """
    Clase base auxiliar para representar un servicio del sistema.
    Permite calcular costos aplicando descuento e impuesto.
    """

    def __init__(self, costo_base, descuento, impuesto):
        """
        Inicializa un servicio validando que los valores recibidos sean correctos.
        """

        if costo_base <= 0:
            raise ValueError("El costo base debe ser mayor que cero.")

        if descuento < 0:
            raise ValueError("El descuento no puede ser negativo.")

        if impuesto < 0:
            raise ValueError("El impuesto no puede ser negativo.")

        self.costo_base = costo_base
        self.descuento = descuento
        self.impuesto = impuesto

    def calcular_costos(self):
        """
        Calcula el costo final del servicio aplicando descuento e impuesto.
        """

        costo_con_descuento = self.costo_base - (self.costo_base * self.descuento / 100)
        costo_final = costo_con_descuento + (costo_con_descuento * self.impuesto / 100)

        return round(costo_final, 2)

    def mostrar_info(self):
        """
        Muestra la información general del servicio.
        """

        print(f"Tipo de servicio: {self.__class__.__name__}")
        print(f"Costo base: ${self.costo_base}")
        print(f"Descuento: {self.descuento}%")
        print(f"Impuesto: {self.impuesto}%")


# ── SERVICIOS ESPECIALIZADOS ────────────────────────────────────

class ReservaSala(ServicioBase):
    """
    Clase auxiliar que representa el servicio de reserva de salas.
    """
    pass


class AlquilerEquipo(ServicioBase):
    """
    Clase auxiliar que representa el servicio de alquiler de equipos.
    """
    pass


class AsesoriaEspecializada(ServicioBase):
    """
    Clase auxiliar que representa el servicio de asesoría especializada.
    """
    pass


# ── ADMINISTRADOR DE SERVICIOS ──────────────────────────────────

class AdminServicios:
    """
    Clase auxiliar para registrar y almacenar servicios dentro de una lista.
    """

    def __init__(self):
        """
        Inicializa la lista interna de servicios.
        """

        self.servicios = []

    def agregar_servicio(self, servicio):
        """
        Agrega un servicio a la lista, validando que no sea un valor vacío.
        """

        if servicio is None:
            raise ValueError("No se puede agregar un servicio vacío.")

        self.servicios.append(servicio)
        print("Servicio agregado correctamente.")


# Se crea un objeto administrador de servicios para la simulación
admin_servicios = AdminServicios()


# ── CLASE CLIENTE AUXILIAR ──────────────────────────────────────

class Cliente:
    """
    Clase auxiliar para representar un cliente dentro de la simulación.
    """

    def __init__(self, nombre):
        """
        Inicializa un cliente validando que el nombre no esté vacío.
        """

        if nombre is None or nombre.strip() == "":
            raise ValueError("El nombre del cliente no puede estar vacío.")

        self.nombre = nombre


# ── CLASE RESERVA AUXILIAR ──────────────────────────────────────

class Reserva:
    """
    Clase auxiliar para representar una reserva del sistema.
    """

    reservas = []

    def __init__(self, cliente, servicio, duracion):
        """
        Inicializa una reserva validando cliente, servicio y duración.
        """

        if cliente is None:
            raise ValueError("La reserva debe tener un cliente válido.")

        if servicio is None:
            raise ValueError("La reserva debe tener un servicio válido.")

        if duracion <= 0:
            raise ValueError("La duración de la reserva debe ser mayor que cero.")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

        Reserva.reservas.append(self)

    def confirmar(self):
        """
        Confirma una reserva si se encuentra en estado pendiente.
        """

        if self.estado != "Pendiente":
            raise ValueError("Solo se pueden confirmar reservas pendientes.")

        self.estado = "Confirmada"
        print(f"Reserva confirmada para el cliente {self.cliente.nombre}.")

    def procesar(self):
        """
        Procesa una reserva si ya fue confirmada.
        """

        if self.estado != "Confirmada":
            raise ValueError("La reserva debe estar confirmada para poder procesarse.")

        self.estado = "Procesada"
        print(f"Reserva procesada para el cliente {self.cliente.nombre}.")

    def cancelar(self):
        """
        Cancela una reserva siempre que no haya sido procesada.
        """

        if self.estado == "Procesada":
            raise ValueError("No se puede cancelar una reserva ya procesada.")

        self.estado = "Cancelada"
        print(f"Reserva cancelada para el cliente {self.cliente.nombre}.")

    @classmethod
    def mostrar_reservas(cls):
        """
        Muestra todas las reservas registradas en la simulación.
        """

        if not cls.reservas:
            print("No hay reservas registradas.")
            return

        for reserva in cls.reservas:
            print(
                f"Cliente: {reserva.cliente.nombre} | "
                f"Servicio: {reserva.servicio.__class__.__name__} | "
                f"Duración: {reserva.duracion} hora(s) | "
                f"Estado: {reserva.estado}"
            )


# ── FUNCIÓN PARA REGISTRAR ERRORES ──────────────────────────────

def registrar_error(mensaje, error):
    """
    Muestra un mensaje de error en consola y lo registra en el archivo logs.txt.
    """

    print(mensaje, error)
    logging.error(f"{mensaje} {error}")


# ── SIMULACIÓN INTEGRAL DEL SISTEMA ─────────────────────────────

def simulacion_integral():
    """
    Ejecuta la simulación integral del sistema.

    En esta función se prueban servicios válidos e inválidos,
    clientes válidos e inválidos, reservas correctas y reservas fallidas.
    El objetivo es demostrar que el programa continúa funcionando aunque
    se presenten errores durante la ejecución.
    """

    print("\n" + "=" * 60)
    print("SIMULACIÓN INTEGRAL DEL SISTEMA")
    print("=" * 60)

    servicio1 = None
    servicio2 = None
    servicio3 = None

    # ── 1. SIMULACIÓN DE SERVICIOS VÁLIDOS ──────────────────────

    try:
        print("\nRegistrando servicios válidos...\n")

        servicio1 = ReservaSala(150000, 5, 0)
        servicio2 = AlquilerEquipo(80000, 10, 5)
        servicio3 = AsesoriaEspecializada(250000, 0, 15)

        admin_servicios.agregar_servicio(servicio1)
        admin_servicios.agregar_servicio(servicio2)
        admin_servicios.agregar_servicio(servicio3)

        servicio1.mostrar_info()
        print(f"Costo final: ${servicio1.calcular_costos()}\n")

        servicio2.mostrar_info()
        print(f"Costo final: ${servicio2.calcular_costos()}\n")

        servicio3.mostrar_info()
        print(f"Costo final: ${servicio3.calcular_costos()}\n")

    except Exception as e:
        registrar_error("Error al registrar servicios:", e)

    else:
        print("Servicios registrados correctamente.")

    finally:
        print("Finalizó la simulación de servicios válidos.")

    # ── 2. SIMULACIÓN DE SERVICIO INVÁLIDO ──────────────────────

    try:
        print("\nProbando servicio inválido...\n")

        servicio_error = ReservaSala(-50000, 5, 0)

    except Exception as e:
        registrar_error("Servicio inválido detectado correctamente:", e)

    # ── 3. SIMULACIÓN DE CLIENTES VÁLIDOS ───────────────────────

    try:
        print("\nRegistrando clientes válidos...\n")

        cliente1 = Cliente("Carlos")
        cliente2 = Cliente("Laura")

        print(f"Cliente registrado: {cliente1.nombre}")
        print(f"Cliente registrado: {cliente2.nombre}")

    except Exception as e:
        registrar_error("Error al registrar clientes:", e)

    else:
        print("Clientes registrados correctamente.")

    finally:
        print("Finalizó la simulación de clientes válidos.")

    # ── 4. SIMULACIÓN DE CLIENTE INVÁLIDO ───────────────────────

    try:
        print("\nProbando cliente inválido...\n")

        cliente_error = Cliente("")

    except Exception as e:
        registrar_error("Cliente inválido detectado correctamente:", e)

    # ── 5. SIMULACIÓN DE RESERVAS VÁLIDAS ───────────────────────

    try:
        print("\nCreando reservas válidas...\n")

        cliente1 = Cliente("Carlos")
        cliente2 = Cliente("Laura")

        reserva1 = Reserva(cliente1, servicio1, 2)
        reserva2 = Reserva(cliente2, servicio2, 1)

        reserva1.confirmar()
        reserva2.confirmar()

        reserva1.procesar()
        reserva2.cancelar()

    except Exception as e:
        registrar_error("Error en reservas:", e)

    else:
        print("Reservas procesadas correctamente.")

    finally:
        print("Finalizó la simulación de reservas válidas.")

    # ── 6. SIMULACIÓN DE RESERVA INVÁLIDA POR CLIENTE NULO ──────

    try:
        print("\nProbando reserva inválida por cliente nulo...\n")

        reserva_error = Reserva(None, servicio1, 2)

    except Exception as e:
        registrar_error("Reserva inválida detectada correctamente:", e)

    # ── 7. SIMULACIÓN DE RESERVA INVÁLIDA POR DURACIÓN ──────────

    try:
        print("\nProbando reserva inválida por duración negativa...\n")

        reserva_error = Reserva(Cliente("Pedro"), servicio1, -5)

    except Exception as e:
        registrar_error("Reserva inválida detectada correctamente:", e)

    # ── 8. SIMULACIÓN DE RESERVA SIN SERVICIO ───────────────────

    try:
        print("\nProbando reserva inválida por servicio nulo...\n")

        reserva_error = Reserva(Cliente("Ana"), None, 3)

    except Exception as e:
        registrar_error("Reserva inválida detectada correctamente:", e)

    # ── 9. SIMULACIÓN DE CANCELACIÓN NO PERMITIDA ───────────────

    try:
        print("\nProbando cancelación de reserva ya procesada...\n")

        cliente3 = Cliente("Miguel")
        reserva3 = Reserva(cliente3, servicio3, 4)

        reserva3.confirmar()
        reserva3.procesar()
        reserva3.cancelar()

    except Exception as e:
        registrar_error("Operación no permitida detectada correctamente:", e)

    # ── 10. MOSTRAR RESERVAS REGISTRADAS ────────────────────────

    try:
        print("\nLISTA DE RESERVAS:")
        Reserva.mostrar_reservas()

    except Exception as e:
        registrar_error("Error al mostrar reservas:", e)

    print("\n" + "=" * 60)
    print("EL SISTEMA CONTINÚA FUNCIONANDO CORRECTAMENTE")
    print("=" * 60)


# ── EJECUCIÓN DEL PROGRAMA ──────────────────────────────────────

if __name__ == "__main__":
    simulacion_integral()