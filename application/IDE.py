import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os

# Asegúrate de que el directorio raíz del proyecto esté en el PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'C:/Users/Personal/Documents/Universidad/8 Semestre/Compis2/SintaxAnalisis-Compiladores')))

from program.Driver import compilador

# Crear una instancia de Tkinter
root = tk.Tk()

# Configurar el título de la ventana
root.title("Compiscript IDE")

# Configurar el tamaño de la ventana
root.geometry("600x500")

# Crear una etiqueta
label = ttk.Label(root, text="¡Escribe tu código Compiscript!")
label.pack(pady=10)

# Crear un campo de entrada de texto
text_input = tk.Text(root, height=10, width=70)
text_input.pack(pady=10)

# Crear un área de texto para mostrar errores
error_output = tk.Text(root, height=10, width=70, bg='light gray')
error_output.pack(pady=10)

# Crear una función para el botón
def boton_click():
    codigo = text_input.get("1.0", tk.END)  # Obtener el texto del campo de entrada
    error_output.delete("1.0", tk.END)  # Limpiar el área de texto de errores
    try:
        resultado = compilador(codigo)
        label.config(text="Compilación exitosa")
        error_output.insert(tk.END, f"Resultado: {resultado}")
    except Exception as e:
        label.config(text="Error de compilación")
        error_output.insert(tk.END, str(e))

# Crear un botón
boton = ttk.Button(root, text="Compilar", command=boton_click)
boton.pack(pady=10)

# Iniciar el bucle de eventos
root.mainloop()
