import logging
from datetime import datetime
from .entidades_base import EntidadSistema, Cliente
from .servicios import Servicio, IDGenerador

# EXCEPCIONES PERSONALIZADAS


class ReservaError(Exception):
    """Excepción general para errores de reserva"""
    pass


class EstadoReservaError(ReservaError):
    """Error relacionado con el estado de la reserva"""
    pass

# Clase principal de reservas del sistema


class Reserva(EntidadSistema):
    # Diccionario que almacena todas las reservas, indexadas por su ID único.
    # Sirve como repositorio único y para la generación de nuevos IDs.
    _reservas = {}

    # Estados posibles de una reserva
    ESTADO_PENDIENTE = "PENDIENTE"
    ESTADO_CONFIRMADA = "CONFIRMADA"
    ESTADO_CANCELADA = "CANCELADA"
    ESTADO_PROCESADA = "PROCESADA"

    def __init__(self, cliente, servicio, duracion):
        """
        Constructor de la clase Reserva
        """
        # Generar ID único para la reserva
        id_reserva = IDGenerador.crear_id("R", Reserva._reservas)
        # Llamar al constructor de la clase base
        super().__init__(id_reserva)

        # Datos principales de la reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        # Estado inicial de la reserva
        self.estado = Reserva.ESTADO_PENDIENTE
        # Fecha de creación
        self.fecha = datetime.now()

        # Validación inicial de datos ANTES de registrar
        self.validar()

        # Registrar la reserva en el diccionario central solo después de validación exitosa
        Reserva._reservas[id_reserva] = self

    # Validación de datos de entrada

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

        # Validar duración numérica
        if not isinstance(self.duracion, (int, float)):
            raise ReservaError("La duración debe ser numérica")

        # Verifica duración positiva
        if self.duracion <= 0:
            raise ReservaError("La duración debe ser mayor a 0")

        return True

    # CONFIRMAR RESERVA
    def confirmar(self):
        """
        Confirma la reserva y calcula el costo
        """
        # Validar que solo se puedan confirmar reservas pendientes
        if self.estado != Reserva.ESTADO_PENDIENTE:
            raise EstadoReservaError(
                "Solo reservas pendientes pueden confirmarse"
            )

        try:
            # Calcular costo usando el servicio (aplica IVA y descuento por defecto)
            costo_unitario = self.servicio.calcular_costo_servicio(
                iva_ok=True, disc_ok=True)
            costo = costo_unitario * self.duracion

        except Exception as e:
            logging.error(
                f"Error al calcular costo de reserva {self.id_entidad}: {e}")
            raise ReservaError(
                "No se pudo calcular el costo de la reserva"
            ) from e

        # Cambiar estado a confirmada (solo si cálculo fue exitoso)
        self.estado = Reserva.ESTADO_CONFIRMADA
        logging.info(
            f"Reserva {self.id_entidad} confirmada. Costo total: ${costo:.2f}")

    # CANCELAR RESERVA
    def cancelar(self):
        """
        Cancela la reserva
        """
        # Validaciones previas
        if self.estado == Reserva.ESTADO_CANCELADA:
            raise EstadoReservaError(
                "La reserva ya está cancelada"
            )
        if self.estado == Reserva.ESTADO_PROCESADA:
            raise EstadoReservaError(
                "No se puede cancelar una reserva ya procesada"
            )

        try:
            # Cambiar estado a cancelada
            self.estado = Reserva.ESTADO_CANCELADA
            logging.info(f"Reserva {self.id_entidad} cancelada correctamente")

        except Exception as e:
            logging.error(f"Error al cancelar reserva {self.id_entidad}: {e}")
            raise ReservaError(
                "Falló la cancelación de la reserva"
            ) from e

    # PROCESAR RESERVA
    def procesar(self):
        """
        Procesa la reserva confirmada
        """
        # Validar que solo se procesen reservas confirmadas
        if self.estado != Reserva.ESTADO_CONFIRMADA:
            raise EstadoReservaError(
                "Solo reservas confirmadas pueden procesarse"
            )

        try:
            # Aquí iría la lógica de procesamiento del servicio
            # (simulado por ahora)
            pass

        except Exception as e:
            logging.error(
                f"Error al procesar servicio de reserva {self.id_entidad}: {e}")
            raise ReservaError(
                "Error durante el procesamiento del servicio"
            ) from e

        # Cambiar estado a procesada (solo si procesamiento fue exitoso)
        self.estado = Reserva.ESTADO_PROCESADA
        logging.info(f"Reserva {self.id_entidad} procesada correctamente")

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
            # Protección que validar que cliente exista
            nombre_cliente = reserva.cliente.nombre if reserva.cliente else "CLIENTE INVÁLIDO"
            print(
                f"Cliente: {nombre_cliente} | "
                f"Estado: {reserva.estado} | "
                f"Duración: {reserva.duracion} horas | "
                f"Fecha: {reserva.fecha}"
            )

    # REPRESENTACIÓN EN TEXTO
    def __str__(self):
        # Protección que validar que cliente exista
        nombre_cliente = self.cliente.nombre if self.cliente else "CLIENTE INVÁLIDO"
        return (
            f"Reserva("
            f"cliente={nombre_cliente}, "
            f"estado={self.estado}, "
            f"duracion={self.duracion}"
            f")"
        )

    def describir(self) -> str:
        """
        Retorna una descripción detallada de la reserva.
        """
        # Protección validar que cliente y servicio existan
        nombre_cliente = self.cliente.nombre if self.cliente else "CLIENTE INVÁLIDO"
        info_servicio = self.servicio.mostrar_info(
        ) if self.servicio else "SERVICIO INVÁLIDO"
        return (
            f"Reserva {self.id_entidad}:\n"
            f"  Cliente:  {nombre_cliente}\n"
            f"  Servicio: {info_servicio}\n"
            f"  Estado:   {self.estado}\n"
            f"  Duración: {self.duracion} horas\n"
            f"  Fecha:    {self.fecha}"
        )
