"""
================================================================================
  SISTEMA INTEGRAL DE GESTIÓN 
  Módulo: Clase Abstracta Raíz + Clase Cliente
  Universidad Nacional Abierta y a Distancia - UNAD
  Curso: Programación 213023
================================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
import re
import os
import logging
from datetime import datetime
from abc import ABC, abstractmethod

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE LOGS
# ─────────────────────────────────────────────────────────────────────────────
LOG_FILE = "sistema_softwarefj.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

def log_evento(nivel: str, mensaje: str):
    """Registra un evento en el archivo de logs."""
    if nivel == "INFO":
        logging.info(mensaje)
    elif nivel == "WARNING":
        logging.warning(mensaje)
    elif nivel == "ERROR":
        logging.error(mensaje)
    elif nivel == "CRITICAL":
        logging.critical(mensaje)


# ─────────────────────────────────────────────────────────────────────────────
# EXCEPCIONES PERSONALIZADAS
# ─────────────────────────────────────────────────────────────────────────────
class SistemaFJError(Exception):
    """Excepción base del sistema Software FJ."""
    def __init__(self, mensaje: str, codigo: int = 0):
        super().__init__(mensaje)
        self.codigo = codigo
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"[Código {self.codigo}] {super().__str__()}"


class ClienteInvalidoError(SistemaFJError):
    """Se lanza cuando los datos de un cliente son inválidos."""
    def __init__(self, campo: str, valor, razon: str):
        mensaje = f"Campo '{campo}' con valor '{valor}' inválido: {razon}"
        super().__init__(mensaje, codigo=100)
        self.campo = campo
        self.valor = valor


class ClienteDuplicadoError(SistemaFJError):
    """Se lanza cuando se intenta registrar un cliente que ya existe."""
    def __init__(self, cedula: str):
        super().__init__(f"Ya existe un cliente con cédula '{cedula}'", codigo=101)
        self.cedula = cedula


class ClienteNoEncontradoError(SistemaFJError):
    """Se lanza cuando no se encuentra un cliente en el sistema."""
    def __init__(self, criterio: str):
        super().__init__(f"Cliente no encontrado con criterio: '{criterio}'", codigo=102)


class OperacionNoPermitidaError(SistemaFJError):
    """Se lanza cuando se intenta una operación no permitida."""
    def __init__(self, operacion: str, razon: str):
        super().__init__(f"Operación '{operacion}' no permitida: {razon}", codigo=103)


# ─────────────────────────────────────────────────────────────────────────────
# CLASE ABSTRACTA RAÍZ: EntidadSistema
# ─────────────────────────────────────────────────────────────────────────────
class EntidadSistema(ABC):
    """
    Clase abstracta raíz del sistema Software FJ.
    Define la interfaz común para todas las entidades del sistema.
    """
    _contador_ids = 0

    def __init__(self, nombre: str):
        EntidadSistema._contador_ids += 1
        self.__id_entidad = EntidadSistema._contador_ids
        self.__nombre = self._validar_nombre(nombre)
        self.__fecha_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__activo = True

    # ── Métodos abstractos que deben implementar las subclases ─────────────
    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripción textual de la entidad."""
        pass

    @abstractmethod
    def validar(self) -> bool:
        """Valida que la entidad tenga datos coherentes."""
        pass

    @abstractmethod
    def obtener_resumen(self) -> dict:
        """Devuelve un diccionario con los datos principales de la entidad."""
        pass

    # ── Método concreto ────────────────────────────────────────────────────
    def _validar_nombre(self, nombre: str) -> str:
        if not nombre or not isinstance(nombre, str):
            raise ClienteInvalidoError("nombre", nombre, "No puede estar vacío")
        nombre = nombre.strip()
        if len(nombre) < 2:
            raise ClienteInvalidoError("nombre", nombre, "Debe tener al menos 2 caracteres")
        if len(nombre) > 100:
            raise ClienteInvalidoError("nombre", nombre, "No puede superar 100 caracteres")
        if not re.match(r"^[A-Za-záéíóúÁÉÍÓÚñÑ\s'-]+$", nombre):
            raise ClienteInvalidoError("nombre", nombre, "Solo letras, espacios, guiones y apóstrofes")
        return nombre

    def activar(self):
        self.__activo = True
        log_evento("INFO", f"Entidad #{self.__id_entidad} '{self.__nombre}' activada.")

    def desactivar(self):
        self.__activo = False
        log_evento("INFO", f"Entidad #{self.__id_entidad} '{self.__nombre}' desactivada.")

    # ── Propiedades ────────────────────────────────────────────────────────
    @property
    def id_entidad(self): return self.__id_entidad

    @property
    def nombre(self): return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        self.__nombre = self._validar_nombre(valor)

    @property
    def fecha_creacion(self): return self.__fecha_creacion

    @property
    def activo(self): return self.__activo

    def __str__(self):
        estado = "Activo" if self.__activo else "Inactivo"
        return f"[{self.__class__.__name__} #{self.__id_entidad}] {self.__nombre} ({estado})"


# ─────────────────────────────────────────────────────────────────────────────
# CLASE CLIENTE
# ─────────────────────────────────────────────────────────────────────────────
class Cliente(EntidadSistema):
    """
    Clase que representa un cliente de Software FJ.
    Hereda de EntidadSistema e implementa encapsulación y validaciones.
    """
    TIPOS_DOCUMENTO = ["CC", "TI", "CE", "PP", "NIT"]

    def __init__(self, nombre: str, cedula: str, email: str,
                 telefono: str, tipo_doc: str = "CC"):
        super().__init__(nombre)
        self.__cedula = self._validar_cedula(cedula)
        self.__email = self._validar_email(email)
        self.__telefono = self._validar_telefono(telefono)
        self.__tipo_doc = self._validar_tipo_doc(tipo_doc)
        self.__historial_reservas = []
        log_evento("INFO", f"Cliente creado: {cedula} - {nombre}")

    # ── Validaciones privadas ──────────────────────────────────────────────
    def _validar_cedula(self, cedula: str) -> str:
        if not cedula or not isinstance(cedula, str):
            raise ClienteInvalidoError("cedula", cedula, "No puede estar vacía")
        cedula = cedula.strip()
        if not re.match(r"^\d{5,15}$", cedula):
            raise ClienteInvalidoError("cedula", cedula,
                                       "Debe tener entre 5 y 15 dígitos numéricos")
        return cedula

    def _validar_email(self, email: str) -> str:
        if not email or not isinstance(email, str):
            raise ClienteInvalidoError("email", email, "No puede estar vacío")
        email = email.strip().lower()
        patron = r"^[\w\.\+\-]+@[\w\-]+\.[a-z]{2,}$"
        if not re.match(patron, email):
            raise ClienteInvalidoError("email", email, "Formato de correo inválido")
        return email

    def _validar_telefono(self, telefono: str) -> str:
        if not telefono or not isinstance(telefono, str):
            raise ClienteInvalidoError("telefono", telefono, "No puede estar vacío")
        telefono = re.sub(r"[\s\-\(\)\+]", "", telefono)
        if not re.match(r"^\d{7,15}$", telefono):
            raise ClienteInvalidoError("telefono", telefono,
                                       "Debe tener entre 7 y 15 dígitos")
        return telefono

    def _validar_tipo_doc(self, tipo: str) -> str:
        tipo = tipo.strip().upper()
        if tipo not in self.TIPOS_DOCUMENTO:
            raise ClienteInvalidoError("tipo_doc", tipo,
                                       f"Debe ser uno de: {', '.join(self.TIPOS_DOCUMENTO)}")
        return tipo

    # ── Implementación de métodos abstractos ──────────────────────────────
    def describir(self) -> str:
        return (f"Cliente: {self.nombre} | {self.__tipo_doc}: {self.__cedula} | "
                f"Email: {self.__email} | Tel: {self.__telefono} | "
                f"Reservas: {len(self.__historial_reservas)}")

    def validar(self) -> bool:
        try:
            self._validar_cedula(self.__cedula)
            self._validar_email(self.__email)
            self._validar_telefono(self.__telefono)
            return True
        except ClienteInvalidoError:
            return False

    def obtener_resumen(self) -> dict:
        return {
            "id": self.id_entidad,
            "nombre": self.nombre,
            "tipo_doc": self.__tipo_doc,
            "cedula": self.__cedula,
            "email": self.__email,
            "telefono": self.__telefono,
            "reservas": len(self.__historial_reservas),
            "activo": self.activo,
            "fecha_registro": self.fecha_creacion
        }

    def agregar_reserva(self, id_reserva: str):
        self.__historial_reservas.append(id_reserva)

    # ── Propiedades públicas (solo lectura para datos sensibles) ───────────
    @property
    def cedula(self): return self.__cedula

    @property
    def email(self): return self.__email

    @email.setter
    def email(self, valor: str):
        self.__email = self._validar_email(valor)
        log_evento("INFO", f"Email actualizado para cliente {self.__cedula}")

    @property
    def telefono(self): return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        self.__telefono = self._validar_telefono(valor)

    @property
    def tipo_doc(self): return self.__tipo_doc

    @property
    def historial_reservas(self): return list(self.__historial_reservas)


# ─────────────────────────────────────────────────────────────────────────────
# GESTIÓN INTERNA DE CLIENTES (sin base de datos)
# ─────────────────────────────────────────────────────────────────────────────
class GestorClientes:
    """
    Gestiona la lista interna de clientes en memoria.
    No usa base de datos; usa listas y diccionarios.
    """
    def __init__(self):
        self.__clientes: dict[str, Cliente] = {}  # cedula -> Cliente

    # ── CRUD ──────────────────────────────────────────────────────────────
    def registrar_cliente(self, nombre: str, cedula: str, email: str,
                          telefono: str, tipo_doc: str = "CC") -> Cliente:
        try:
            if cedula.strip() in self.__clientes:
                raise ClienteDuplicadoError(cedula.strip())
            cliente = Cliente(nombre, cedula, email, telefono, tipo_doc)
            self.__clientes[cliente.cedula] = cliente
            log_evento("INFO", f"Cliente registrado exitosamente: {cedula}")
            return cliente
        except ClienteDuplicadoError as e:
            log_evento("WARNING", str(e))
            raise
        except ClienteInvalidoError as e:
            log_evento("ERROR", str(e))
            raise
        except Exception as e:
            log_evento("CRITICAL", f"Error inesperado al registrar cliente: {e}")
            raise SistemaFJError(f"Error inesperado: {e}", 999) from e

    def buscar_por_cedula(self, cedula: str) -> Cliente:
        try:
            cedula = cedula.strip()
            if cedula not in self.__clientes:
                raise ClienteNoEncontradoError(f"cédula={cedula}")
            return self.__clientes[cedula]
        except ClienteNoEncontradoError as e:
            log_evento("WARNING", str(e))
            raise

    def buscar_por_nombre(self, nombre: str) -> list:
        nombre_lower = nombre.strip().lower()
        resultados = [c for c in self.__clientes.values()
                      if nombre_lower in c.nombre.lower()]
        return resultados

    def eliminar_cliente(self, cedula: str) -> bool:
        try:
            cliente = self.buscar_por_cedula(cedula)
            if cliente.historial_reservas:
                raise OperacionNoPermitidaError(
                    "eliminar", "El cliente tiene reservas asociadas; desactívelo en su lugar")
            del self.__clientes[cedula]
            log_evento("INFO", f"Cliente {cedula} eliminado del sistema.")
            return True
        except (ClienteNoEncontradoError, OperacionNoPermitidaError):
            raise

    def desactivar_cliente(self, cedula: str):
        cliente = self.buscar_por_cedula(cedula)
        cliente.desactivar()

    def activar_cliente(self, cedula: str):
        cliente = self.buscar_por_cedula(cedula)
        cliente.activar()

    def listar_clientes(self, solo_activos: bool = False) -> list:
        clientes = list(self.__clientes.values())
        if solo_activos:
            clientes = [c for c in clientes if c.activo]
        return clientes

    @property
    def total_clientes(self): return len(self.__clientes)


# ─────────────────────────────────────────────────────────────────────────────
# INTERFAZ GRÁFICA TKINTER
# ─────────────────────────────────────────────────────────────────────────────

# Paleta de colores Software FJ
COLORS = {
    "bg_dark":    "#1a1a2e",
    "bg_mid":     "#16213e",
    "bg_card":    "#0f3460",
    "accent":     "#e94560",
    "accent2":    "#533483",
    "text":       "#eaeaea",
    "text_dim":   "#a0a0b0",
    "success":    "#4caf50",
    "warning":    "#ff9800",
    "error":      "#f44336",
    "input_bg":   "#1e2a4a",
    "border":     "#2a4a7f",
    "white":      "#ffffff",
    "row_even":   "#0d2137",
    "row_odd":    "#0f2940",
}

FONT_TITLE  = ("Segoe UI", 16, "bold")
FONT_HEADER = ("Segoe UI", 12, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 9)
FONT_MONO   = ("Consolas", 9)


class AplicacionSoftwareFJ(tk.Tk):
    def __init__(self):
        super().__init__()
        self.gestor = GestorClientes()
        self._configurar_ventana()
        self._construir_ui()
        self._cargar_datos_demo()

    # ─── Configuración ventana ───────────────────────────────────────────
    def _configurar_ventana(self):
        self.title("Software FJ — Gestión de Clientes")
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.configure(bg=COLORS["bg_dark"])
        self.resizable(True, True)
        # Centrar
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 1100) // 2
        y = (self.winfo_screenheight() - 700) // 2
        self.geometry(f"1100x700+{x}+{y}")

    # ─── UI principal ────────────────────────────────────────────────────
    def _construir_ui(self):
        # Header
        self._crear_header()
        # Contenido principal
        main = tk.Frame(self, bg=COLORS["bg_dark"])
        main.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        main.columnconfigure(0, weight=4)
        main.columnconfigure(1, weight=3)
        main.rowconfigure(0, weight=1)
        # Panel izquierdo: tabla
        self._crear_panel_tabla(main)
        # Panel derecho: formulario + acciones
        self._crear_panel_formulario(main)
        # Barra de estado
        self._crear_barra_estado()

    def _crear_header(self):
        hdr = tk.Frame(self, bg=COLORS["bg_card"], height=60)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        tk.Label(hdr, text="⬡  SOFTWARE FJ", font=("Segoe UI", 18, "bold"),
                 bg=COLORS["bg_card"], fg=COLORS["accent"]).pack(side="left", padx=20, pady=10)
        tk.Label(hdr, text="Sistema Integral de Gestión de Clientes",
                 font=FONT_BODY, bg=COLORS["bg_card"], fg=COLORS["text_dim"]).pack(side="left")
        tk.Label(hdr, text=f"UNAD · Programación 213023",
                 font=FONT_SMALL, bg=COLORS["bg_card"], fg=COLORS["text_dim"]).pack(side="right", padx=20)

    def _crear_panel_tabla(self, parent):
        frame = tk.Frame(parent, bg=COLORS["bg_mid"], bd=0)
        frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        # Barra de búsqueda
        search_frame = tk.Frame(frame, bg=COLORS["bg_mid"])
        search_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(search_frame, text="🔍  Buscar:", font=FONT_BODY,
                 bg=COLORS["bg_mid"], fg=COLORS["text"]).pack(side="left")
        self.var_busqueda = tk.StringVar()
        self.var_busqueda.trace_add("write", self._filtrar_tabla)
        entry_bus = tk.Entry(search_frame, textvariable=self.var_busqueda,
                             font=FONT_BODY, bg=COLORS["input_bg"],
                             fg=COLORS["text"], insertbackground=COLORS["accent"],
                             relief="flat", bd=5)
        entry_bus.pack(side="left", fill="x", expand=True, padx=(8, 0))

        # Contador
        self.lbl_contador = tk.Label(frame, text="Clientes: 0",
                                     font=FONT_SMALL, bg=COLORS["bg_mid"],
                                     fg=COLORS["text_dim"])
        self.lbl_contador.pack(anchor="e", padx=12)

        # Tabla con scrollbar
        tabla_frame = tk.Frame(frame, bg=COLORS["bg_mid"])
        tabla_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        cols = ("id", "nombre", "tipo_doc", "cedula", "email", "telefono", "estado")
        self.tabla = ttk.Treeview(tabla_frame, columns=cols, show="headings",
                                  selectmode="browse")

        encabezados = {"id": ("#", 40), "nombre": ("Nombre", 160),
                       "tipo_doc": ("Doc", 55), "cedula": ("Cédula", 100),
                       "email": ("Correo", 170), "telefono": ("Teléfono", 100),
                       "estado": ("Estado", 70)}
        for col, (texto, ancho) in encabezados.items():
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=ancho, minwidth=30)

        scroll_y = ttk.Scrollbar(tabla_frame, orient="vertical",
                                 command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll_y.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")

        self.tabla.bind("<<TreeviewSelect>>", self._al_seleccionar_fila)

        # Estilo tabla
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("Treeview", background=COLORS["row_even"],
                        foreground=COLORS["text"], fieldbackground=COLORS["row_even"],
                        rowheight=26, font=FONT_SMALL)
        style.configure("Treeview.Heading", background=COLORS["bg_card"],
                        foreground=COLORS["accent"], font=("Segoe UI", 9, "bold"))
        style.map("Treeview", background=[("selected", COLORS["accent2"])])
        self.tabla.tag_configure("activo", background=COLORS["row_even"])
        self.tabla.tag_configure("inactivo", background="#1a0a0a",
                                 foreground=COLORS["error"])

        # Botones de acción sobre tabla
        btn_frame = tk.Frame(frame, bg=COLORS["bg_mid"])
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))

        self._boton(btn_frame, "✏  Editar", self._cargar_en_form,
                    COLORS["accent2"]).pack(side="left", padx=4)
        self._boton(btn_frame, "⛔  Desactivar", self._desactivar_seleccionado,
                    COLORS["warning"]).pack(side="left", padx=4)
        self._boton(btn_frame, "✅  Activar", self._activar_seleccionado,
                    COLORS["success"]).pack(side="left", padx=4)
        self._boton(btn_frame, "🗑  Eliminar", self._eliminar_seleccionado,
                    COLORS["error"]).pack(side="left", padx=4)
        self._boton(btn_frame, "📋  Ver Logs", self._ver_logs,
                    COLORS["bg_card"]).pack(side="right", padx=4)

    def _crear_panel_formulario(self, parent):
        frame = tk.Frame(parent, bg=COLORS["bg_mid"])
        frame.grid(row=0, column=1, sticky="nsew")

        # Título
        tk.Label(frame, text="➕  Registrar / Editar Cliente",
                 font=FONT_HEADER, bg=COLORS["bg_mid"],
                 fg=COLORS["accent"]).pack(pady=(15, 5))

        tk.Frame(frame, bg=COLORS["border"], height=1).pack(fill="x", padx=15)

        form = tk.Frame(frame, bg=COLORS["bg_mid"])
        form.pack(fill="both", expand=True, padx=20, pady=10)

        campos = [
            ("Nombre completo *", "nombre"),
            ("Cédula / Documento *", "cedula"),
            ("Correo electrónico *", "email"),
            ("Teléfono *", "telefono"),
        ]

        self.vars_form = {}
        for etiqueta, campo in campos:
            tk.Label(form, text=etiqueta, font=FONT_SMALL,
                     bg=COLORS["bg_mid"], fg=COLORS["text_dim"],
                     anchor="w").pack(fill="x", pady=(8, 2))
            var = tk.StringVar()
            self.vars_form[campo] = var
            entry = tk.Entry(form, textvariable=var, font=FONT_BODY,
                             bg=COLORS["input_bg"], fg=COLORS["text"],
                             insertbackground=COLORS["accent"],
                             relief="flat", bd=6)
            entry.pack(fill="x", ipady=4)

        # Tipo de documento
        tk.Label(form, text="Tipo de documento *", font=FONT_SMALL,
                 bg=COLORS["bg_mid"], fg=COLORS["text_dim"],
                 anchor="w").pack(fill="x", pady=(8, 2))
        self.var_tipo_doc = tk.StringVar(value="CC")
        tipo_combo = ttk.Combobox(form, textvariable=self.var_tipo_doc,
                                  values=Cliente.TIPOS_DOCUMENTO,
                                  state="readonly", font=FONT_BODY)
        tipo_combo.pack(fill="x", ipady=4)

        # Mensaje de estado del formulario
        self.var_msg_form = tk.StringVar()
        self.lbl_msg_form = tk.Label(form, textvariable=self.var_msg_form,
                                     font=FONT_SMALL, bg=COLORS["bg_mid"],
                                     fg=COLORS["error"], wraplength=260,
                                     justify="left")
        self.lbl_msg_form.pack(fill="x", pady=(8, 0))

        # Flag para modo edición
        self._cedula_editando = None

        # Botones formulario
        btn_frame = tk.Frame(frame, bg=COLORS["bg_mid"])
        btn_frame.pack(fill="x", padx=20, pady=10)

        self._boton(btn_frame, "💾  Guardar", self._guardar_cliente,
                    COLORS["accent"], width=14).pack(side="left", padx=(0, 8))
        self._boton(btn_frame, "🔄  Limpiar", self._limpiar_form,
                    COLORS["bg_card"], width=10).pack(side="left")

        # Resumen del cliente seleccionado
        tk.Frame(frame, bg=COLORS["border"], height=1).pack(fill="x", padx=15, pady=(10, 0))
        tk.Label(frame, text="Detalle del cliente seleccionado",
                 font=FONT_SMALL, bg=COLORS["bg_mid"],
                 fg=COLORS["text_dim"]).pack(pady=(6, 0))

        self.txt_detalle = tk.Text(frame, height=7, font=FONT_MONO,
                                   bg=COLORS["bg_dark"], fg=COLORS["text"],
                                   relief="flat", bd=8, state="disabled",
                                   wrap="word")
        self.txt_detalle.pack(fill="both", expand=True, padx=15, pady=(4, 15))

    def _crear_barra_estado(self):
        bar = tk.Frame(self, bg=COLORS["bg_card"], height=28)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)
        self.var_estado = tk.StringVar(value="Sistema listo.")
        tk.Label(bar, textvariable=self.var_estado, font=FONT_SMALL,
                 bg=COLORS["bg_card"], fg=COLORS["text_dim"],
                 anchor="w").pack(side="left", padx=15)
        tk.Label(bar, text=f"Log: {LOG_FILE}", font=FONT_SMALL,
                 bg=COLORS["bg_card"], fg=COLORS["text_dim"]).pack(side="right", padx=15)

    # ─── Helpers UI ──────────────────────────────────────────────────────
    def _boton(self, parent, texto, comando, color, width=None):
        cfg = dict(text=texto, command=comando, font=FONT_SMALL,
                   bg=color, fg=COLORS["white"], relief="flat",
                   activebackground=COLORS["accent"], activeforeground=COLORS["white"],
                   cursor="hand2", padx=10, pady=5)
        if width:
            cfg["width"] = width
        btn = tk.Button(parent, **cfg)
        btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(bg=self._aclarar(c)))
        btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
        return btn

    def _aclarar(self, hex_color: str) -> str:
        r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
        r = min(255, r + 30); g = min(255, g + 30); b = min(255, b + 30)
        return f"#{r:02x}{g:02x}{b:02x}"

    def _set_estado(self, msg: str, color=None):
        self.var_estado.set(msg)
        if color:
            for w in self.winfo_children():
                pass  # solo barra

    # ─── Lógica de tabla ─────────────────────────────────────────────────
    def _actualizar_tabla(self, clientes=None):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        if clientes is None:
            clientes = self.gestor.listar_clientes()

        for i, c in enumerate(clientes):
            estado = "Activo" if c.activo else "Inactivo"
            tag = "activo" if c.activo else "inactivo"
            self.tabla.insert("", "end", iid=c.cedula,
                              values=(c.id_entidad, c.nombre, c.tipo_doc,
                                      c.cedula, c.email, c.telefono, estado),
                              tags=(tag,))

        self.lbl_contador.config(
            text=f"Clientes: {self.gestor.total_clientes}")

    def _filtrar_tabla(self, *_):
        texto = self.var_busqueda.get().strip()
        if not texto:
            self._actualizar_tabla()
            return
        resultados = self.gestor.buscar_por_nombre(texto)
        # También buscar por cédula
        try:
            por_cedula = self.gestor.buscar_por_cedula(texto)
            if por_cedula not in resultados:
                resultados.append(por_cedula)
        except ClienteNoEncontradoError:
            pass
        self._actualizar_tabla(resultados)

    def _al_seleccionar_fila(self, _event=None):
        sel = self.tabla.selection()
        if not sel:
            return
        cedula = sel[0]
        try:
            cliente = self.gestor.buscar_por_cedula(cedula)
            resumen = cliente.obtener_resumen()
            self.txt_detalle.config(state="normal")
            self.txt_detalle.delete("1.0", "end")
            lineas = [
                f"{'─'*40}",
                f"  ID sistema   : {resumen['id']}",
                f"  Nombre       : {resumen['nombre']}",
                f"  Documento    : {resumen['tipo_doc']} {resumen['cedula']}",
                f"  Email        : {resumen['email']}",
                f"  Teléfono     : {resumen['telefono']}",
                f"  Estado       : {'✅ Activo' if resumen['activo'] else '❌ Inactivo'}",
                f"  Registrado   : {resumen['fecha_registro']}",
                f"  Reservas     : {resumen['reservas']}",
                f"{'─'*40}",
            ]
            self.txt_detalle.insert("end", "\n".join(lineas))
            self.txt_detalle.config(state="disabled")
        except ClienteNoEncontradoError:
            pass

    # ─── Acciones de formulario ──────────────────────────────────────────
    def _guardar_cliente(self):
        nombre   = self.vars_form["nombre"].get()
        cedula   = self.vars_form["cedula"].get()
        email    = self.vars_form["email"].get()
        telefono = self.vars_form["telefono"].get()
        tipo_doc = self.var_tipo_doc.get()

        self.var_msg_form.set("")
        try:
            if self._cedula_editando:
                # Modo edición: actualizar email y teléfono
                cliente = self.gestor.buscar_por_cedula(self._cedula_editando)
                cliente.nombre   = nombre
                cliente.email    = email
                cliente.telefono = telefono
                log_evento("INFO", f"Cliente {self._cedula_editando} actualizado.")
                self._set_estado(f"✔ Cliente '{nombre}' actualizado.")
                self._cedula_editando = None
            else:
                self.gestor.registrar_cliente(nombre, cedula, email, telefono, tipo_doc)
                self._set_estado(f"✔ Cliente '{nombre}' registrado correctamente.")

            self._limpiar_form()
            self._actualizar_tabla()
            self.lbl_msg_form.config(fg=COLORS["success"])
            self.var_msg_form.set("✔ Operación exitosa.")

        except ClienteDuplicadoError as e:
            self.var_msg_form.set(f"⚠ {e}")
            self.lbl_msg_form.config(fg=COLORS["warning"])
            log_evento("WARNING", str(e))
        except ClienteInvalidoError as e:
            self.var_msg_form.set(f"✗ {e}")
            self.lbl_msg_form.config(fg=COLORS["error"])
        except SistemaFJError as e:
            self.var_msg_form.set(f"✗ Error del sistema: {e}")
            self.lbl_msg_form.config(fg=COLORS["error"])

    def _limpiar_form(self):
        for var in self.vars_form.values():
            var.set("")
        self.var_tipo_doc.set("CC")
        self.var_msg_form.set("")
        self._cedula_editando = None
        self.txt_detalle.config(state="normal")
        self.txt_detalle.delete("1.0", "end")
        self.txt_detalle.config(state="disabled")

    def _cargar_en_form(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Sin selección", "Seleccione un cliente de la tabla.")
            return
        cedula = sel[0]
        try:
            c = self.gestor.buscar_por_cedula(cedula)
            self.vars_form["nombre"].set(c.nombre)
            self.vars_form["cedula"].set(c.cedula)
            self.vars_form["email"].set(c.email)
            self.vars_form["telefono"].set(c.telefono)
            self.var_tipo_doc.set(c.tipo_doc)
            self._cedula_editando = c.cedula
            self.var_msg_form.set("Modo edición activo — modifique los campos y guarde.")
            self.lbl_msg_form.config(fg=COLORS["warning"])
        except ClienteNoEncontradoError as e:
            messagebox.showerror("Error", str(e))

    def _desactivar_seleccionado(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Sin selección", "Seleccione un cliente.")
            return
        try:
            self.gestor.desactivar_cliente(sel[0])
            self._actualizar_tabla()
            self._set_estado(f"Cliente {sel[0]} desactivado.")
        except (ClienteNoEncontradoError, SistemaFJError) as e:
            messagebox.showerror("Error", str(e))

    def _activar_seleccionado(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Sin selección", "Seleccione un cliente.")
            return
        try:
            self.gestor.activar_cliente(sel[0])
            self._actualizar_tabla()
            self._set_estado(f"Cliente {sel[0]} activado.")
        except (ClienteNoEncontradoError, SistemaFJError) as e:
            messagebox.showerror("Error", str(e))

    def _eliminar_seleccionado(self):
        sel = self.tabla.selection()
        if not sel:
            messagebox.showwarning("Sin selección", "Seleccione un cliente.")
            return
        cedula = sel[0]
        if not messagebox.askyesno("Confirmar", f"¿Eliminar cliente con cédula {cedula}?"):
            return
        try:
            self.gestor.eliminar_cliente(cedula)
            self._actualizar_tabla()
            self._set_estado(f"Cliente {cedula} eliminado.")
        except OperacionNoPermitidaError as e:
            messagebox.showerror("Operación no permitida", str(e))
        except ClienteNoEncontradoError as e:
            messagebox.showerror("No encontrado", str(e))

    # ─── Visor de logs ───────────────────────────────────────────────────
    def _ver_logs(self):
        win = tk.Toplevel(self)
        win.title("📋 Registro de Eventos y Errores")
        win.geometry("750x450")
        win.configure(bg=COLORS["bg_dark"])

        tk.Label(win, text="Archivo de Logs del Sistema",
                 font=FONT_HEADER, bg=COLORS["bg_dark"],
                 fg=COLORS["accent"]).pack(pady=10)

        txt = tk.Text(win, font=FONT_MONO, bg=COLORS["bg_dark"],
                      fg=COLORS["text"], relief="flat", bd=10)
        sc = ttk.Scrollbar(win, command=txt.yview)
        txt.configure(yscrollcommand=sc.set)
        sc.pack(side="right", fill="y")
        txt.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                contenido = f.read()
            txt.insert("end", contenido if contenido else "(Sin registros aún)")
        except FileNotFoundError:
            txt.insert("end", "(Archivo de log aún no creado)")

        txt.config(state="disabled")
        txt.see("end")

        self._boton(win, "Cerrar", win.destroy, COLORS["accent"]).pack(pady=8)

    # ─── Datos de demostración ───────────────────────────────────────────
    def _cargar_datos_demo(self):
        """Simula 10 operaciones completas (válidas e inválidas) como pide el enunciado."""
        demos = [
            # Válidos
            ("María González López",  "1012345678", "maria.gonzalez@gmail.com", "3101234567", "CC"),
            ("Carlos Andrés Ruiz",    "98765432",   "carlos.ruiz@hotmail.com",  "3209876543", "CC"),
            ("Lucía Martínez Peña",   "55443322",   "lucia.m@empresa.co",       "6012345678", "CE"),
            ("Jorge Enrique Salcedo", "1234567890", "j.salcedo@unad.edu.co",    "3154321098", "CC"),
            ("Ana Sofía Torres",      "87654321",   "ana.torres@outlook.com",   "3007654321", "TI"),
        ]
        invalidos = [
            # Cédula corta
            ("Pedro Inválido", "12", "pedro@mail.com", "3100000000", "CC"),
            # Email incorrecto
            ("Luis Fallas", "99887766", "correo-invalido", "3150000000", "CC"),
            # Nombre vacío
            ("", "77665544", "vacio@mail.com", "3160000000", "CC"),
            # Teléfono inválido
            ("Rosa Errónea", "66554433", "rosa@mail.com", "abc", "CC"),
        ]

        for datos in demos:
            try:
                self.gestor.registrar_cliente(*datos)
            except SistemaFJError:
                pass

        for datos in invalidos:
            try:
                self.gestor.registrar_cliente(*datos)
            except (ClienteInvalidoError, SistemaFJError) as e:
                log_evento("ERROR", f"[DEMO-Inválido] {e}")

        # Intentar duplicado
        try:
            self.gestor.registrar_cliente("María Duplicada", "1012345678",
                                           "dup@mail.com", "3000000000", "CC")
        except ClienteDuplicadoError as e:
            log_evento("WARNING", f"[DEMO-Duplicado] {e}")

        self._actualizar_tabla()
        self._set_estado(f"Sistema iniciado con {self.gestor.total_clientes} clientes registrados.")
        log_evento("INFO", "Sistema iniciado. Datos demo cargados.")


# ─────────────────────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = AplicacionSoftwareFJ()
    app.mainloop()