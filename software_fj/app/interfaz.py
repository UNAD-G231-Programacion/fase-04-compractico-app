# app/interfaz.py
"""
Interfaz gráfica básica para el sistema Software FJ.
Autor: Everson Daniel Cumbalaza Benavides
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import sys
import io
import os
import logging

# Importaciones de las clases oficiales del sistema
from .entidades_base import Cliente, ErrorClienteDuplicado, ErrorDatoInvalido
from .servicios import (
    AdminServicios,
    admin_servicios,
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada,
)
from .reservas import Reserva
from .logs import simulacion_integral


class WidgetLogHandler(logging.Handler):
    """Envía mensajes de logging al widget de logs."""

    def __init__(self, widget):
        super().__init__()
        self.widget = widget
        self.setFormatter(logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"))

    def emit(self, record):
        mensaje = self.format(record)

        def agregar():
            if self.widget.winfo_exists():
                self.widget.insert(tk.END, mensaje + "\n")
                self.widget.see(tk.END)
        self.widget.after(0, agregar)


class InterfazSistema:
    """Clase Interfaz de la app"""

    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ - Gestión")
        self.root.geometry("800x550")

        # Notebook (pestañas): Funcion de pestanas en la interfaz tkinter
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # Crear pestañas
        self.crear_pestana_clientes()
        self.crear_pestana_servicios()
        self.crear_pestana_reservas()
        self.crear_pestana_simulacion()
        self.crear_pestana_logs()

        # Configurar logs en ejecucion
        self.configurar_log_handler()
        logging.info("Aplicación iniciada.")

    # -------------------------------------------------------------------------
    # Configuración de logs en vivo
    # -------------------------------------------------------------------------
    def configurar_log_handler(self):
        logger = logging.getLogger()
        handler = WidgetLogHandler(self.texto_logs)
        logger.addHandler(handler)

    # -------------------------------------------------------------------------
    # PESTAÑA CLIENTES
    # -------------------------------------------------------------------------
    def crear_pestana_clientes(self):
        pestana = ttk.Frame(self.notebook)
        self.notebook.add(pestana, text="Clientes")

        # Formulario
        frame = ttk.LabelFrame(pestana, text="Registrar cliente")
        frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame, text="ID:").grid(
            row=0, column=0, sticky="w", padx=2, pady=2)
        self.entry_id = ttk.Entry(frame, width=15)
        self.entry_id.grid(row=0, column=1, padx=2, pady=2)

        ttk.Label(frame, text="Nombre:").grid(
            row=1, column=0, sticky="w", padx=2, pady=2)
        self.entry_nombre = ttk.Entry(frame, width=30)
        self.entry_nombre.grid(row=1, column=1, padx=2, pady=2)

        ttk.Label(frame, text="Correo:").grid(
            row=2, column=0, sticky="w", padx=2, pady=2)
        self.entry_correo = ttk.Entry(frame, width=30)
        self.entry_correo.grid(row=2, column=1, padx=2, pady=2)

        ttk.Label(frame, text="Teléfono:").grid(
            row=3, column=0, sticky="w", padx=2, pady=2)
        self.entry_telefono = ttk.Entry(frame, width=15)
        self.entry_telefono.grid(row=3, column=1, padx=2, pady=2)

        ttk.Button(frame, text="Agregar Cliente", command=self.agregar_cliente).grid(
            row=4, column=0, columnspan=2, pady=5)

        # Label de busqueda
        ttk.Label(pestana, text="Buscar:").pack(
            anchor="w", padx=5, pady=(5, 0))
        self.busqueda_cliente = ttk.Entry(pestana, width=30)
        self.busqueda_cliente.pack(fill="x", padx=5, pady=(0, 5))
        self.busqueda_cliente.bind("<KeyRelease>", self.filtrar_clientes)

        # Lista
        self.tree_clientes = ttk.Treeview(pestana, columns=(
            "ID", "Nombre", "Correo", "Teléfono"), show="headings", height=8)
        self.tree_clientes.heading("ID", text="ID")
        self.tree_clientes.heading("Nombre", text="Nombre")
        self.tree_clientes.heading("Correo", text="Correo")
        self.tree_clientes.heading("Teléfono", text="Teléfono")
        self.tree_clientes.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        ttk.Button(pestana, text="Actualizar lista",
                   command=self.cargar_clientes).pack(pady=(0, 5))

        self.cargar_clientes()

    def agregar_cliente(self):
        id_cliente = self.entry_id.get().strip()
        nombre = self.entry_nombre.get().strip()
        correo = self.entry_correo.get().strip()
        telefono = self.entry_telefono.get().strip()
        if not all([id_cliente, nombre, correo, telefono]):
            messagebox.showerror("Error", "Complete todos los campos.")
            return
        try:
            cliente = Cliente(id_cliente, nombre, correo, telefono)
            Cliente.agregar_cliente(cliente)
            messagebox.showinfo("Éxito", f"Cliente '{nombre}' registrado.")
            logging.info(f"Cliente registrado: {cliente.describir()}")
            for entry in (self.entry_id, self.entry_nombre, self.entry_correo, self.entry_telefono):
                entry.delete(0, tk.END)
            self.cargar_clientes()
            self.actualizar_combos_reservas()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            logging.error(f"Error al registrar cliente: {e}")

    def cargar_clientes(self):
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        for cliente in Cliente.listar_clientes():
            self.tree_clientes.insert("", "end", values=(
                cliente.id_entidad, cliente.nombre, cliente.correo, cliente.telefono))

    def filtrar_clientes(self, event=None):
        filtro = self.busqueda_cliente.get().strip().lower()
        self.tree_clientes.delete(*self.tree_clientes.get_children())
        for cliente in Cliente.listar_clientes():
            if filtro in cliente.nombre.lower() or filtro in cliente.id_entidad.lower():
                self.tree_clientes.insert("", "end", values=(
                    cliente.id_entidad, cliente.nombre, cliente.correo, cliente.telefono))

    # -------------------------------------------------------------------------
    # PESTAÑA SERVICIOS
    # -------------------------------------------------------------------------
    def crear_pestana_servicios(self):
        pestana = ttk.Frame(self.notebook)
        self.notebook.add(pestana, text="Servicios")

        frame = ttk.LabelFrame(pestana, text="Agregar servicio")
        frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame, text="Tipo:").grid(
            row=0, column=0, sticky="w", padx=2, pady=2)
        self.tipo_var = tk.StringVar()
        combo = ttk.Combobox(frame, textvariable=self.tipo_var,
                             values=[
                                 "Reserva de Salas", "Alquiler de Equipo", "Asesoría Especializada"],
                             state="readonly", width=25)
        combo.grid(row=0, column=1, padx=2, pady=2)
        combo.current(0)

        ttk.Label(frame, text="Costo base:").grid(
            row=1, column=0, sticky="w", padx=2, pady=2)
        self.entry_costo = ttk.Entry(frame, width=15)
        self.entry_costo.grid(row=1, column=1, padx=2, pady=2, sticky="w")

        ttk.Label(frame, text="IVA (%):").grid(
            row=2, column=0, sticky="w", padx=2, pady=2)
        self.entry_iva = ttk.Entry(frame, width=10)
        self.entry_iva.grid(row=2, column=1, padx=2, pady=2, sticky="w")

        ttk.Label(frame, text="Descuento (%):").grid(
            row=3, column=0, sticky="w", padx=2, pady=2)
        self.entry_descuento = ttk.Entry(frame, width=10)
        self.entry_descuento.grid(row=3, column=1, padx=2, pady=2, sticky="w")

        ttk.Button(frame, text="Agregar Servicio", command=self.agregar_servicio).grid(
            row=4, column=0, columnspan=2, pady=5)

        # Búsqueda
        ttk.Label(pestana, text="Buscar:").pack(
            anchor="w", padx=5, pady=(5, 0))
        self.busqueda_servicio = ttk.Entry(pestana, width=30)
        self.busqueda_servicio.pack(fill="x", padx=5, pady=(0, 5))
        self.busqueda_servicio.bind("<KeyRelease>", self.filtrar_servicios)

        self.tree_servicios = ttk.Treeview(pestana, columns=(
            "ID", "Tipo", "Costo", "IVA", "Desc."), show="headings", height=8)
        for col in ("ID", "Tipo", "Costo", "IVA", "Desc."):
            self.tree_servicios.heading(col, text=col)
        self.tree_servicios.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        ttk.Button(pestana, text="Actualizar lista",
                   command=self.cargar_servicios).pack(pady=(0, 5))
        self.cargar_servicios()

    def agregar_servicio(self):
        tipo = self.tipo_var.get()
        try:
            costo = float(self.entry_costo.get())
            iva = float(self.entry_iva.get())
            descuento = float(self.entry_descuento.get())
        except ValueError:
            messagebox.showerror(
                "Error", "Costo, IVA y Descuento deben ser números.")
            return
        repositorio = admin_servicios.servicios
        try:
            if tipo == "Reserva de Salas":
                servicio = ReservaSala(costo, iva, descuento, repositorio)
            elif tipo == "Alquiler de Equipo":
                servicio = AlquilerEquipo(costo, iva, descuento, repositorio)
            elif tipo == "Asesoría Especializada":
                servicio = AsesoriaEspecializada(
                    costo, iva, descuento, repositorio)
            else:
                messagebox.showerror("Error", "Tipo no válido.")
                return
            if admin_servicios.agregar_servicio(servicio):
                messagebox.showinfo(
                    "Éxito", f"Servicio '{servicio.nombre_servicio}' agregado.")
                logging.info(f"Servicio creado: {servicio.mostrar_info()}")
                self.cargar_servicios()
                self.actualizar_combos_reservas()
            else:
                messagebox.showerror("Error", "Servicio duplicado.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            logging.error(f"Error al crear servicio: {e}")

    def cargar_servicios(self):
        for item in self.tree_servicios.get_children():
            self.tree_servicios.delete(item)
        for s in admin_servicios.servicios.values():
            self.tree_servicios.insert("", "end", values=(
                s.id_servicio,
                s.__class__.__name__,
                f"${s.costo_servicio:.2f}",
                f"{s.valor_iva * 100:.1f}%",
                f"{s.valor_desc * 100:.1f}%"
            ))

    def filtrar_servicios(self, event=None):
        filtro = self.busqueda_servicio.get().strip().lower()
        self.tree_servicios.delete(*self.tree_servicios.get_children())
        for s in admin_servicios.servicios.values():
            if filtro in s.id_servicio.lower() or filtro in s.__class__.__name__.lower():
                self.tree_servicios.insert("", "end", values=(
                    s.id_servicio,
                    s.__class__.__name__,
                    f"${s.costo_servicio:.2f}",
                    f"{s.valor_iva * 100:.1f}%",
                    f"{s.valor_desc * 100:.1f}%"
                ))

    # -------------------------------------------------------------------------
    # PESTAÑA RESERVAS
    # -------------------------------------------------------------------------
    def crear_pestana_reservas(self):
        pestana = ttk.Frame(self.notebook)
        self.notebook.add(pestana, text="Reservas")

        frame = ttk.LabelFrame(pestana, text="Nueva reserva")
        frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame, text="Cliente:").grid(
            row=0, column=0, sticky="w", padx=2, pady=2)
        self.combo_cliente = ttk.Combobox(frame, state="readonly", width=30)
        self.combo_cliente.grid(row=0, column=1, padx=2, pady=2)

        ttk.Label(frame, text="Servicio:").grid(
            row=1, column=0, sticky="w", padx=2, pady=2)
        self.combo_servicio = ttk.Combobox(frame, state="readonly", width=30)
        self.combo_servicio.grid(row=1, column=1, padx=2, pady=2)

        ttk.Label(frame, text="Duración (horas/días):").grid(row=2,
                                                             column=0, sticky="w", padx=2, pady=2)
        self.entry_duracion = ttk.Entry(frame, width=10)
        self.entry_duracion.grid(row=2, column=1, padx=2, pady=2, sticky="w")

        ttk.Button(frame, text="Crear Reserva", command=self.crear_reserva).grid(
            row=3, column=0, columnspan=2, pady=5)

        # Acciones
        frame_acciones = ttk.LabelFrame(pestana, text="Acciones")
        frame_acciones.pack(fill="x", padx=5, pady=5)
        self.btn_confirmar = ttk.Button(
            frame_acciones, text="Confirmar", command=self.confirmar_reserva, state="disabled")
        self.btn_confirmar.pack(side="left", padx=2, pady=2)
        self.btn_procesar = ttk.Button(
            frame_acciones, text="Procesar", command=self.procesar_reserva, state="disabled")
        self.btn_procesar.pack(side="left", padx=2, pady=2)
        self.btn_cancelar = ttk.Button(
            frame_acciones, text="Cancelar", command=self.cancelar_reserva, state="disabled")
        self.btn_cancelar.pack(side="left", padx=2, pady=2)

        self.tree_reservas = ttk.Treeview(pestana, columns=(
            "ID", "Cliente", "Servicio", "Dur.", "Estado", "Costo"), show="headings", height=8)
        for col in ("ID", "Cliente", "Servicio", "Dur.", "Estado", "Costo"):
            self.tree_reservas.heading(col, text=col)
        self.tree_reservas.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        self.tree_reservas.bind("<<TreeviewSelect>>",
                                self.al_seleccionar_reserva)

        ttk.Button(pestana, text="Actualizar lista",
                   command=self.cargar_reservas).pack(pady=(0, 5))

        self.actualizar_combos_reservas()
        self.cargar_reservas()

    def actualizar_combos_reservas(self):
        clientes = [
            f"{c.id_entidad} - {c.nombre}" for c in Cliente.listar_clientes()]
        self.combo_cliente["values"] = clientes
        if clientes:
            self.combo_cliente.current(0)
        servicios = [
            f"{s.id_servicio} - {s.__class__.__name__}" for s in admin_servicios.servicios.values()]
        self.combo_servicio["values"] = servicios
        if servicios:
            self.combo_servicio.current(0)

    def _obtener_id_desde_combo(self, texto):
        return texto.split(" - ")[0].strip() if texto else None

    def crear_reserva(self):
        texto_cliente = self.combo_cliente.get()
        texto_servicio = self.combo_servicio.get()
        duracion_str = self.entry_duracion.get()
        if not texto_cliente or not texto_servicio or not duracion_str:
            messagebox.showerror(
                "Error", "Seleccione cliente, servicio y duración.")
            return
        try:
            duracion = float(duracion_str)
        except ValueError:
            messagebox.showerror("Error", "Duración debe ser un número.")
            return
        try:
            id_cliente = self._obtener_id_desde_combo(texto_cliente)
            id_servicio = self._obtener_id_desde_combo(texto_servicio)
            cliente = Cliente.buscar_cliente(id_cliente)
            servicio = admin_servicios.obtener_servicio(id_servicio)
            reserva = Reserva(cliente, servicio, duracion)
            messagebox.showinfo(
                "Éxito", f"Reserva {reserva.id_entidad} creada (pendiente).")
            logging.info(f"Reserva creada: {reserva.id_entidad}")
            self.cargar_reservas()
            self.entry_duracion.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            logging.error(f"Error al crear reserva: {e}")

    def al_seleccionar_reserva(self, event):
        seleccion = self.tree_reservas.selection()
        if seleccion:
            reserva = self._obtener_reserva_seleccionada()
            if reserva:
                estado = reserva.estado
                if estado == Reserva.ESTADO_PENDIENTE:
                    self.btn_confirmar["state"] = "normal"
                    self.btn_procesar["state"] = "disabled"
                    self.btn_cancelar["state"] = "normal"
                elif estado == Reserva.ESTADO_CONFIRMADA:
                    self.btn_confirmar["state"] = "disabled"
                    self.btn_procesar["state"] = "normal"
                    self.btn_cancelar["state"] = "normal"
                elif estado == Reserva.ESTADO_PROCESADA:
                    self.btn_confirmar["state"] = "disabled"
                    self.btn_procesar["state"] = "disabled"
                    self.btn_cancelar["state"] = "disabled"
                elif estado == Reserva.ESTADO_CANCELADA:
                    self.btn_confirmar["state"] = "disabled"
                    self.btn_procesar["state"] = "disabled"
                    self.btn_cancelar["state"] = "disabled"
                return
        self.btn_confirmar["state"] = "disabled"
        self.btn_procesar["state"] = "disabled"
        self.btn_cancelar["state"] = "disabled"

    def _obtener_reserva_seleccionada(self):
        sel = self.tree_reservas.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione una reserva.")
            return None
        id_reserva = self.tree_reservas.item(sel[0], "values")[0]
        return Reserva._reservas.get(id_reserva)

    def confirmar_reserva(self):
        r = self._obtener_reserva_seleccionada()
        if r:
            try:
                r.confirmar()
                messagebox.showinfo("Éxito", "Reserva confirmada.")
                logging.info(f"Reserva confirmada: {r.id_entidad}")
                self.cargar_reservas()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                logging.error(f"Error al confirmar: {e}")

    def procesar_reserva(self):
        r = self._obtener_reserva_seleccionada()
        if r:
            try:
                r.procesar()
                messagebox.showinfo("Éxito", "Reserva procesada.")
                logging.info(f"Reserva procesada: {r.id_entidad}")
                self.cargar_reservas()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                logging.error(f"Error al procesar: {e}")

    def cancelar_reserva(self):
        r = self._obtener_reserva_seleccionada()
        if r:
            try:
                r.cancelar()
                messagebox.showinfo("Éxito", "Reserva cancelada.")
                logging.info(f"Reserva cancelada: {r.id_entidad}")
                self.cargar_reservas()
            except Exception as e:
                messagebox.showerror("Error", str(e))
                logging.error(f"Error al cancelar: {e}")

    def cargar_reservas(self):
        for item in self.tree_reservas.get_children():
            self.tree_reservas.delete(item)
        for r in Reserva._reservas.values():
            costo_str = "N/A"
            if r.estado in (Reserva.ESTADO_CONFIRMADA, Reserva.ESTADO_PROCESADA):
                unitario = r.servicio.calcular_costo_servicio(
                    iva_ok=True, disc_ok=True)
                costo_str = f"${unitario * r.duracion:.2f}"
            self.tree_reservas.insert("", "end", values=(
                r.id_entidad, r.cliente.nombre, r.servicio.__class__.__name__,
                f"{r.duracion}", r.estado, costo_str
            ))
        self.actualizar_combos_reservas()

    # -------------------------------------------------------------------------
    # PESTAÑA SIMULACIÓN
    # -------------------------------------------------------------------------
    def crear_pestana_simulacion(self):
        pestana = ttk.Frame(self.notebook)
        self.notebook.add(pestana, text="Simulacion")

        ttk.Button(pestana, text="Ejecutar Simulacion",
                   command=self.ejecutar_simulacion).pack(pady=10)

        self.texto_simulacion = scrolledtext.ScrolledText(
            pestana, wrap="word", width=90, height=20)
        self.texto_simulacion.pack(
            fill="both", expand=True, padx=5, pady=(0, 5))

    def ejecutar_simulacion(self):
        self.texto_simulacion.delete("1.0", tk.END)
        self.texto_simulacion.insert(tk.END, "Ejecutando simulación...\n\n")
        self.texto_simulacion.update()
        viejo_stdout = sys.stdout
        buffer = io.StringIO()
        sys.stdout = buffer
        try:
            simulacion_integral()
        except Exception as e:
            print(f"\n*** ERROR: {e} ***")
        finally:
            sys.stdout = viejo_stdout
            self.texto_simulacion.insert(tk.END, buffer.getvalue())
            self.texto_simulacion.see(tk.END)
        logging.info("Simulación integral ejecutada.")

    # -------------------------------------------------------------------------
    # PESTAÑA LOGS
    # -------------------------------------------------------------------------
    def crear_pestana_logs(self):
        pestana = ttk.Frame(self.notebook)
        self.notebook.add(pestana, text="Logs")

        frame_botones = ttk.Frame(pestana)
        frame_botones.pack(fill="x", padx=5, pady=5)

        ttk.Button(frame_botones, text="Recargar archivo",
                   command=self.actualizar_logs_archivo).pack(side="left", padx=2)
        ttk.Button(frame_botones, text="Limpiar ventana",
                   command=self.limpiar_logs_window).pack(side="left", padx=2)
        ttk.Button(frame_botones, text="Exportar...",
                   command=self.exportar_logs).pack(side="left", padx=2)

        self.texto_logs = scrolledtext.ScrolledText(
            pestana, wrap="word", width=90, height=20)
        self.texto_logs.pack(fill="both", expand=True, padx=5, pady=(0, 5))

        self.actualizar_logs_archivo()

    def actualizar_logs_archivo(self):
        self.texto_logs.delete("1.0", tk.END)
        ruta = os.path.join(os.path.dirname(__file__),
                            "..", "logs", "sistema.log")
        if os.path.exists(ruta):
            with open(ruta, "r", encoding="utf-8") as f:
                self.texto_logs.insert(tk.END, f.read())
        else:
            self.texto_logs.insert(tk.END, "No hay logs aún.")
        self.texto_logs.see(tk.END)

    def limpiar_logs_window(self):
        # limpia la ventana de logs
        self.texto_logs.delete("1.0", tk.END)
        logging.info("Ventana de logs limpiada.")

    def exportar_logs(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".log", filetypes=[
                                            ("Logs", "*.log"), ("Texto", "*.txt")])
        if ruta:
            try:
                with open(ruta, "w", encoding="utf-8") as f:
                    f.write(self.texto_logs.get("1.0", tk.END))
                messagebox.showinfo("Listo", f"Logs exportados a {ruta}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar: {e}")
