# main.py - Punto de entrada del sistema Software FJ
import tkinter as tk
from app.interfaz import InterfazSistema

if __name__ == "__main__":
    # Crea la ventana
    root = tk.Tk()
    app = InterfazSistema(root)
    # Mantiene la ventana en ejecucion
    root.mainloop()
