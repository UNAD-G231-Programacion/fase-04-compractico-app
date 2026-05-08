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