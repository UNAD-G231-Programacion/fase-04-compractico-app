# EXCEPCIONES DE RESERVA

class ReservaError(Exception):
    pass

class EstadoReservaError(ReservaError):
    pass

# RESERVA

class Reserva:
    lista_reservas = []

    def __init__(self, cliente, servicio, duracion):
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "PENDIENTE"
        self.validar()

    def validar(self):
        if self.cliente is None:
            raise ReservaError("Cliente inválido")

        if self.servicio is None:
            raise ReservaError("Servicio inválido")

        if self.duracion <= 0:
            raise ReservaError("Duración inválida")

    # ✔ try / except / else
    def confirmar(self):
        try:
            if self.estado != "PENDIENTE":
                raise EstadoReservaError("No se puede confirmar")

            costo = self.servicio.calcular_costo(self.duracion)

        except Exception as e:
            self.log_error("Error al confirmar", e)

        else:
            self.estado = "CONFIRMADA"
            Reserva.lista_reservas.append(self)
            print(f"Reserva confirmada. Costo: {costo}")

    # ✔ try / except / finally
    def cancelar(self):
        try:
            if self.estado == "CANCELADA":
                raise EstadoReservaError("Ya cancelada")

            self.estado = "CANCELADA"

        except Exception as e:
            self.log_error("Error al cancelar", e)

        finally:
            print("Cancelación finalizada")

    def procesar(self):
        try:
            if self.estado != "CONFIRMADA":
                raise EstadoReservaError("No confirmada")

            print("Procesando reserva...")

        except Exception as e:
            self.log_error("Error al procesar", e)

    # Logs
    def log_error(self, mensaje, error):
        with open("logs.txt", "a") as f:
            f.write(f"{mensaje}: {str(error)}\n")

    @classmethod
    def mostrar_reservas(cls):
        for r in cls.lista_reservas:
            print(f"{r.cliente.nombre} - {r.estado}")