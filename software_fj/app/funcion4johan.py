from datetime import datetime

# EXCEPCIONES PERSONALIZADAS

class ReservaError(Exception):
    """Excepción general para errores de reserva"""
    pass


class EstadoReservaError(ReservaError):
    """Error relacionado con el estado de la reserva"""
    pass

# CLASE RESERVA

class Reserva:

    # Estados posibles
    ESTADO_PENDIENTE = "PENDIENTE"
    ESTADO_CONFIRMADA = "CONFIRMADA"
    ESTADO_CANCELADA = "CANCELADA"

    # Lista general de reservas
    lista_reservas = []

    def __init__(self, cliente, servicio, duracion):
        """
        Constructor de la clase Reserva
        """

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = Reserva.ESTADO_PENDIENTE
        self.fecha = datetime.now()

        self.validar()

    # VALIDACIONES

    def validar(self):
        """
        Valida los datos de la reserva
        """

        # Validar cliente
        if self.cliente is None:
            raise ReservaError("Cliente inválido")

        # Validar servicio
        if self.servicio is None:
            raise ReservaError("Servicio inválido")

        # Validar duración
        if not isinstance(self.duracion, (int, float)):
            raise ReservaError("La duración debe ser numérica")

        if self.duracion <= 0:
            raise ReservaError("La duración debe ser mayor a 0")
        
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
            costo = self.servicio.calcular_costo(self.duracion)

        except Exception as e:

            self.log_error("Error al confirmar reserva", e)

            # Encadenamiento de excepciones
            raise ReservaError(
                "Falló la confirmación de la reserva"
            ) from e

        else:

            self.estado = Reserva.ESTADO_CONFIRMADA

            Reserva.lista_reservas.append(self)

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

        if not cls.lista_reservas:
            print("No hay reservas registradas")
            return

        for reserva in cls.lista_reservas:

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