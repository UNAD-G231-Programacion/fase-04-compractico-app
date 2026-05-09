# main.py - Punto de entrada del sistema Software FJ
import tkinter as tk
from app.interfaz import InterfazSistema

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazSistema(root)
    root.mainloop()
