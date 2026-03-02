from tkinter import ttk, Tk, LabelFrame, Label, Entry, E, W, CENTER, END, Toplevel, StringVar, font
from tkinter.ttk import Combobox
from db import Session
from models import Producto, CategoriaEnum
from ventana_editar import VentanaEditarProducto


class VentanaPrincipal():

    def __init__(self):
        self.session = Session()
        self.ventana =Tk()
        self.ventana.title('App Gestor de Productos')
        self.ventana.resizable(1,1)
        self.ventana.wm_iconbitmap('recursos/icon.ico')

        # Creación del contenedor principal (frame)
        frame = LabelFrame(self.ventana, text='Registrar un nuevo Producto',font=('Calibri', 15 ,'bold'))
        frame.grid(row=0, column = 0, pady=20, columnspan=3)

        # Label de Nombre
        self.etiqueta_nombre = Label(frame,text='Nombre: ',font=('Calibri', 15 ,'bold'))
        self.etiqueta_nombre.grid(row=1, column=0)
        # Entry de Nombre
        self.nombre = Entry(frame)
        self.nombre.grid(row=1, column=1)
        self.nombre.focus() # Para que al abrir la app se posicione el ratón en el entry directamente


        # Label de Precio
        self.etiqueta_precio = Label(frame, text='Precio: ',font=('Calibri', 15 ,'bold'))
        self.etiqueta_precio.grid(row=2, column=0)
        # Entry de Precio
        self.precio = Entry(frame)
        self.precio.grid(row=2, column=1)

        fuente_estilo = font.Font(family="Calibri", size=11, weight="bold")

        # Label y Combobox para Categoría
        Label(frame, text='Categoría:', font=fuente_estilo).grid(row=3, column=0, pady=5)
        self.categoria = StringVar()
        self.combo_categoria = Combobox(frame, textvariable=self.categoria, font=fuente_estilo, state='readonly')
        self.combo_categoria['values'] = ("Hogar", "Electrónica", "Alimentación", "Papelería", "Farmacia", "Droguería")
        self.combo_categoria.grid(row=3, column=1, pady=5)
        self.combo_categoria.current(0)

        # Label y Combobox para Stock
        Label(frame, text='En stock:', font=fuente_estilo).grid(row=4, column=0, pady=5)
        self.en_stock = StringVar()
        self.combo_stock = Combobox(frame, textvariable=self.en_stock, font=fuente_estilo, state='readonly')
        self.combo_stock['values'] = ("Sí", "No")
        self.combo_stock.grid(row=4, column=1, pady=5)
        self.combo_stock.current(0)  # Valor por defecto

        # Botón anyadir_producto
        style = ttk.Style()
        style.configure('BotonGuardar.TButton', font=('Calibri', 12, 'bold'))
        self.boton_anyadir = ttk.Button(frame, text='Guardar Producto',style='BotonGuardar.TButton',command=self.add_producto)
        self.boton_anyadir.grid(row=5, columnspan=2, sticky=W+E)

        #Mensaje informativo para el usuario
        self.mensaje = Label(text='', fg = 'red')
        self.mensaje.grid(row=6, column=0, columnspan=2, sticky=W+E)

        # Tabla de Productos
        # Estilo personalizado para la tabla
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13, 'bold'))
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky':'nswe'})])  # Eliminamos los bordes

        # Estructura de la tabla
        self.tabla = ttk.Treeview(height=20, columns=('precio','categoria','stock'), style="mystyle.Treeview")
        self.tabla.grid(row=7, column=0, columnspan=2)
        self.tabla.heading('#0', text='Nombre', anchor=CENTER)
        self.tabla.heading('precio', text='Precio', anchor=CENTER)
        self.tabla.heading('categoria', text='Categoría', anchor=CENTER)
        self.tabla.heading('stock', text='En Stock', anchor=CENTER)

        style.configure('my.TButton', font=('Calibri', 12, 'bold'))
        self.boton_eliminar = ttk.Button(text='ELIMINAR', command=self.del_producto, style='my.TButton')
        self.boton_eliminar.grid(row=8, column=0, sticky=W + E)
        self.boton_editar = ttk.Button(text='EDITAR', command=self.edit_producto, style='my.TButton')
        self.boton_editar.grid(row=8, column=1, sticky=W + E)


        self.get_productos()



        self.ventana.mainloop()

    def get_productos(self):
        # Limpiar tabla
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        productos = self.session.query(Producto).order_by(Producto.nombre.desc()).all()

        for producto in productos:
            stock = "Sí" if producto.en_stock else "No"
            categoria = producto.categoria.value.capitalize()
            self.tabla.insert('', 0, text=producto.nombre, values=(producto.precio, categoria, stock))

    def validacion_nombre(self):
        return self.nombre.get().strip() != ''

    def validacion_precio(self):
        try:
            precio = float(self.precio.get())
            return precio > 0
        except ValueError:
            return False

    def add_producto(self):
        if not self.validacion_nombre():
            print('El nombre es obligatorio')
            self.mensaje['text'] = 'El nombre es obligatorio y no puede estar vacio'
            return
        if not self.validacion_precio():
            print('El precio es obligatorio')
            self.mensaje['text'] = 'El precio es obligatorio y debe ser un número mayor que 0'
            return

        try:
            categoria_enum = CategoriaEnum(self.categoria.get().lower())

            en_stock_bool = True if self.en_stock.get() == 'Sí' else False

            nuevo_producto = Producto(
                nombre=self.nombre.get(),
                precio=float(self.precio.get()),
                categoria = categoria_enum,
                en_stock = en_stock_bool
            )
            self.session.add(nuevo_producto)
            self.session.commit()

            print('Datos guardados')
            self.mensaje['text'] = 'Producto añadido con éxito'
            self.nombre.delete(0, END)
            self.precio.delete(0, END)

            self.get_productos()

        except Exception as e:
            self.session.rollback()
            print(f"Error al guardar en la base de datos: {e}")
            self.mensaje['text'] = 'Error al guardar el producto'

    def del_producto(self):
        self.mensaje['text'] = ''
        seleccion = self.tabla.selection()
        if not seleccion:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
            return

        nombre = self.tabla.item(seleccion[0])['text']

        try:
            producto = self.session.query(Producto).filter(Producto.nombre == nombre).first()
            if producto:
                self.session.delete(producto)
                self.session.commit()
                self.mensaje['text'] = 'Producto eliminado con éxito'
                self.get_productos()
            else:
                self.mensaje['text'] = 'Producto no encontrado en la base de datos'
        except Exception as e:
            self.session.rollback()
            self.mensaje['text'] = f'Error al eliminar producto: {e}'

    def edit_producto(self):
        try:
            nombre = self.tabla.item(self.tabla.selection())['text']
            precio = self.tabla.item(self.tabla.selection())['values'][0]
            VentanaEditarProducto(self, nombre, precio, self.mensaje)
        except IndexError:
            self.mensaje['text'] = 'Por favor, seleccione un producto'
