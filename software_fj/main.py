###
# PUNTO DE ENTRADA DE LA APLICACION
# Este archivo main.py es el que se debe ejecutar para iniciar la app.
###

# main.py - Punto de entrada del sistema Software FJ
import tkinter as tk
from app.interfaz import InterfazSistema

if __name__ == "__main__":
    # Crea la ventana
    root = tk.Tk()
    # asigna la interfaz del programa a la ventana creada
    app = InterfazSistema(root)
    # Mantiene la ventana en ejecucion
    root.mainloop()
