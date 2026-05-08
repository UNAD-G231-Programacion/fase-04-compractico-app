"""
=====================================================================
 Funcion 1

 Diseñar la clase abstracta raíz del sistema y la clase Cliente con 
 encapsulación, validaciones, gestión de la lista interna de clientes 
 y excepciones personalizadas del módulo.

 Nombre: Andres Felipe Maya Ortega
=====================================================================
"""
# Importación de módulos base para la creación de interfaces (ABC), 
# manipulación de textos (re) y definición de tipos de datos (typing).

from abc import ABC, abstractmethod
import re
from typing import Dict

# ─────────────────────────────────────────────
# EXCEPCIONES PERSONALIZADAS
# ─────────────────────────────────────────────

"""
Jerarquía de excepciones personalizadas para la gestión de errores del sistema.
Permite capturar fallos específicos relacionados con el manejo de clientes
y validación de datos de forma controlada.
"""

# Excepción general para errores de lógica de clientes
class ErrorSistema(Exception):
    def __init__(self, mensaje: str):
        super().__init__(mensaje)

# Clase base para todas las excepciones del software
class ErrorSistema(Exception):
    def __init__(self, mensaje: str):
        super().__init__(mensaje)

# Excepción general para errores de lógica de clientes
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
