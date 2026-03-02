from tkinter import ttk, Tk, LabelFrame, Label, Entry, E, W, CENTER, END, Toplevel, StringVar
import db
from ventana_bienvenida import VentanaBienvenida


def run_app():
    ventana_bienvenida=VentanaBienvenida()

if __name__ == '__main__':

    db.Base.metadata.create_all(bind=db.engine)

    run_app()


