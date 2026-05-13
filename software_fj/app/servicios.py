# MODULO 2: CLASE SERVICIOS Y SERVICIOS ESPECIALIZADOS
# Autor: Everson Daniel Cumbalaza Benavides

from abc import ABC, abstractmethod
from .entidades_base import EntidadSistema
from .calculos import CalculadoraCostos, ErrorCalculo
import re


# -----------------------------------------------------------------------
# EXCEPCIONES MODULO SERVICIOS: Excepciones personalizadas para servicios.
# -----------------------------------------------------------------------
class ServicioError(Exception):
    """Error base del módulo de servicios."""

    def __init__(self, mensaje, valor_recibido=None):
        super().__init__(mensaje)
        self.valor_recibido = valor_recibido


class ServicioNoDisponibleError(ServicioError):
    """Se lanza cuando se intenta acceder a un servicio que no existe."""
    pass


class ServicioNombreInvalidoError(ServicioError):
    """Se lanza cuando el nombre del servicio no cumple las reglas."""
    pass


class ServicioCostoInvalidoError(ServicioError):
    """Se lanza cuando el costo del servicio es inválido."""
    pass


class ServicioIVAInvalidoError(ServicioError):
    """Se lanza cuando la tasa de IVA es inválida."""
    pass


class ServicioDescuentoInvalidoError(ServicioError):
    """Se lanza cuando la tasa de descuento es inválida."""
    pass


# -----------------------------------------------------------------------
# AdminServicios: guarda todos los servicios creados en un diccionario.
# -----------------------------------------------------------------------
class AdminServicios:
    """Repositorio en memoria para todos los servicios del sistema."""

    def __init__(self) -> None:
        self._servicios: dict = {}

    @property
    def servicios(self) -> dict:
        return self._servicios

    def agregar_servicio(self, nuevo_servicio: "Servicio") -> bool:
        """Agrega un servicio al repositorio. Retorna True si tuvo éxito."""
        if not isinstance(nuevo_servicio, Servicio):
            return False

        if nuevo_servicio.id_servicio in self._servicios:
            # Si el servicio (id) ya esta registrado
            print("Ya existe un servicio con ese ID:")
            print(self._servicios[nuevo_servicio.id_servicio].mostrar_info())
            print("Use la función actualizar_servicio.")
            return False

        # Si el servicio (id) NO esta registrado
        self._servicios[nuevo_servicio.id_servicio] = nuevo_servicio
        return True

    def actualizar_servicio(self, id_servicio: str, nuevo_servicio: "Servicio") -> bool:
        """Reemplaza un servicio existente. Retorna True si tuvo éxito."""
        if not isinstance(nuevo_servicio, Servicio) or id_servicio not in self._servicios:
            # Si el servicio que se quiere actualizar no esta en la base de datos
            return False

        self._servicios[id_servicio] = nuevo_servicio
        return True

    def obtener_servicio(self, id_servicio: str) -> "Servicio":
        """Busca un servicio por ID y lanza excepción si no existe."""
        if id_servicio not in self._servicios:
            raise ServicioNoDisponibleError(
                f"Servicio con ID {id_servicio} no encontrado.")
        return self._servicios[id_servicio]


# Instancia de servicios
admin_servicios = AdminServicios()


# -----------------------------------------------------------------------
# IDGenerador: crea IDs únicos con formato Letra+Número (ej: S100, S101).
# -----------------------------------------------------------------------
class IDGenerador:
    """Genera IDs únicos y secuenciales para los servicios."""

    @staticmethod
    def crear_id(letra: str, base_datos: dict) -> "str | None":
        """
        Crea un ID que no exista en base_datos.
        Ejemplo: si S100 ya existe, retorna S101, y así sucesivamente.
        """
        if not isinstance(letra, str) or not isinstance(base_datos, dict):
            return None

        letra = letra.upper()
        num = 100  # Los IDs empiezan desde 100 para tener siempre 3 dígitos

        while True:
            nuevo_id = letra + str(num)
            if nuevo_id not in base_datos:
                return nuevo_id
            num += 1


# -----------------------------------------------------------------------
# Entrada: valida y transforma datos antes de guardarlos en un objeto.
# -----------------------------------------------------------------------
class Entrada:
    """Valida y convierte datos de entrada del sistema."""

    def __init__(self, valor) -> None:
        self._valor = valor

    def es_valida(self) -> bool:
        """Verifica que sea un string sin espacios."""
        if not isinstance(self._valor, str):
            return False
        return re.fullmatch(r'\S+', self._valor) is not None

    def es_id_valido(self) -> bool:
        """Verifica formato de ID: una letra seguida de 3 dígitos (ej: S100)."""
        if not isinstance(self._valor, str):
            return False
        return re.fullmatch(r'[A-Z]\d{3}', self._valor.upper()) is not None

    def limpiar(self) -> "str | None":
        """Elimina espacios al inicio, al final y los dobles en medio del texto."""
        if not isinstance(self._valor, str):
            return None
        resultado = self._valor.strip()
        resultado = re.sub(r' {2,}', ' ', resultado)
        return resultado if resultado else None

    def _extraer_numero_porcentaje(self) -> float:
        """Convierte la entrada a float, quitando el símbolo % si existe."""
        if isinstance(self._valor, (int, float)):
            return float(self._valor)

        if isinstance(self._valor, str):
            texto = self._valor.strip()
            if texto.endswith('%'):
                texto = texto[:-1].strip()
            return float(texto)

        raise ValueError("No se puede convertir a porcentaje.")

    def es_porcentaje_valido(self) -> bool:
        """Verifica que la entrada sea un porcentaje válido (mayor o igual a 0)."""
        try:
            return self._extraer_numero_porcentaje() >= 0
        except (ValueError, TypeError):
            return False

    def a_decimal(self) -> float:
        """Convierte un porcentaje a su equivalente decimal. Ej: 19 -> 0.19"""
        if not self.es_porcentaje_valido():
            raise ValueError("La entrada no es un porcentaje válido.")
        return self._extraer_numero_porcentaje() / 100

    def a_numero(self) -> "int | float | None":
        """Intenta convertir la entrada a int o float. Retorna None si no puede."""
        if isinstance(self._valor, (int, float)):
            return self._valor
        if isinstance(self._valor, str):
            try:
                return int(self._valor)
            except ValueError:
                try:
                    return float(self._valor)
                except ValueError:
                    return None
        return None


# -----------------------------------------------------------------------
# Servicio: clase abstracta base para todos los servicios del sistema.
# -----------------------------------------------------------------------
class Servicio(EntidadSistema, ABC):
    """Clase abstracta base para los servicios de Software FJ."""

    def __init__(self, nombre: str, costo: float, iva: float, descuento: float, base_datos: dict) -> None:
        # El ID se genera automáticamente usando la letra "S" y el repositorio actual
        id_generado = IDGenerador.crear_id('S', base_datos)
        super().__init__(id_generado)

        self.__id_servicio = id_generado

        # Usamos los setters directamente para que la validación ocurra al crear el objeto
        self.nombre_servicio = nombre
        self.costo_servicio = costo
        self.valor_iva = iva
        self.valor_desc = descuento

    @property
    def id_servicio(self):
        """ID único del servicio. Solo lectura, no cambia una vez creado."""
        return self.__id_servicio

    @property
    def nombre_servicio(self):
        return self.__nombre_servicio

    @nombre_servicio.setter
    def nombre_servicio(self, valor: str):
        nombre_limpio = Entrada(str(valor)).limpiar()
        if nombre_limpio is None or not (4 <= len(nombre_limpio) <= 50):
            raise ServicioNombreInvalidoError(
                f"El nombre '{valor}' debe tener entre 4 y 50 caracteres.")
        self.__nombre_servicio = nombre_limpio

    @property
    def costo_servicio(self) -> float:
        # Obtiene el costo de servicio
        return self.__costo_servicio

    @costo_servicio.setter
    def costo_servicio(self, valor) -> None:
        numero = Entrada(str(valor)).a_numero()
        if numero is None or numero < 0:
            # Si el numero es None o menor a cero (negativo)
            raise ServicioCostoInvalidoError(
                "El costo debe ser un número mayor o igual a 0.", valor_recibido=valor)
        self.__costo_servicio = float(numero)

    @property
    def valor_iva(self) -> float:
        """IVA almacenado como decimal. Ej: 19% se guarda como 0.19"""
        return self.__valor_iva

    @valor_iva.setter
    def valor_iva(self, valor) -> None:
        try:
            self.__valor_iva = Entrada(valor).a_decimal()
        except ValueError as e:
            raise ServicioIVAInvalidoError(
                "La tasa de IVA no es válida.", valor_recibido=valor) from e

    @property
    def valor_desc(self) -> float:
        """Descuento almacenado como decimal. Ej: 10% se guarda como 0.10"""
        return self.__valor_desc

    @valor_desc.setter
    def valor_desc(self, valor) -> None:
        try:
            self.__valor_desc = Entrada(valor).a_decimal()
        except ValueError as e:
            raise ServicioDescuentoInvalidoError(
                "La tasa de descuento no es válida.", valor_recibido=valor) from e

    def validar(self) -> bool:
        """Valida que el servicio tenga datos consistentes. Retorna True si es válido."""
        # Las validaciones se realizan en los setters, aquí se verifica integridad
        return self.costo_servicio >= 0

    def describir(self) -> str:
        """Descripción genérica que cumple el contrato de EntidadSistema."""
        return self.mostrar_info()

    def calcular_costo_servicio(self, iva_ok: bool = False, disc_ok: bool = False) -> float:
        """
        Calcula el costo final del servicio usando el módulo de cálculos.

        - iva_ok: si es True, se incluye el IVA.
        - disc_ok: si es True, se aplica el descuento.

        Delega en CalculadoraCostos.
        """
        costo = self.costo_servicio

        try:
            if iva_ok and disc_ok:
                # Implmenta iva y descuento en el calculo de costo
                return CalculadoraCostos.costo_combinado(costo, self.valor_iva, self.valor_desc)
            if iva_ok:
                # implementa solo iva en el calculo de costo
                return CalculadoraCostos.costo_con_impuesto(costo, self.valor_iva)
            if disc_ok:
                # implementa solo descuento en el calculo de costo
                return CalculadoraCostos.costo_con_descuento(costo, self.valor_desc)
            return CalculadoraCostos.costo_base(costo)
        except ErrorCalculo as e:
            raise ServicioCostoInvalidoError(
                f"Error al calcular costo del servicio {self.id_servicio}: {e}",
                valor_recibido=costo
            ) from e

    @abstractmethod
    def mostrar_info(self) -> str:
        """
        Retorna un string con la información del servicio.
        """

    def __str__(self) -> str:
        # Permite usar print(servicio) directamente sin llamar mostrar_info() aparte
        return self.mostrar_info()

    def __repr__(self) -> str:
        # Úmuestra el tipo y datos clave del objeto
        return f"{self.__class__.__name__}(id='{self.id_servicio}', nombre='{self.nombre_servicio}')"


# -----------------------------------------------------------------------
# ReservaSala: servicio para reservar salas de reuniones.
# -----------------------------------------------------------------------
class ReservaSala(Servicio):
    """Servicio de reserva de salas de reuniones."""

    def __init__(
        self,
        costo: float,
        iva: float,
        descuento: float,
        base_datos: "dict | None" = None,
        nombre: str = "Reserva de Salas"
    ) -> None:
        # Si no recibe, usa el global compartido con todos los módulos
        base_datos = base_datos or admin_servicios.servicios
        super().__init__(nombre, costo, iva, descuento, base_datos)

    def mostrar_info(self) -> str:
        """Retorna la información de la reserva de sala"""
        return (
            f"RESERVA DE SALAS:\n"
            f"  ID:         {self.id_servicio}\n"
            f"  Nombre:     {self.nombre_servicio}\n"
            f"  Costo base: ${self.costo_servicio:.2f}\n"
            f"  IVA:        {self.valor_iva * 100:.1f}%\n"
            f"  Descuento:  {self.valor_desc * 100:.1f}%"
        )


# -----------------------------------------------------------------------
# AlquilerEquipo: servicio para alquilar equipos tecnológicos por día.
# -----------------------------------------------------------------------
class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos (computadores, proyectores, etc.)."""

    def __init__(
        self,
        costo: float,
        iva: float,
        descuento: float,
        base_datos: "dict | None" = None,
        nombre: str = "Alquiler de Equipo"
    ) -> None:
        base_datos = base_datos or admin_servicios.servicios
        super().__init__(nombre, costo, iva, descuento, base_datos)

    def mostrar_info(self) -> str:
        """Retorna la información del alquiler de equipo"""
        return (
            f"ALQUILER DE EQUIPO:\n"
            f"  ID:        {self.id_servicio}\n"
            f"  Nombre:    {self.nombre_servicio}\n"
            f"  Costo/día: ${self.costo_servicio:.2f}\n"
            f"  IVA:       {self.valor_iva * 100:.1f}%\n"
            f"  Descuento: {self.valor_desc * 100:.1f}%"
        )


# -----------------------------------------------------------------------
# AsesoriaEspecializada: servicio de consultoría por hora.
# -----------------------------------------------------------------------
class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría especializada facturado por hora."""

    def __init__(
        self,
        costo: float,
        iva: float,
        descuento: float,
        base_datos: "dict | None" = None,
        nombre: str = "Asesoría Especializada"
    ) -> None:
        base_datos = base_datos or admin_servicios.servicios
        super().__init__(nombre, costo, iva, descuento, base_datos)

    def mostrar_info(self) -> str:
        """Retorna la información de la asesoría especializada"""
        return (
            f"ASESORÍA ESPECIALIZADA:\n"
            f"  ID:         {self.id_servicio}\n"
            f"  Nombre:     {self.nombre_servicio}\n"
            f"  Costo/hora: ${self.costo_servicio:.2f}\n"
            f"  IVA:        {self.valor_iva * 100:.1f}%\n"
            f"  Descuento:  {self.valor_desc * 100:.1f}%"
        )
