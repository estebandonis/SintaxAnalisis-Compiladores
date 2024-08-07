import tkinter as tk
from tkinter import ttk
import subprocess
from program.Driver import compilador
import sys

# Crear una instancia de Tkinter
root = tk.Tk()

# Configurar el título de la ventana
root.title("Compiscript IDE")

# Configurar el tamaño de la ventana
root.geometry("600x400")

# Crear una etiqueta
label = ttk.Label(root, text="¡Escribe tu código Compiscript!")
label.pack(pady=20)

# Crear un campo de entrada de texto
text_input = tk.Text(root, height=15, width=70)
text_input.pack(pady=20)

# Crear una función para el botón
def boton_click():
    codigo = text_input.get("1.0", tk.END)  # Obtener el texto del campo de entrada
    try:
        # resultado = subprocess.check_output([sys.executable, "Driver.py", codigo], stderr=subprocess.STDOUT, text=True)
        resultado = compilador(codigo)
        label.config(text=f"Compilación exitosa: {resultado}")
    except subprocess.CalledProcessError as e:
        label.config(text=f"Error de compilación: {e.output}")

# Crear un botón
boton = ttk.Button(root, text="Compilar", command=boton_click)
boton.pack(pady=10)

# Iniciar el bucle de eventos
root.mainloop()