from abc import ABC, abstractmethod
import re


class AdminServicios:
    """Administra la colección de servicios en memoria."""

    def __init__(self) -> None:
        self._servicios = {}

    @property
    def servicios(self):
        return self._servicios

    def agregar_servicio(self, nuevo_servicio):
        """Agrega un servicio si no existe el mismo ID."""
        if not isinstance(nuevo_servicio, Servicio):
            return False

        if nuevo_servicio.id_servicio in self._servicios:
            # El mismo ID ya está registrado, no se reemplaza.
            print("Ya existe un servicio con ese ID:\n")
            self._servicios[nuevo_servicio.id_servicio].mostrar_info()
            print("\nUse la función actualizar_servicio")
            return False

        self._servicios[nuevo_servicio.id_servicio] = nuevo_servicio
        return True

    def actualizar_servicio(self, id_servicio, nuevo_valor):
        """Reemplaza un servicio existente por un nuevo objeto."""
        if id_servicio in self._servicios:
            self._servicios[id_servicio] = nuevo_valor
            return True
        return False


admin_servicios = AdminServicios()


class IDGenerador:
    """Genera identificadores secuenciales para servicios."""

    @staticmethod
    def crear_id(letra, base_datos):
        """Genera un ID unico basado en una letra inicial y una base de datos."""
        if isinstance(letra, str) and isinstance(base_datos, dict):
            letra = letra.upper()
            num = 100

            while True:
                nuevo_id = letra + str(num)
                if nuevo_id not in base_datos:
                    # Retorna el primer ID libre en la secuencia.
                    return nuevo_id
                num += 1


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
        entrada = self._entrada_usuario.upper()
        return bool(re.fullmatch(r'[A-Z]\d{3}', entrada))

    def limpiar(self):
        """Devuelve una cadena sin espacios multiples en medio, al inicio o a final"""

        if isinstance(self._entrada_usuario, str):
            # Quita espacios al inicio y final
            resultado = self._entrada_usuario.strip()
            # Reemplaza múltiples espacios en medio por uno solo
            resultado = re.sub(r' {2,}', ' ', resultado)
            return resultado if resultado else None
        return str(self._entrada_usuario)

    def _parse_porcentaje(self):
        """Extrae el numero de una entrada tipo porcentaje."""
        if isinstance(self._entrada_usuario, (int, float)):
            return float(self._entrada_usuario)

        if isinstance(self._entrada_usuario, str):
            entrada = self._entrada_usuario.strip()
            # Si la entrada termina en '%', se ignora el símbolo.
            if entrada.endswith('%'):
                entrada = entrada[:-1].strip()
            return float(entrada)

        raise ValueError("No es un porcentaje valido")

    def es_porcentaje_valido(self):
        """Valida que la entrada es un porcentaje positivo o cero."""
        try:
            valor = self._parse_porcentaje()
            return valor >= 0
        except (ValueError, TypeError):
            # Cualquier error en el parseo indica que la entrada no es valida.
            return False

    def conv_porcentaje(self):
        """Convierte una entrada valida a su valor decimal (porcentaje/100)."""
        if not self.es_porcentaje_valido():
            raise ValueError("La entrada no es un porcentaje valido.")

        return self._parse_porcentaje() / 100


# CLASE ABSTRACTA SERVICIO
class Servicio(ABC):
    """Clase abstracta Servicio"""

    @abstractmethod
    def __init__(self, nombre_servicio, costo_servicio, valor_iva, valor_desc, base_datos):
        self.__id_servicio = IDGenerador.crear_id("S", base_datos)

        # Validamos el nombre usando el setter para aplicar limpieza y limite de largo.
        self.nombre_servicio = nombre_servicio

        # Usamos los setters para reutilizar validación y conversión.
        self.costo_servicio = costo_servicio
        self.valor_iva = valor_iva
        self.valor_desc = valor_desc

    @property
    def id_servicio(self):
        """Accede a la propiedad ID servicio."""
        return self.__id_servicio

    # ACCESO PROPIEDAD NOMBRE SERVICIO
    @property
    def nombre_servicio(self):
        """Accede a la propiedad nombre del servicio."""
        return self.__nombre_servicio

    @nombre_servicio.setter
    def nombre_servicio(self, nuevo_valor):
        # Limpia la entrada y elimina espacios extras.
        nuevo_valor = Entrada(str(nuevo_valor)).limpiar()

        if nuevo_valor is not None and 4 <= len(nuevo_valor) <= 50:
            self.__nombre_servicio = nuevo_valor
            return

        raise ValueError(
            f"El nombre ingresado: '{nuevo_valor}' excede el limite de caracteres (4-50) o no es valido.")

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

    @property
    def valor_iva(self):
        return self.__valor_iva

    @valor_iva.setter
    def valor_iva(self, nuevo_valor):
        self.__valor_iva = Entrada(nuevo_valor).conv_porcentaje()

    @property
    def valor_desc(self):
        return self.__valor_desc

    @valor_desc.setter
    def valor_desc(self, nuevo_valor):
        self.__valor_desc = Entrada(nuevo_valor).conv_porcentaje()

    def mostrar_info(self):
        """Muestra la informacion del servicio."""
        return f"""INFORMACION DEL SERVICIO:
- ID: {self.id_servicio}
- Nombre: {self.nombre_servicio}
- Costo: ${self.costo_servicio}
- Porc. IVA: {self.valor_iva*100}%
- Porc.Desc: {self.valor_desc*100}%"""

    def calcular_costos(self):
        """Calcula el costo final aplicando IVA y descuento."""
        total_pago = self.costo_servicio

        # Suma IVA sobre el costo actual.
        if self.valor_iva > 0:
            total_pago += total_pago * self.valor_iva
        # Aplica descuento sobre el total actual, después de IVA si ya se agregó.
        if self.valor_desc > 0:
            total_pago -= total_pago * self.valor_desc

        return total_pago


# SERVICIOS
class ReservaSala(Servicio):
    """Servicio Reserva de Salas"""

    def __init__(self, costo_servicio, valor_iva, valor_desc, base_datos=None, nombre_servicio="Reserva de Salas"):
        if base_datos is None:
            base_datos = admin_servicios.servicios
        super().__init__(nombre_servicio, costo_servicio, valor_iva, valor_desc, base_datos)


class AlquilerEquipo(Servicio):
    """Servicio Alquiler Equipo"""

    def __init__(self, costo_servicio, valor_iva, valor_desc, base_datos=None, nombre_servicio="Alquiler Equipo"):
        if base_datos is None:
            base_datos = admin_servicios.servicios
        super().__init__(nombre_servicio, costo_servicio, valor_iva, valor_desc, base_datos)


class AsesoriaEspecializada(Servicio):
    """Servicio Asesoria Especializada"""

    def __init__(self, costo_servicio, valor_iva, valor_desc, base_datos=None, nombre_servicio="Asesoria Especializada"):
        if base_datos is None:
            base_datos = admin_servicios.servicios
        super().__init__(nombre_servicio, costo_servicio, valor_iva, valor_desc, base_datos)
