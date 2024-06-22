import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

import calibrar_emisor as ce
import calibrar_receptor as cr
import emisor
import receptor
import test_velocidad_emisor
import test_velocidad_receptor

# ----------------------Variables globales---------------

version = None

# ----------------------Funciones------------------------

def seleccionarCombobox(event):
    tipo = combobox.get()

    if tipo == "Emisor":
        mostrarEmisor()

    elif tipo == "Receptor":
        mostrarReceptor()

def mostrarEmisor():
    ocultarReceptor()
    botonCalibrarEmisor.pack(pady=5)
    botonCalibrarEmisor.config(state=tk.NORMAL)
    botonTransmitirEmisor.pack(pady=5)
    botonTransmitirEmisor.config(state=tk.DISABLED)
    botonTestEmisor.pack(pady=5)
    botonTestEmisor.config(state=tk.DISABLED)

def mostrarReceptor():
    ocultarEmisor()
    botonCalibrarReceptor.pack(pady=5)
    botonCalibrarReceptor.config(state=tk.NORMAL)
    botonTransmitirReceptor.pack(pady=5)
    botonTransmitirReceptor.config(state=tk.DISABLED)
    botonTestReceptor.pack(pady=5)
    botonTestReceptor.config(state=tk.DISABLED)

def ocultarEmisor():
    botonCalibrarEmisor.pack_forget()
    botonTransmitirEmisor.pack_forget()
    botonTestEmisor.pack_forget()

def ocultarReceptor():
    botonCalibrarReceptor.pack_forget()
    botonTransmitirReceptor.pack_forget()
    botonTestReceptor.pack_forget()

def calibrar():
    global version

    if combobox.get() == "Emisor":

        version, error = ce.calibrar_emisor()

        if error == "camera":
            messagebox.showerror("ERROR: Cámara","No se puede abrir la cámara.")
            version = None
        elif error == "frame":
            messagebox.showerror("ERROR: Fotograma","Error al capturar el fotograma de la cámara.")
            version = None
        else:
            messagebox.showinfo("Versión","Calibración completada, versión óptima: {}".format(version))
            botonTransmitirEmisor.config(state=tk.NORMAL)
            botonTestEmisor.config(state=tk.NORMAL)

        if version == None:
            botonTransmitirEmisor.config(state=tk.DISABLED)
            botonTestEmisor.config(state=tk.DISABLED)



    elif combobox.get() == "Receptor":
        error = cr.calibrar_receptor()

        if error == "camera":
            messagebox.showerror("ERROR: Cámara","No se puede abrir la cámara.")
        elif error == "frame":
            messagebox.showerror("ERROR: Fotograma","Error al capturar el fotograma de la cámara.")
        else:
            messagebox.showinfo("Calibración", "Calibración completada.")
            botonTransmitirReceptor.config(state=tk.NORMAL)
            botonTestReceptor.config(state=tk.NORMAL)

def transmision():
    global version

    if combobox.get() == "Emisor":
        fichero = filedialog.askopenfilename(title="Abrir archivo", initialdir="C:/Users/Manolo/Desktop/Archivos_originales")

        error = emisor.emisor(version,fichero)

        if error == "camera":
            messagebox.showerror("ERROR: Cámara", "No se puede abrir la cámara.")
        elif error == "fileNotFound":
            messagebox.showerror("ERROR: Fichero", "El archivo '{}' no fue encontrado.".format(fichero))
        elif error == "cannotReadFile":
            messagebox.showerror("ERROR: Leer fichero", "Error al leer el archivo.")
        elif error == "frame":
            messagebox.showerror("ERROR: Fotograma","Error al capturar el fotograma de la cámara.")
        elif error == "timeout":
            messagebox.showerror("ERROR: Time Out","Error en la transmisión: Time Out.")
        else:
            messagebox.showinfo("Completado", "Transmisión Completada.")


    elif combobox.get() == "Receptor":
        fichero = filedialog.asksaveasfilename(initialdir="C:/Users/Manolo/Desktop/Archivos_reconstruidos",
                                          initialfile="archivo",
                                          filetypes=[("Todos los archivos","*.*"),("Archivos de texto", "*.txt")])

        error = receptor.receptor(fichero)

        if error == "camera":
            messagebox.showerror("ERROR: Cámara", "No se puede abrir la cámara.")
        elif error == "frame":
            messagebox.showerror("ERROR: Fotograma","Error al capturar el fotograma de la cámara.")
        elif error == "reconstruir":
            messagebox.showerror("ERROR: Reconstruir", "Error al reconstruir el archivo")
        elif error == "timeout":
            messagebox.showerror("ERROR: Time Out", "Error en la transmisión: Time Out.")
        else:
            messagebox.showinfo("Completado", "Archivo reconstruido y guardado en {}.".format(fichero))


def testVelocidad():
    global version

    if combobox.get() == "Emisor":

        error, mediaTiempo, mediaTiempoTrx, mediaVelocidad = test_velocidad_emisor.testVelocidadEmisor(version)

        if error == "camera":
            messagebox.showerror("ERROR: Cámara", "No se puede abrir la cámara.")
        elif error == "frame":
            messagebox.showerror("ERROR: Fotograma","Error al capturar el fotograma de la cámara.")
        else:
            messagebox.showinfo("Completado", "Velocidad media de la transmisión: {} bps.".format(mediaVelocidad))
            print(f"Media Tiempo de Propagación:",mediaTiempo)
            print(f"Media Tiempo de Transmision:", mediaTiempoTrx)

    elif combobox.get() == "Receptor":

        error, mediaTiempoTrxACK = test_velocidad_receptor.testVelocidadReceptor()

        if error == "camera":
            messagebox.showerror("ERROR: Cámara", "No se puede abrir la cámara.")
        elif error == "frame":
            messagebox.showerror("ERROR: Fotograma", "Error al capturar el fotograma de la cámara.")
        else:
            messagebox.showinfo("Completado", "Test de velocidad completado.")
            print(f"Media Tiempo de Transmisión ACK: ", mediaTiempoTrxACK)


# ----------------------Ventana--------------------------

root = tk.Tk()
root.title("Transmisor QR")
root.geometry("500x400")
root.iconbitmap("qr-code.ico")

# ----------------------Label----------------------------
label = tk.Label(root, text="Seleccionar opción:")
label.pack(pady=(10,0))

# ----------------------ComboBox-------------------------

opciones = ["Emisor", "Receptor"]

combobox = ttk.Combobox(root, values=opciones, state="readonly")
combobox.pack(pady=(10,40))
combobox.bind("<<ComboboxSelected>>", seleccionarCombobox)

# ----------------------Botones--------------------------

botonCalibrarEmisor = tk.Button(root, text="Calibrar", state=tk.DISABLED, command=calibrar)
botonTransmitirEmisor = tk.Button(root, text="Transmitir", state=tk.DISABLED, command=transmision)
botonTestEmisor = tk.Button(root, text="Test de Velocidad", state=tk.DISABLED, command=testVelocidad)

botonCalibrarReceptor = tk.Button(root, text="Calibrar", state=tk.DISABLED, command=calibrar)
botonTransmitirReceptor = tk.Button(root, text="Recibir", state=tk.DISABLED, command=transmision)
botonTestReceptor = tk.Button(root, text="Test de Velocidad", state=tk.DISABLED, command=testVelocidad)

root.mainloop()