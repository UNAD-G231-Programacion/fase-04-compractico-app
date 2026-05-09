# app/interfaz.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import io
import os
import logging  # <-- nuevo

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


# Handler personalizado para redirigir logs al widget de la pestaña Logs
class WidgetLogHandler(logging.Handler):
    """Handler que envía los mensajes de logging a un widget Text."""

    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def emit(self, record):
        mensaje = self.format(record)
        # Insertar en el widget de forma segura desde cualquier hilo

        def agregar():
            self.widget.insert(tk.END, mensaje + "\n")
            self.widget.see(tk.END)
        # Programar la inserción en el hilo principal de Tkinter
        if self.widget.winfo_exists():
            self.widget.after(0, agregar)


class InterfazSistema:
    """Ventana principal del sistema Software FJ."""

    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ - Gestión")
        self.root.geometry("800x550")

        # Notebook (pestañas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # Crear las pestañas (logs se crea después porque necesitamos el widget antes del handler)
        self.crear_pestana_clientes()
        self.crear_pestana_servicios()
        self.crear_pestana_reservas()
        self.crear_pestana_simulacion()
        self.crear_pestana_logs()

        # Configurar el handler de logs para mostrar en la pestaña logs
        self.configurar_log_handler()

    # --------------------- Configuración de logs en vivo -----------------
    def configurar_log_handler(self):
        """Añade un handler al logger raíz para mostrar mensajes en la pestaña Logs."""
        logger = logging.getLogger()  # Obtiene el logger raíz, el mismo que usa basicConfig
        # Creamos un formateador similar al del archivo (sin fecha para ahorrar espacio en la UI)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s")
        handler = WidgetLogHandler(self.texto_logs)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        # También registramos un mensaje de inicio
        logging.info("Sistema iniciado. Logs en tiempo real activados.")

    # --------------------- PESTAÑA CLIENTES ---------------------
    def crear_pestana_clientes(self):
        pestana = ttk.Frame(self.notebook)
        self.notebook.add(pestana, text="Clientes")

        frame = ttk.LabelFrame(pestana, text="Registrar cliente")
        frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame, text="ID:").grid(
            row=0, column=0, sticky="w", padx=3, pady=2)
        self.entry_id = ttk.Entry(frame, width=15)
        self.entry_id.grid(row=0, column=1, padx=3, pady=2)

        ttk.Label(frame, text="Nombre:").grid(
            row=1, column=0, sticky="w", padx=3, pady=2)
        self.entry_nombre = ttk.Entry(frame, width=25)
        self.entry_nombre.grid(row=1, column=1, padx=3, pady=2)

        ttk.Label(frame, text="Correo:").grid(
            row=2, column=0, sticky="w", padx=3, pady=2)
        self.entry_correo = ttk.Entry(frame, width=25)
        self.entry_correo.grid(row=2, column=1, padx=3, pady=2)

        ttk.Label(frame, text="Teléfono:").grid(
            row=3, column=0, sticky="w", padx=3, pady=2)
        self.entry_telefono = ttk.Entry(frame, width=15)
        self.entry_telefono.grid(row=3, column=1, padx=3, pady=2)

        btn_agregar = ttk.Button(
            frame, text="Agregar Cliente", command=self.agregar_cliente)
        btn_agregar.grid(row=4, column=0, columnspan=2, pady=5)

        self.tree_clientes = ttk.Treeview(pestana, columns=(
            "ID", "Nombre", "Correo", "Teléfono"), show="headings", height=8)
        self.tree_clientes.heading("ID", text="ID")
        self.tree_clientes.heading("Nombre", text="Nombre")
        self.tree_clientes.heading("Correo", text="Correo")
        self.tree_clientes.heading("Teléfono", text="Teléfono")
        self.tree_clientes.pack(fill="both", expand=True, padx=5, pady=5)

        btn_refrescar = ttk.Button(
            pestana, text="Actualizar lista", command=self.actualizar_lista_clientes)
        btn_refrescar.pack(pady=3)

        self.actualizar_lista_clientes()

    def agregar_cliente(self):
        id_cliente = self.entry_id.get().strip()
        nombre = self.entry_nombre.get().strip()
        correo = self.entry_correo.get().strip()
        telefono = self.entry_telefono.get().strip()
        if not id_cliente or not nombre or not correo or not telefono:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            logging.warning(
                "Intento de registro de cliente con campos vacíos.")  # registro
            return
        try:
            cliente = Cliente(id_cliente, nombre, correo, telefono)
            Cliente.agregar_cliente(cliente)
            messagebox.showinfo("Éxito", f"Cliente '{nombre}' registrado.")
            # registro
            logging.info(f"Cliente registrado: {cliente.describir()}")
            self.entry_id.delete(0, tk.END)
            self.entry_nombre.delete(0, tk.END)
            self.entry_correo.delete(0, tk.END)
            self.entry_telefono.delete(0, tk.END)
            self.actualizar_lista_clientes()
            self.actualizar_combos_reservas()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            logging.error(f"Error al registrar cliente: {e}")  # registro

    def actualizar_lista_clientes(self):
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        for cliente in Cliente.listar_clientes():
            self.tree_clientes.insert("", "end", values=(
                cliente.id_entidad, cliente.nombre, cliente.correo, cliente.telefono))

    # --------------------- PESTAÑA SERVICIOS --------------------
    def crear_pestana_servicios(self):
        pestana = ttk.Frame(self.notebook)
        self.notebook.add(pestana, text="Servicios")

        frame = ttk.LabelFrame(pestana, text="Agregar servicio")
        frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame, text="Tipo:").grid(
            row=0, column=0, sticky="w", padx=3, pady=2)
        self.tipo_var = tk.StringVar()
        combo_tipo = ttk.Combobox(frame, textvariable=self.tipo_var,
                                  values=[
                                      "Reserva de Salas", "Alquiler de Equipo", "Asesoría Especializada"],
                                  state="readonly", width=22)
        combo_tipo.grid(row=0, column=1, padx=3, pady=2)
        combo_tipo.current(0)

        ttk.Label(frame, text="Costo base:").grid(
            row=1, column=0, sticky="w", padx=3, pady=2)
        self.entry_costo = ttk.Entry(frame, width=15)
        self.entry_costo.grid(row=1, column=1, padx=3, pady=2)

        ttk.Label(frame, text="IVA (%):").grid(
            row=2, column=0, sticky="w", padx=3, pady=2)
        self.entry_iva = ttk.Entry(frame, width=15)
        self.entry_iva.grid(row=2, column=1, padx=3, pady=2)

        ttk.Label(frame, text="Descuento (%):").grid(
            row=3, column=0, sticky="w", padx=3, pady=2)
        self.entry_descuento = ttk.Entry(frame, width=15)
        self.entry_descuento.grid(row=3, column=1, padx=3, pady=2)

        btn_agregar = ttk.Button(
            frame, text="Agregar Servicio", command=self.agregar_servicio)
        btn_agregar.grid(row=4, column=0, columnspan=2, pady=5)

        self.tree_servicios = ttk.Treeview(pestana, columns=(
            "ID", "Tipo", "Costo", "IVA", "Desc."), show="headings", height=8)
        self.tree_servicios.heading("ID", text="ID")
        self.tree_servicios.heading("Tipo", text="Tipo")
        self.tree_servicios.heading("Costo", text="Costo base")
        self.tree_servicios.heading("IVA", text="IVA")
        self.tree_servicios.heading("Desc.", text="Desc.")
        self.tree_servicios.pack(fill="both", expand=True, padx=5, pady=5)

        btn_refrescar = ttk.Button(
            pestana, text="Actualizar lista", command=self.actualizar_lista_servicios)
        btn_refrescar.pack(pady=3)

        self.actualizar_lista_servicios()

    def agregar_servicio(self):
        tipo = self.tipo_var.get()
        try:
            costo = float(self.entry_costo.get())
            iva = float(self.entry_iva.get())
            descuento = float(self.entry_descuento.get())
        except ValueError:
            messagebox.showerror(
                "Error", "Costo, IVA y Descuento deben ser números.")
            logging.warning(
                "Intento de crear servicio con valores no numéricos.")  # registro
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
                # registro
                logging.info(f"Servicio creado: {servicio.mostrar_info()}")
                self.actualizar_lista_servicios()
                self.actualizar_combos_reservas()
            else:
                messagebox.showerror(
                    "Error", "No se pudo agregar el servicio.")
                logging.warning(
                    # registro
                    f"No se pudo agregar servicio ID {servicio.id_servicio} (posible duplicado).")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            logging.error(f"Error al crear servicio: {e}")  # registro

    def actualizar_lista_servicios(self):
        for item in self.tree_servicios.get_children():
            self.tree_servicios.delete(item)
        for servicio in admin_servicios.servicios.values():
            self.tree_servicios.insert("", "end", values=(
                servicio.id_servicio,
                servicio.__class__.__name__,
                f"${servicio.costo_servicio:.2f}",
                f"{servicio.valor_iva * 100:.1f}%",
                f"{servicio.valor_desc * 100:.1f}%"
            ))

    # --------------------- PESTAÑA RESERVAS ---------------------
    def crear_pestana_reservas(self):
        pestana = ttk.Frame(self.notebook)
        self.notebook.add(pestana, text="Reservas")

        frame = ttk.LabelFrame(pestana, text="Nueva reserva")
        frame.pack(fill="x", padx=5, pady=5)

        ttk.Label(frame, text="Cliente:").grid(
            row=0, column=0, sticky="w", padx=3, pady=2)
        self.combo_cliente = ttk.Combobox(frame, state="readonly", width=30)
        self.combo_cliente.grid(row=0, column=1, padx=3, pady=2)

        ttk.Label(frame, text="Servicio:").grid(
            row=1, column=0, sticky="w", padx=3, pady=2)
        self.combo_servicio = ttk.Combobox(frame, state="readonly", width=30)
        self.combo_servicio.grid(row=1, column=1, padx=3, pady=2)

        ttk.Label(frame, text="Duración (horas/días):").grid(row=2,
                                                             column=0, sticky="w", padx=3, pady=2)
        self.entry_duracion = ttk.Entry(frame, width=10)
        self.entry_duracion.grid(row=2, column=1, padx=3, pady=2, sticky="w")

        btn_crear = ttk.Button(frame, text="Crear Reserva",
                               command=self.crear_reserva)
        btn_crear.grid(row=3, column=0, columnspan=2, pady=5)

        frame_acciones = ttk.LabelFrame(
            pestana, text="Acciones sobre reserva seleccionada")
        frame_acciones.pack(fill="x", padx=5, pady=5)

        self.btn_confirmar = ttk.Button(
            frame_acciones, text="Confirmar", command=self.confirmar_reserva, state="disabled")
        self.btn_confirmar.pack(side="left", padx=3, pady=3)

        self.btn_procesar = ttk.Button(
            frame_acciones, text="Procesar", command=self.procesar_reserva, state="disabled")
        self.btn_procesar.pack(side="left", padx=3, pady=3)

        self.btn_cancelar = ttk.Button(
            frame_acciones, text="Cancelar", command=self.cancelar_reserva, state="disabled")
        self.btn_cancelar.pack(side="left", padx=3, pady=3)

        self.tree_reservas = ttk.Treeview(pestana, columns=(
            "ID", "Cliente", "Servicio", "Dur.", "Estado", "Costo"), show="headings", height=8)
        self.tree_reservas.heading("ID", text="ID")
        self.tree_reservas.heading("Cliente", text="Cliente")
        self.tree_reservas.heading("Servicio", text="Servicio")
        self.tree_reservas.heading("Dur.", text="Dur.")
        self.tree_reservas.heading("Estado", text="Estado")
        self.tree_reservas.heading("Costo", text="Costo total")
        self.tree_reservas.pack(fill="both", expand=True, padx=5, pady=5)

        self.tree_reservas.bind("<<TreeviewSelect>>",
                                self.al_seleccionar_reserva)

        btn_refrescar = ttk.Button(
            pestana, text="Actualizar lista", command=self.actualizar_lista_reservas)
        btn_refrescar.pack(pady=3)

        self.actualizar_combos_reservas()
        self.actualizar_lista_reservas()

    def actualizar_combos_reservas(self):
        clientes = [
            f"{c.id_entidad} - {c.nombre}" for c in Cliente.listar_clientes()]
        self.combo_cliente["values"] = clientes
        if clientes:
            self.combo_cliente.current(0)

        servicios = []
        for s in admin_servicios.servicios.values():
            servicios.append(f"{s.id_servicio} - {s.__class__.__name__}")
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
            logging.warning("Intento de crear reserva sin datos completos.")
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
            nueva_reserva = Reserva(cliente, servicio, duracion)
            messagebox.showinfo(
                "Éxito", f"Reserva {nueva_reserva.id_entidad} creada (pendiente).")
            logging.info(f"Reserva creada: {nueva_reserva.describir()}")
            self.actualizar_lista_reservas()
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
        seleccion = self.tree_reservas.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Seleccione una reserva.")
            return None
        id_reserva = self.tree_reservas.item(seleccion[0], "values")[0]
        return Reserva._reservas.get(id_reserva)

    def confirmar_reserva(self):
        reserva = self._obtener_reserva_seleccionada()
        if reserva:
            try:
                reserva.confirmar()
                messagebox.showinfo("Éxito", "Reserva confirmada.")
                logging.info(f"Reserva confirmada: {reserva.id_entidad}")
                self.actualizar_lista_reservas()
                self.al_seleccionar_reserva(None)
            except Exception as e:
                messagebox.showerror("Error", str(e))
                logging.error(f"Error al confirmar reserva: {e}")

    def procesar_reserva(self):
        reserva = self._obtener_reserva_seleccionada()
        if reserva:
            try:
                reserva.procesar()
                messagebox.showinfo("Éxito", "Reserva procesada.")
                logging.info(f"Reserva procesada: {reserva.id_entidad}")
                self.actualizar_lista_reservas()
                self.al_seleccionar_reserva(None)
            except Exception as e:
                messagebox.showerror("Error", str(e))
                logging.error(f"Error al procesar reserva: {e}")

    def cancelar_reserva(self):
        reserva = self._obtener_reserva_seleccionada()
        if reserva:
            try:
                reserva.cancelar()
                messagebox.showinfo("Éxito", "Reserva cancelada.")
                logging.info(f"Reserva cancelada: {reserva.id_entidad}")
                self.actualizar_lista_reservas()
                self.al_seleccionar_reserva(None)
            except Exception as e:
                messagebox.showerror("Error", str(e))
                logging.error(f"Error al cancelar reserva: {e}")

    def actualizar_lista_reservas(self):
        for item in self.tree_reservas.get_children():
            self.tree_reservas.delete(item)
        for reserva in Reserva._reservas.values():
            costo_str = "N/A"
            if reserva.estado in (Reserva.ESTADO_CONFIRMADA, Reserva.ESTADO_PROCESADA):
                unitario = reserva.servicio.calcular_costo_servicio(
                    iva_ok=True, disc_ok=True)
                costo_str = f"${unitario * reserva.duracion:.2f}"
            self.tree_reservas.insert("", "end", values=(
                reserva.id_entidad,
                reserva.cliente.nombre,
                reserva.servicio.__class__.__name__,
                f"{reserva.duracion}",
                reserva.estado,
                costo_str
            ))

    # --------------------- PESTAÑA SIMULACIÓN --------------------
    def crear_pestana_simulacion(self):
        pestana = ttk.Frame(self.notebook)
        self.notebook.add(pestana, text="Simulación")

        btn_simular = ttk.Button(
            pestana, text="Ejecutar Simulación Integral", command=self.ejecutar_simulacion)
        btn_simular.pack(pady=5)

        self.texto_simulacion = scrolledtext.ScrolledText(
            pestana, wrap=tk.WORD, width=90, height=20)
        self.texto_simulacion.pack(fill="both", expand=True, padx=5, pady=5)

    def ejecutar_simulacion(self):
        self.texto_simulacion.delete("1.0", tk.END)
        viejo_stdout = sys.stdout
        buffer = io.StringIO()
        sys.stdout = buffer
        try:
            simulacion_integral()
        except Exception as e:
            print(f"\n*** ERROR DURANTE LA SIMULACIÓN: {e} ***")
        finally:
            sys.stdout = viejo_stdout
            self.texto_simulacion.insert(tk.END, buffer.getvalue())
            self.texto_simulacion.see(tk.END)

    # --------------------- PESTAÑA LOGS (con limpiar) ------------
    def crear_pestana_logs(self):
        pestana = ttk.Frame(self.notebook)
        self.notebook.add(pestana, text="Logs")

        frame_botones = ttk.Frame(pestana)
        frame_botones.pack(fill="x", pady=5)

        btn_actualizar = ttk.Button(
            frame_botones, text="Actualizar desde archivo", command=self.actualizar_logs)
        btn_actualizar.pack(side="left", padx=5)

        btn_limpiar = ttk.Button(
            frame_botones, text="Limpiar ventana", command=self.limpiar_logs)
        btn_limpiar.pack(side="left", padx=5)

        self.texto_logs = scrolledtext.ScrolledText(
            pestana, wrap=tk.WORD, width=90, height=20)
        self.texto_logs.pack(fill="both", expand=True, padx=5, pady=5)

        # Mostrar contenido inicial del archivo, si existe
        self.actualizar_logs()

    def actualizar_logs(self):
        """Lee el archivo de logs y muestra su contenido (útil para ver lo anterior)."""
        self.texto_logs.delete("1.0", tk.END)
        ruta_logs = os.path.join(os.path.dirname(
            __file__), "..", "logs", "sistema.log")
        try:
            if os.path.exists(ruta_logs):
                with open(ruta_logs, "r", encoding="utf-8") as f:
                    contenido = f.read()
                self.texto_logs.insert(tk.END, contenido)
            else:
                self.texto_logs.insert(
                    tk.END, "No se ha generado ningún log todavía.")
        except Exception as e:
            self.texto_logs.insert(
                tk.END, f"Error al leer el archivo de logs: {e}")
        self.texto_logs.see(tk.END)

    def limpiar_logs(self):
        """Limpia el widget de logs (no borra el archivo)."""
        self.texto_logs.delete("1.0", tk.END)
        # también se registra en el archivo
        logging.info("Ventana de logs limpiada por el usuario.")
