# ============================================================
# SISTEMA INTEGRAL DE GESTIÓN DE CLIENTES, SERVICIOS Y RESERVAS
# Universidad Nacional Abierta y a Distancia - UNAD
# Curso: Programación 213023 - Grupo: 231
# Integrantes:
#   - Daniel Benavides  → Módulo: Servicios Especializados
#   - Johan Pérez       → Módulo: Reservas
#   - Andrés Maya       → Módulo: Arquitectura Base y Gestion de Clientes
#   - Sebastian Gonzales     → Módulo: Calculo de Costos
#   - Jaider Pantoja     → Módulo: No Seleccionado, sin contribuciones
# ============================================================


# ── IMPORTACIONES ───────────────────────────────────────────


# ── MÓDULO 1: SERVICIOS ESPECIALIZADOS (Autor: Daniel Benavides) ───
# (código de Daniel)


# ── MÓDULO 2: RESERVAS (Autor: Johan Pérez) ────────
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

# ── MÓDULO 3: ARQUITECTURA BASE Y GESTION DE CLIENTES (Autor: Andrés Maya) ────────
# (código de Andrés)


# ── MÓDULO 4: CALCULO DE COSTOS (Autor: Sebastian Gonzales) ────────
# (código del Sebastian Gonzales)


# ── MÓDULO 5: SISTEMA DE LOGS Y SIMULACION (Autor: Jaider Pantoja) ────────
# (código del Jaider Pantoja)


# ── PUNTO DE ENTRADA ─────────────────────────────────────────
if __name__ == "__main__":
    # Para iniciar la app.
    pass
