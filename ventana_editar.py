from tkinter import Toplevel, LabelFrame, Label, Entry, StringVar, W, E
from tkinter import ttk
from models import Producto, CategoriaEnum


class VentanaEditarProducto:

    def __init__(self, ventana_principal, nombre, precio, mensaje_label):
        self.ventana_principal = ventana_principal
        self.session = ventana_principal.session
        self.nombre_original = nombre
        self.precio_original = precio
        self.mensaje = mensaje_label

        # Obtener producto actual desde la base de datos
        self.producto = self.session.query(Producto).filter_by(nombre=self.nombre_original).first()
        if not self.producto:
            self.mensaje['text'] = 'Producto no encontrado'
            return

        self.ventana_editar = Toplevel()
        self.ventana_editar.title('Editar Producto')

        frame = LabelFrame(self.ventana_editar, text='Editar el Producto', font=('Calibri', 16, 'bold'))
        frame.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

        Label(frame, text='Nombre antiguo:', font=('Calibri', 13)).grid(row=0, column=0)
        Entry(frame, textvariable=StringVar(value=nombre), state='readonly', font=('Calibri', 13)).grid(row=0, column=1)

        Label(frame, text='Nombre nuevo:', font=('Calibri', 13)).grid(row=1, column=0)
        self.input_nombre_nuevo = Entry(frame, font=('Calibri', 13))
        self.input_nombre_nuevo.grid(row=1, column=1)
        self.input_nombre_nuevo.focus()

        Label(frame, text='Precio antiguo:', font=('Calibri', 13)).grid(row=2, column=0)
        Entry(frame, textvariable=StringVar(value=precio), state='readonly', font=('Calibri', 13)).grid(row=2, column=1)

        Label(frame, text='Precio nuevo:', font=('Calibri', 13)).grid(row=3, column=0)
        self.input_precio_nuevo = Entry(frame, font=('Calibri', 13))
        self.input_precio_nuevo.grid(row=3, column=1)

        # Categoría
        Label(frame, text='Categoría:', font=('Calibri', 13)).grid(row=4, column=0)
        self.categoria_var = StringVar()
        self.combo_categoria = ttk.Combobox(frame, textvariable=self.categoria_var, font=('Calibri', 13), state='readonly')
        self.combo_categoria['values'] = [c.value.capitalize() for c in CategoriaEnum]
        self.combo_categoria.grid(row=4, column=1)
        categoria_index = list(CategoriaEnum).index(self.producto.categoria)
        self.combo_categoria.current(categoria_index)

        # Stock
        Label(frame, text='En Stock:', font=('Calibri', 13)).grid(row=5, column=0)
        self.stock_var = StringVar()
        self.combo_stock = ttk.Combobox(frame, textvariable=self.stock_var, font=('Calibri', 13), state='readonly')
        self.combo_stock['values'] = ['Sí', 'No']
        self.combo_stock.grid(row=5, column=1)
        self.combo_stock.current(0 if self.producto.en_stock else 1)

        # Botón actualizar
        style = ttk.Style()
        style.configure('BotonActualizar.TButton', font=('Calibri', 12, 'bold'))
        boton_actualizar = ttk.Button(frame, text='Actualizar Producto', command=self.actualizar_producto,style='BotonActualizar.TButton')
        boton_actualizar.grid(row=6, columnspan=2, sticky=W + E, pady=10)

    def actualizar_producto(self):
        nuevo_nombre = self.input_nombre_nuevo.get().strip() or self.nombre_original
        nuevo_precio_str = self.input_precio_nuevo.get().strip()
        try:
            nuevo_precio = float(nuevo_precio_str) if nuevo_precio_str else float(self.precio_original)
        except ValueError:
            self.mensaje['text'] = 'Precio no válido'
            return

        nueva_categoria = self.categoria_var.get().lower()
        nuevo_en_stock = self.stock_var.get() == 'Sí'

        try:
            self.producto.nombre = nuevo_nombre
            self.producto.precio = nuevo_precio
            self.producto.categoria = CategoriaEnum(nueva_categoria)
            self.producto.en_stock = nuevo_en_stock

            self.session.commit()
            self.mensaje['text'] = 'Producto actualizado con éxito'
        except Exception as e:
            self.session.rollback()
            self.mensaje['text'] = f'Error al actualizar: {e}'

        self.ventana_editar.destroy()
        self.ventana_principal.get_productos()
