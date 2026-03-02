import tkinter as tk
from tkinter import PhotoImage
from ventana_principal import VentanaPrincipal

class VentanaBienvenida:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("GestProd")
        self.ventana.geometry("500x500")
        self.ventana.iconbitmap("recursos/icon.ico")

        # Etiqueta de bienvenida
        etiqueta = tk.Label(self.ventana, text="Bienvenido a GestProd", font=("Helvetica", 18, "bold"))
        etiqueta.pack(pady=20)

        # Imagen
        self.imagen = PhotoImage(file="recursos/logotipo.png")
        imagen_label = tk.Label(self.ventana, image=self.imagen)
        imagen_label.pack(pady=20)


        boton_entrar = tk.Button(self.ventana, text="Entrar", font=("Helvetica", 14), command=self.abrir_principal)
        boton_entrar.pack(pady=30)

        self.ventana.mainloop()

    def abrir_principal(self):
        self.ventana.destroy()
        VentanaPrincipal()


