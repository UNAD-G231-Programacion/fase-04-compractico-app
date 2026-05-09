
# =====================================================================
# Funcion 1

# Diseñar la clase abstracta raíz del sistema y la clase Cliente con
# encapsulación, validaciones, gestión de la lista interna de clientes
# y excepciones personalizadas del módulo.

# Nombre: Andres Felipe Maya Ortega
# =====================================================================

# Importación de módulos base para la creación de interfaces (ABC),
# manipulación de textos (re) y definición de tipos de datos (typing).

from abc import ABC, abstractmethod
import re
from typing import Dict

# ─────────────────────────────────────────────
# EXCEPCIONES PERSONALIZADAS
# ─────────────────────────────────────────────


# Jerarquía de excepciones personalizadas para la gestión de errores del sistema.
# Permite capturar fallos específicos relacionados con el manejo de clientes
# y validación de datos de forma controlada.


# Excepción general para errores de lógica de clientes


class ErrorSistema(Exception):
    def __init__(self, mensaje: str):
        super().__init__(mensaje)


class ErrorCliente(ErrorSistema):
    pass

# Error cuando el ID o documento ya está registrado en el sistema


class ErrorClienteDuplicado(ErrorCliente):
    pass

# Error cuando el cliente solicitado no existe en la base de datos


class ErrorClienteNoEncontrado(ErrorCliente):
    pass

# Error para validaciones de formato (ej. correo mal escrito o campos vacíos)


class ErrorDatoInvalido(ErrorCliente):
    pass

# ─────────────────────────────────────────────
# CLASE ABSTRACTA
# ─────────────────────────────────────────────

# Una clase abstracta es un "molde" que no se puede usar directamente,
# sirve para que otras clases hereden de ella.


class EntidadSistema(ABC):

    def __init__(self, id_entidad: str):
        # El guion bajo (_) indica que este atributo es "protegido".
        # Es una buena práctica para encapsular los datos.
        self._id_entidad = id_entidad

    @property
    def id_entidad(self):
        # Este decorador permite leer el ID, pero no modificarlo fácilmente.
        # Funciona como un método "getter".
        return self._id_entidad

    @abstractmethod
    def validar(self):
        # Al ser un método abstracto, no tiene código aquí (pass).
        # Obliga a que cualquier clase hija (ej. Cliente) cree su propia validación.
        pass

    @abstractmethod
    def describir(self):
        # Al igual que validar, obliga a las clases hijas a implementar
        # un método que devuelva una descripción de la entidad.
        pass

# ─────────────────────────────────────────────
# CLASE CLIENTE
# ─────────────────────────────────────────────

# La clase Cliente hereda de EntidadSistema, cumpliendo el "contrato" anterior.


class Cliente(EntidadSistema):

    # Atributo de clase: Un diccionario que funciona como una pequeña base de datos
    # en memoria para almacenar a todos los clientes creados, usando su ID como llave.
    _clientes_por_id: Dict[str, "Cliente"] = {}

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        # Llama al constructor de la clase padre (EntidadSistema) para asignar el ID.
        super().__init__(id_cliente)

        # Asigna los atributos específicos de un cliente.
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    # ─── ENCAPSULACIÓN Y VALIDACIONES ───

    @property
    def nombre(self):
        # Devuelve el valor del atributo privado _nombre
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        # Valida que el nombre solo tenga letras y espacios, mínimo 3 caracteres
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]{3,}$", valor):
            raise ErrorDatoInvalido(
                "Nombre inválido: Debe contener solo letras y mínimo 3 caracteres")
        self._nombre = valor

    @property
    def correo(self):
        # Devuelve el valor del atributo privado _correo
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        # Usa una expresión regular para validar el formato estándar de un email
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", valor):
            raise ErrorDatoInvalido("Correo inválido: Formato no reconocido")
        self._correo = valor

    @property
    def telefono(self):
        # Devuelve el valor del atributo privado _telefono
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        # Valida que sean solo números y tengan una longitud entre 7 y 15 dígitos
        if not valor.isdigit() or not (7 <= len(valor) <= 15):
            raise ErrorDatoInvalido(
                "Teléfono inválido: Debe tener entre 7 y 15 dígitos numéricos")
        self._telefono = valor

    # ─── IMPLEMENTACIÓN DE MÉTODOS ABSTRACTOS ───

    def validar(self):
        # Implementación del método obligatorio de EntidadSistema.
        # En este punto, si el objeto se creó, ya pasó por los setters
        # que validaron los datos, por lo que retorna True.
        return True

    def describir(self):
        # Implementación del método obligatorio para mostrar la información.
        # Retorna una cadena de texto formateada con los detalles del cliente.
        return f"Cliente: {self.nombre}, Correo: {self.correo}, Tel: {self.telefono}"

    # ─── GESTIÓN DE CLIENTES ───

    @classmethod
    def agregar_cliente(cls, cliente):
        # Verifica si el ID del cliente ya existe en el diccionario global.
        # Si existe, lanza la excepción personalizada que creamos al inicio.
        if cliente.id_entidad in cls._clientes_por_id:
            raise ErrorClienteDuplicado(
                f"El cliente con ID {cliente.id_entidad} ya está registrado")

        # Si es nuevo, lo guarda en el diccionario usando el ID como clave.
        cls._clientes_por_id[cliente.id_entidad] = cliente

    @classmethod
    def buscar_cliente(cls, id_cliente):
        # Busca un ID específico en el diccionario.
        # Si no lo encuentra, lanza una excepción controlada.
        if id_cliente not in cls._clientes_por_id:
            raise ErrorClienteNoEncontrado(
                f"No se encontró ningún cliente con el ID: {id_cliente}")

        # Retorna el objeto Cliente completo si la búsqueda es exitosa.
        return cls._clientes_por_id[id_cliente]

    @classmethod
    def listar_clientes(cls):
        # Convierte todos los valores del diccionario (los objetos Cliente)
        # en una lista simple para facilitar su visualización o iteración.
        return list(cls._clientes_por_id.values())
