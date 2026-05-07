"""
=====================================================================
  Software FJ - Versión Básica (Ajustada al Requerimiento)
=====================================================================
"""

from abc import ABC, abstractmethod
import re
from typing import Dict

# ─────────────────────────────────────────────
# EXCEPCIONES PERSONALIZADAS
# ─────────────────────────────────────────────

class ErrorSistema(Exception):
    def __init__(self, mensaje: str):
        super().__init__(mensaje)

class ErrorCliente(ErrorSistema):
    pass

class ErrorClienteDuplicado(ErrorCliente):
    pass

class ErrorClienteNoEncontrado(ErrorCliente):
    pass

class ErrorDatoInvalido(ErrorCliente):
    pass

# ─────────────────────────────────────────────
# CLASE ABSTRACTA
# ─────────────────────────────────────────────

class EntidadSistema(ABC):

    def __init__(self, id_entidad: str):
        self._id_entidad = id_entidad

    @property
    def id_entidad(self):
        return self._id_entidad

    @abstractmethod
    def validar(self):
        pass

    @abstractmethod
    def describir(self):
        pass

# ─────────────────────────────────────────────
# CLASE CLIENTE
# ─────────────────────────────────────────────

class Cliente(EntidadSistema):

    _clientes_por_id: Dict[str, "Cliente"] = {}

    def __init__(self, id_cliente: str, nombre: str, correo: str, telefono: str):
        super().__init__(id_cliente)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    # ─── ENCAPSULACIÓN Y VALIDACIONES ───

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]{3,}$", valor):
            raise ErrorDatoInvalido("Nombre inválido")
        self._nombre = valor

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", valor):
            raise ErrorDatoInvalido("Correo inválido")
        self._correo = valor

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not valor.isdigit() or not (7 <= len(valor) <= 15):
            raise ErrorDatoInvalido("Teléfono inválido")
        self._telefono = valor

    # ─── IMPLEMENTACIÓN DE MÉTODOS ABSTRACTOS ───

    def validar(self):
        return True

    def describir(self):
        return f"Cliente: {self.nombre}, Correo: {self.correo}, Tel: {self.telefono}"

    # ─── GESTIÓN DE CLIENTES ───

    @classmethod
    def agregar_cliente(cls, cliente):
        if cliente.id_entidad in cls._clientes_por_id:
            raise ErrorClienteDuplicado("El cliente ya existe")
        cls._clientes_por_id[cliente.id_entidad] = cliente

    @classmethod
    def buscar_cliente(cls, id_cliente):
        if id_cliente not in cls._clientes_por_id:
            raise ErrorClienteNoEncontrado("Cliente no encontrado")
        return cls._clientes_por_id[id_cliente]

    @classmethod
    def listar_clientes(cls):
        return list(cls._clientes_por_id.values())
