from datetime import datetime
from entidades_base import EntidadSistema, Cliente
from servicios import Servicio, IDGenerador

# EXCEPCIONES PERSONALIZADAS


class ReservaError(Exception):
    """Excepción general para errores de reserva"""
    pass


class EstadoReservaError(ReservaError):
    """Error relacionado con el estado de la reserva"""
    pass

# Clase principal de reservas del sistema


class Reserva(EntidadSistema):
    # Diccionario para generar IDs únicos (compatible con IDGenerador)
    _reservas = {}

    # Estados posibles de una reserva
    ESTADO_PENDIENTE = "PENDIENTE"
    ESTADO_CONFIRMADA = "CONFIRMADA"
    ESTADO_CANCELADA = "CANCELADA"

    def __init__(self, cliente, servicio, duracion):
        """
        Constructor de la clase Reserva
        """
        # Generar ID único para la reserva
        id_reserva = IDGenerador.crear_id("R", Reserva._reservas)
        # Llamar al constructor de la clase base
        super().__init__(id_reserva)
        # Registrar la reserva en el diccionario central desde su creación
        Reserva._reservas[id_reserva] = self

        # Datos principales de la reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        # Estado inicial de la reserva
        self.estado = Reserva.ESTADO_PENDIENTE
        # Fecha de creacion
        self.fecha = datetime.now()

        # Validacion inicial de datos
        self.validar()

    # Validacion de datos de entrada

    def validar(self) -> bool:
        """
        Valida los datos de la reserva.
        Retorna True si es válida, lanza excepción en caso contrario.
        """
        # Validar que cliente sea una instancia de Cliente
        if not isinstance(self.cliente, Cliente):
            raise ReservaError(
                "El cliente no es una instancia válida de Cliente")

        # Validar que servicio sea una instancia de Servicio
        if not isinstance(self.servicio, Servicio):
            raise ReservaError(
                "El servicio no es una instancia válida de Servicio")

        # Validar duración numerica
        if not isinstance(self.duracion, (int, float)):
            raise ReservaError("La duración debe ser numérica")

        # Verifica duracion positiva
        if self.duracion <= 0:
            raise ReservaError("La duración debe ser mayor a 0")

        return True

    # CONFIRMAR RESERVA
    # try / except / else
    def confirmar(self):
        """
        Confirma la reserva y calcula el costo
        """

        try:

            if self.estado != Reserva.ESTADO_PENDIENTE:
                raise EstadoReservaError(
                    "Solo reservas pendientes pueden confirmarse"
                )

            # Calcular costo usando el servicio
            costo_unitario = self.servicio.calcular_costo_servicio(
                iva_ok=True, disc_ok=True)

            costo = costo_unitario * self.duracion

        except Exception as e:

            self.log_error("Error al confirmar reserva", e)

            # Encadenamiento de excepciones
            raise ReservaError(
                "Falló la confirmación de la reserva"
            ) from e

        else:

            self.estado = Reserva.ESTADO_CONFIRMADA
            # La reserva ya está en _reservas desde su creación

            print(f"Reserva confirmada correctamente")
            print(f"Costo total: ${costo}")

    # CANCELAR RESERVA
    # try / except / finally

    def cancelar(self):
        """
        Cancela la reserva
        """

        try:

            if self.estado == Reserva.ESTADO_CANCELADA:
                raise EstadoReservaError(
                    "La reserva ya está cancelada"
                )

            self.estado = Reserva.ESTADO_CANCELADA

            print("Reserva cancelada correctamente")

        except Exception as e:

            self.log_error("Error al cancelar reserva", e)

            raise ReservaError(
                "Falló la cancelación de la reserva"
            ) from e

        finally:

            print("Proceso de cancelación finalizado")

    # PROCESAR RESERVA

    def procesar(self):
        """
        Procesa la reserva confirmada
        """

        try:

            if self.estado != Reserva.ESTADO_CONFIRMADA:
                raise EstadoReservaError(
                    "Solo reservas confirmadas pueden procesarse"
                )

            print("Procesando reserva...")
            print("Servicio ejecutado correctamente")

        except Exception as e:

            self.log_error("Error al procesar reserva", e)

            raise ReservaError(
                "Error durante el procesamiento"
            ) from e
    # LOGS

    def log_error(self, mensaje, error):
        """
        Guarda errores en archivo logs.txt
        """

        with open("logs.txt", "a", encoding="utf-8") as archivo:

            archivo.write(
                f"{datetime.now()} | ERROR | "
                f"{mensaje}: {str(error)}\n"
            )

    # MOSTRAR RESERVAS

    @classmethod
    def mostrar_reservas(cls):
        """
        Muestra todas las reservas registradas
        """
        print("\n===== LISTA DE RESERVAS =====")
        if not cls._reservas:
            print("No hay reservas registradas")
            return
        for reserva in cls._reservas.values():
            print(
                f"Cliente: {reserva.cliente.nombre} | "
                f"Estado: {reserva.estado} | "
                f"Duración: {reserva.duracion} horas | "
                f"Fecha: {reserva.fecha}"
            )

    # REPRESENTACIÓN EN TEXTO

    def __str__(self):

        return (
            f"Reserva("
            f"cliente={self.cliente.nombre}, "
            f"estado={self.estado}, "
            f"duracion={self.duracion}"
            f")"
        )

    def describir(self) -> str:
        """
        Retorna una descripción detallada de la reserva.
        """
        return (
            f"Reserva {self.id_entidad}:\n"
            f"  Cliente:  {self.cliente.nombre}\n"
            f"  Servicio: {self.servicio.mostrar_info()}\n"
            f"  Estado:   {self.estado}\n"
            f"  Duración: {self.duracion} horas\n"
            f"  Fecha:    {self.fecha}"
        )
