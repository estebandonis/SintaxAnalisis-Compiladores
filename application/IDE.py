import tkinter as tk
from tkinter import ttk

# Crear una instancia de Tkinter
root = tk.Tk()

# Configurar el título de la ventana
root.title("Mi Primera Ventana de Tkinter")

# Configurar el tamaño de la ventana
root.geometry("300x200")

# Crear una etiqueta
label = ttk.Label(root, text="¡Hola, Tkinter!")
label.pack(pady=20)

# Crear una función para el botón
def boton_click():
    label.config(text="¡Botón presionado!")

# Crear un botón
boton = ttk.Button(root, text="Haz clic aquí", command=boton_click)
boton.pack(pady=10)

# Iniciar el bucle de eventos
root.mainloop()
