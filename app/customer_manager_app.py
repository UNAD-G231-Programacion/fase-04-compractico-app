from abc import ABC, abstractmethod
import re

# class EntidadBase(ABC):
#     """Clase Abstracta Entidad Base"""

#     @abstractmethod
#     def __init__(self, nombre_entidad):
#         self.nombre_entidad = nombre_entidad

# BASES DE DATOS
SERVICIOS = {}
CLIENTES = {}
RESERVAS = {}


# GENERADOR DE IDS:
class IDGenerador:
    """Generador de ID para as distintas entidades."""

    def __init__(self) -> None:
        pass

    def crear_id(self, letra, base_datos):
        """Crea un ID"""
        if isinstance(letra, str):
            if isinstance(base_datos, dict):
                letra = letra.upper()
                num = 100

                while True:
                    nuevo_id = letra + str(num)
                    if nuevo_id not in base_datos:
                        return nuevo_id
                    num += 1

    def id_servicio(self):
        """Crea un ID para servicio con el formato 'S###'"""
        return self.crear_id('S', SERVICIOS)

    def id_cliente(self):
        """Crea un ID para servicio con el formato 'C###'"""
        return self.crear_id('C', CLIENTES)

    def id_reserva(self):
        """Crea un ID para servicio con el formato 'R###'"""
        return self.crear_id('R', RESERVAS)


generador_id = IDGenerador()


class Entrada:
    """Clase que recibe entradas para validarlas"""

    def __init__(self, entrada_usuario):
        self._entrada_usuario = entrada_usuario

    def es_valida(self):
        """Valida que la cadena no sean solo espacios
        o tenga espacios entre caracteres."""
        # No solo espacios/saltos de línea, y sin espacios entre caracteres
        if not isinstance(self._entrada_usuario, str):
            return False
        return bool(re.fullmatch(r'\S+', self._entrada_usuario))

    def es_id_valido(self):
        """Valida que sea un ID valido (1 Letra, 3 Numeros)"""
        if not isinstance(self._entrada_usuario, str):
            return False
        self._entrada_usuario = self._entrada_usuario.upper()
        return bool(re.fullmatch(r'[A-Z]\d{3}', self._entrada_usuario))

    def limpiar(self):
        """Devuelve una cadena sin espacios multiples en medio, al inicio o a final"""

        if isinstance(self._entrada_usuario, str):
            # Quita espacios al inicio y final
            resultado = self._entrada_usuario.strip()
            # reemplaza múltiples espacios en medio por uno solo
            resultado = re.sub(r' {2,}', ' ', resultado)
            return resultado if resultado else None
        return str(self._entrada_usuario)

    def es_porcentaje_valido(self):
        """Valida que una entrada sea un porcentaje valido y lo convierte a su forma decimal."""

        if isinstance(self._entrada_usuario, (int, float)):
            return float(self._entrada_usuario) / 100

        if isinstance(self._entrada_usuario, str):
            entrada = self._entrada_usuario.strip()
            if entrada.endswith('%'):
                entrada = entrada[:-1].strip()

            try:
                valor = float(entrada)
                return valor / 100
            except ValueError:
                return False

        return False


# CLASE ABSTRACTA SERVICIO
class Servicio(ABC):
    """Clase abstracta Servicio"""

    @abstractmethod
    def __init__(self, nombre_servicio, costo_servicio, valor_iva, valor_desc):
        # Generamos un ID nuevo automatico para el servicio creado:
        self.__id_servicio = generador_id.id_servicio()

        self.__nombre_servicio = str(nombre_servicio).strip()

        try:
            self.__costo_servicio = float(costo_servicio)
        except Exception as exc:
            raise ValueError(
                "El argumento 'costo_servicio' debe de ser un numero valido.") from exc

    @property
    def id_servicio(self):
        """Accede a la propiedad ID servicio."""
        return self.__id_servicio

    @id_servicio.setter
    def id_servicio(self, nuevo_valor):
        nuevo_valor = str(nuevo_valor)
        if not Entrada(nuevo_valor).es_id_valido():
            raise ValueError(
                f"El ID '{nuevo_valor}' no es valido. (1 Letra, 3 Numeros).")

        if nuevo_valor not in SERVICIOS:
            # Si el id nuevo no existe en la base de datos de servicios.
            self.__id_servicio = nuevo_valor.upper()
            return

        raise ValueError(
            f"El ID '{nuevo_valor}' ya se encuentra registrado para un servivio.")

    # ACCESO PROPIEDAD NOMBRE SERVICIO
    @property
    def nombre_servicio(self):
        """Accede a la propiedad nombre del servicio."""
        return self.__nombre_servicio

    @nombre_servicio.setter
    def nombre_servicio(self, nuevo_valor):
        nuevo_valor = Entrada(str(nuevo_valor)).limpiar()

        if not nuevo_valor is None:
            print(len(nuevo_valor))
            if 4 <= len(nuevo_valor) <= 50:
                self.__nombre_servicio = nuevo_valor
                return
        raise ValueError(
            f"El nombre ingresado: '{nuevo_valor}' excede el limite de caracteres (3-50) o no es valido.")

    # ACCESO PROPIEDAD COSTO SERVICIO
    @property
    def costo_servicio(self):
        """Accede a la propiedad costo del servicio."""
        return self.__costo_servicio

    @costo_servicio.setter
    def costo_servicio(self, nuevo_valor):
        try:
            nuevo_valor = float(nuevo_valor)
            self.__costo_servicio = nuevo_valor

        except Exception as exc:
            raise ValueError(
                "El valor ingresado debe de ser un numero valido.") from exc

    def mostrar_info(self):
        """Muestra la informacion del servicio."""
        print("INFORMACION DEL SERVICIO:")
        print(f"- ID: {self.id_servicio}")
        print(f"- Nombre: {self.nombre_servicio}")
        print(f"- Costo: ${self.costo_servicio}")

    def calcular_costos(self, impuesto=False, descuento=False):
        """Calcula los costos del servicio"""
        print("No se ha especificado la operacion para obtener el costo.")


# SERVICIOS
class ReservaSala(Servicio):
    """Servicio Reserva de Salas"""

    def __init__(self, costo_servicio, valor_iva, valor_desc, nombre_servicio="Reserva de Sala"):
        super().__init__(nombre_servicio, costo_servicio,
                         valor_iva=valor_iva, valor_desc=valor_desc)


class AlquilerEquipo(Servicio):
    """Servicio Alquiler Equipo"""

    def __init__(self, costo_servicio, valor_iva, valor_desc, nombre_servicio="Alquiler de Equipo"):
        super().__init__(nombre_servicio, costo_servicio,
                         valor_iva=valor_iva, valor_desc=valor_desc)


class AsesoriaEspecializada(Servicio):
    """Servicio Asesoria Especializada"""

    def __init__(self, costo_servicio, valor_iva, valor_desc, nombre_servicio="Asesoria Especializada"):
        super().__init__(nombre_servicio, costo_servicio,
                         valor_iva=valor_iva, valor_desc=valor_desc)
