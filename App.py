from ftplib import FTP # Libreria para hacer uso de FTP
import os
from tkinter import Tk, Button, Label, filedialog, messagebox, Frame, Listbox, Scrollbar

# Abrir archivo 
def abrir_archivo(ruta_archivo):
    try:
        import subprocess
        subprocess.Popen(['start', '', ruta_archivo], shell=True)
    except Exception as e:
        print("Error al abrir el archivo:", str(e))

# Funcion para seleccionar el archivo del explorador de archivos 
def seleccionar_archivo():
    ruta_archivo = filedialog.askopenfilename()
    etiqueta_ruta.config(text="Ruta del archivo: " + ruta_archivo)

    boton_abrir = Button(ventana, text="Abrir Archivo", command=lambda: abrir_archivo(ruta_archivo), relief="raised", borderwidth=2)
    boton_abrir.pack(pady=10)

    boton_enviar.config(state="normal", command=lambda: enviar_archivo(ruta_archivo), relief="raised", borderwidth=2)

#Funcion para enviar el archivo
def enviar_archivo(ruta_archivo):
    try:
        # Configuracion de FTP
        ftp = FTP() # Creamos un objeto de tipo FTP
        ftp.connect('server_url') # Nos conectamos a la direccion de nuestro servidor
        ftp.login('user', 'password') # Accedemos con nuestras credenciales
        ftp.set_pasv(True) # Activar el modo pasivo

        # Cambiar al directorio correcto en el servidor con cwd
        directorio_servidor = '/directorio'
        ftp.cwd(directorio_servidor)

        # Obtener el nombre del archivo
        nombre_archivo = os.path.basename(ruta_archivo)

        print("Enviando archivo:", nombre_archivo)

        with open(ruta_archivo, 'rb') as file:
            ftp.storbinary('STOR ' + nombre_archivo, file)

        print("Archivo enviado con éxito.")
        etiqueta_estado.config(text="Archivo enviado con éxito.", fg="green")
        boton_enviar.config(state="disabled", relief="sunken", borderwidth=2) 
        actualizar_lista_archivos()  
    except Exception as e:
        print("Error al enviar el archivo:", str(e))
        etiqueta_estado.config(text="Error al enviar el archivo: " + str(e), fg="red")
        messagebox.showerror("Error", "Error al enviar el archivo: " + str(e))
    finally:
        ftp.quit() # Terminamos la conexion

#Funcion para actualizar la lista
def actualizar_lista_archivos():
    try:
        archivos_en_servidor = ftp.nlst()
        lista_archivos.delete(0, 'end')  
        for archivo in archivos_en_servidor:
            lista_archivos.insert('end', archivo)
    except Exception as e:
        print("Error al actualizar la lista de archivos:", str(e))

# Logica para descargar archivos del servidor
def descargar_archivo():
    try:
        seleccion = lista_archivos.curselection()
        if seleccion:
            archivo_seleccionado = lista_archivos.get(seleccion)
            ruta_guardado = filedialog.asksaveasfilename(defaultextension=".*", initialfile=archivo_seleccionado)
            with open(ruta_guardado, 'wb') as archivo_local:
                ftp.retrbinary('RETR ' + archivo_seleccionado, archivo_local.write)
            messagebox.showinfo("Éxito", "Archivo descargado con éxito.")
        else:
            messagebox.showwarning("Advertencia", "Selecciona un archivo para descargar.")
    except Exception as e:
        print("Error al descargar el archivo:", str(e))
        messagebox.showerror("Error", "Error al descargar el archivo: " + str(e))

# Cracion de la parte visual del programa con TK
ventana = Tk()
ventana.title("Transferencia de archivos via FTP")
ventana.geometry("500x700")
ventana.resizable(False, False)
title = Label(ventana, text="TRANSFERENCIA DE ARCHIVOS VIA FTP")
title.pack()
contenedor_input = Frame(ventana)
contenedor_input.pack(padx=20, pady=20)
label_seleccionar = Label(contenedor_input, text="Selecciona un archivo: ")
label_seleccionar.pack(side="left", padx=10)
boton_seleccionar = Button(contenedor_input, text="Seleccionar Archivo", command=seleccionar_archivo, relief="raised", borderwidth=2)
boton_seleccionar.pack(side="left", padx=10)
etiqueta_ruta = Label(ventana, text="Ruta del archivo:")
etiqueta_ruta.pack()
boton_enviar = Button(ventana, text="Enviar", state="disabled", relief="sunken", borderwidth=2)
boton_enviar.pack(pady=20)
etiqueta_estado = Label(ventana, text="", fg="black")
etiqueta_estado.pack()
lista_archivos = Listbox(ventana, selectmode='single', width=50, height=10)
lista_archivos.pack(pady=10)
boton_descargar = Button(ventana, text="Descargar Archivo", command=descargar_archivo, relief="raised", borderwidth=2)
boton_descargar.pack(pady=10)
ventana.update_idletasks()
width = ventana.winfo_width()
height = ventana.winfo_height()
x_coordinate = (ventana.winfo_screenwidth() // 2) - (width // 2)
y_coordinate = (ventana.winfo_screenheight() // 2) - (height // 2)
ventana.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")

# Iniciar la conexión FTP y actualizar la lista de archivos
ftp = FTP()
ftp.connect('server_url')
ftp.login('user', 'password') 
ftp.set_pasv(True) 
ftp.cwd('/directorio')  
actualizar_lista_archivos()

ventana.mainloop()
