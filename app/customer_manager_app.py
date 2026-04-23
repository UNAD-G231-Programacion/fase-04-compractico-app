from abc import ABC, abstractmethod
import re

# class EntidadBase(ABC):
#     """Clase Abstracta Entidad Base"""

#     @abstractmethod
#     def __init__(self, nombre_entidad):
#         self.nombre_entidad = nombre_entidad

servicios_db = {}


class Servicio(ABC):
    """Clase abstracta Servicio"""

    @abstractmethod
    def __init__(self, id_servicio, nombre_servicio, costo_servicio):
        self.__id_servicio = id_servicio
        self.__nombre_servicio = str(nombre_servicio).strip()

        try:
            self.__costo_servicio = float(costo_servicio)
        except Exception as exc:
            raise ValueError(
                "El argumento Costo debe de ser un numero valido.") from exc

    # ACCESO PROPIEDAD ID SERVICIO

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

        if nuevo_valor not in servicios_db:
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


class Entrada:
    """Clase que recibe entradas para validarlas"""

    def __init__(self, entrada_usuario):
        self._entrada_usuario = entrada_usuario

    def es_valida(self):
        """
        Valida que la cadena no sean solo espacios 
        o tenga espacios entre caracteres.
        """
        # No solo espacios/saltos de línea, y sin espacios entre caracteres
        return bool(re.fullmatch(r'\S+', self._entrada_usuario))

    def es_id_valido(self):
        """Valida que sea un ID valido (1 Letra, 3 Numeros)"""
        self._entrada_usuario = self._entrada_usuario.upper()
        return bool(re.fullmatch(r'[A-Z]\d{3}', self._entrada_usuario))

    def limpiar(self):
        """Devuelve una cadena sin espacios multiples en medio, al inicio o a final"""
        # Quita espacios al inicio y final
        resultado = self._entrada_usuario.strip()
        # reemplaza múltiples espacios en medio por uno solo
        resultado = re.sub(r' {2,}', ' ', resultado)
        return resultado if resultado else None


# class ReservaSalas(Servicio):
#     """
#     Clase que representa el servicio de reserva de salas.
#     """

#     def __init__(self, id_servicio, nombre_servicio, costo_servicio):
#         super().__init__(id_servicio, nombre_servicio, costo_servicio)
