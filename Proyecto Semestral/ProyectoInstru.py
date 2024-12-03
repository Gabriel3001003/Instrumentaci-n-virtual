import paho.mqtt.client as mqtt 
import random
import time
import json 
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import qrcode
import os
from datetime import datetime
import serial
import cv2
from pyzbar import pyzbar
from PIL import Image, ImageTk
import pymysql
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QSlider, QVBoxLayout, QWidget, QLCDNumber
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QMessageBox, QLabel, QTableWidgetItem
from PyQt5.QtGui import QPixmap
import threading
import streamlit as st
import pandas as pd
from tkinter import messagebox
import matplotlib.pyplot as plt

# Función de callback en caso de conexión exitosa
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conexión exitosa")
    else:
        print(f"Error de conexión, código: {rc}")


# Función para Qt designer (Interfáz)
app = QtWidgets.QApplication([])
gui1 = uic.loadUi('Interfaz.ui')
gui2 = uic.loadUi('RegistrarUsuario.ui')
gui3 = uic.loadUi('Menu.ui')
gui4 = uic.loadUi('inventario.ui')
gui5 = uic.loadUi('Qr.ui')
gui6 = uic.loadUi('retirar.ui')
gui7 = uic.loadUi('Qropciones.ui')
gui8 = uic.loadUi('Sensores.ui')
gui9 = uic.loadUi('Alterar.ui')


def node_red():
    broker = "9677ffc66171483a83133c060ddfbecc.s1.eu.hivemq.cloud"
    port = 8883  # Usar puerto seguro
    topic = "sensor/data"


    # Configuración del cliente MQTT
    cliente = mqtt.Client()
   
    # Configurar credenciales
    usuario = "Reyes8"  # Sustituye con tu nombre de usuario de HiveMQ Cloud
    contraseña = "Reyes1201"  # Sustituye con tu contraseña de HiveMQ Cloud
    cliente.username_pw_set(usuario, contraseña)
   
    # Habilitar TLS/SSL para HiveMQ
    cliente.tls_set()  # Configura automáticamente los certificados TLS predeterminados
   
    # Definir la función de callback cuando se conecta
    cliente.on_connect = on_connect
   
    # Conectar al broker con TLS/SSL
    print("Conectando al broker...")
    cliente.connect(broker, port, keepalive=60)
   
    # Iniciar el bucle de la red para gestionar la conexión y callbacks
    cliente.loop_start()


# Configuración de la conexión a MySQL
def conectar_base_datos():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",  # Ajusta estos valores según tu configuración de MySQL
            password="Reyes1201",
            database="Inventario"
        )
        return conn
    except pymysql.MySQLError as err:
        print(f"Error: {err}")
        return None


def fetch_data():
    connection = conectar_base_datos()
    query = "SELECT Temperatura, Humedad, Amperaje FROM Datosalmacen01"
    df = pd.read_sql(query, connection)
    connection.close()
    return df

st.title("Datos sensores Almacen")

if st.button("Cargar datos"):
    try:
        data = fetch_data()
        st.success("Datos cargados exitosamente.")
        
        # Mostrar la tabla
        st.write("### Tabla de Datos")
        st.dataframe(data)
        
        # Gráficas
        st.write("### Gráficas")
        fig, ax = plt.subplots(1, 2, figsize=(12, 5))

        # Gráfica de Temperatura y Humedad
        ax[0].plot(data.index, data['Temperatura'], label="Temperatura (°C)", color='red')
        ax[0].plot(data.index, data['Humedad'], label="Humedad (%)", color='blue')
        ax[0].set_title("Temperatura y Humedad")
        ax[0].set_xlabel("Registro")
        ax[0].set_ylabel("Valores")
        ax[0].legend()

        # Gráfica de Amperaje
        ax[1].bar(data.index, data['Amperaje'], color='green', alpha=0.7)
        ax[1].set_title("Amperaje")
        ax[1].set_xlabel("Registro")
        ax[1].set_ylabel("Amperaje (A)")

        st.pyplot(fig)
    except Exception as e:
        st.error(f"Ocurrió un error: {e}")

# Función para entrar al modo registrar usuario
def registrar_principal():
    gui1.hide()  # Ocultamos la GUI 1 en lugar de destruirla
    gui2.show()

# Función para salir del registro y volver a la GUI 1
def SalirRegistro():
    gui2.hide()
    gui1.show()

# Función para capturar el UID del RFID
def leer_uid():
    try:
        ser = serial.Serial('COM4', 9600, timeout=1)
        time.sleep(2)  # Esperar para asegurar la conexión
        ser.write(b'L')  # Suponiendo que el Arduino espera este comando
        uid = ser.readline().decode('utf-8').strip()  # Leemos el UID
        ser.close()
        return uid
    except serial.SerialException as e:
        print(f"Error de conexión serial: {e}")
        return None

# Función que se activa cuando se presiona el botón btnRFID para capturar el UID
def capturar_uid():
    uid = leer_uid()
    if uid:
        gui2.labelUID.setText(uid)
    else:
        messagebox.showwarning("Error", "No se pudo leer el UID. Intenta nuevamente.")

# Función para registrar el usuario en la base de datos
def registrar_usuario():
    nombre = gui2.Nombre.text()  # LineEdit para nombre
    apellido = gui2.Apellido.text()  # LineEdit para apellido
    uid = gui2.labelUID.text()  # UID capturado y mostrado en el Label
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    if not nombre or not apellido or not uid:
        messagebox.showwarning("Error", "Completa todos los campos antes de registrar.")
        return

    # Conexión a la base de datos
    conn = conectar_base_datos()
    if conn:
        cursor = conn.cursor()
        try:
            query = "INSERT INTO Usuarios (Nombre, Apellido, UID, timestamp) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (nombre, apellido, uid, timestamp))
            conn.commit()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
        except pymysql.MySQLError as err:
            messagebox.showerror("Error", f"No se pudo registrar al usuario: {err}")
        finally:
            cursor.close()
            conn.close()
    else:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")

# Función para verificar el UID y abrir GUI 3
def ingresar_usuario():
    uid = leer_uid()  # Leer el UID del RFID
    if uid:
        conn = conectar_base_datos()
        if conn:
            cursor = conn.cursor()
            query = "SELECT Nombre, Apellido FROM Usuarios WHERE UID = %s"
            cursor.execute(query, (uid,))
            result = cursor.fetchone()
            if result:
                nombre, apellido = result
                # Mostrar un mensaje de bienvenida con el nombre del usuario
                messagebox.showinfo("Ingreso", f"Bienvenido {nombre} {apellido}")
                
                # Actualizar el label en gui3 con el nombre del usuario
                gui3.Usuario.setText(f"Usuario: {nombre} {apellido}")
                
                # Ocultamos gui1 y mostramos gui3
                gui1.hide()
                gui3.show()
                
                
            else:
                messagebox.showwarning("Error", "UID no registrado.")
            cursor.close()
            conn.close()
        else:
            messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
    else:
        messagebox.showwarning("Error", "No se pudo leer el UID. Intenta nuevamente.")
    

# Función para cerrar sesión y regresar a gui1
def cerrar_sesion():
    gui3.hide()  # Oculta la GUI 3
    gui1.show()  # Muestra la GUI 1

# Abrimos la interfaz del inventario
def abrir_inventario():
    gui3.hide()
    gui4.show()

def agregar_producto():
    # Obtener valores de los widgets
    nombre_articulo = gui5.NombreArticulo.text()
    cantidad = gui5.Cantidad.value()
    
    # Determinar el tipo de producto
    if gui5.radioButton.isChecked():
        tipo = "Herramienta"
    elif gui5.radioButton_2.isChecked():
        tipo = "Componente"
    elif gui5.radioButton_3.isChecked():
        tipo = "Material"
    else:
        messagebox.showwarning("Error", "Selecciona un tipo de artículo.")
        return
    
    # Conectar a la base de datos
    conn = conectar_base_datos()
    if conn:
        cursor = conn.cursor()
        try:
            # Insertar en la tabla Productos01
            query = "INSERT INTO Productos01 (Nombre, Tipo, Cantidad) VALUES (%s, %s, %s)"
            cursor.execute(query, (nombre_articulo, tipo, cantidad))
            conn.commit()
            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
            
            # Generar código QR
            generar_codigo_qr(nombre_articulo)

            # Abrir la cámara para tomar foto
            tomar_foto(nombre_articulo)

            # Actualizar la TableView en gui4
            actualizar_tableview()

            # Actualizar la progressBar
            actualizar_progressbar()
            
            # Limpiar el LineEdit y reiniciar el Slider
            gui5.NombreArticulo.clear()
            gui5.Cantidad.setValue(0)

        except pymysql.MySQLError as err:
            messagebox.showerror("Error", f"No se pudo agregar el producto: {err}")
        finally:
            cursor.close()
            conn.close()


def generar_codigo_qr(nombre_articulo):
    # Generar código QR
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(nombre_articulo)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')

    # Guardar el QR
    qr_path = f"C:\\Users\\rreye\\OneDrive\\Documentos\\IET LA SALLE BAJIO\\IET 7mo Semestre\\Proyecto Semestral\\QR base datos\\{nombre_articulo}.png"
    img.save(qr_path)
    messagebox.showinfo("Éxito", f"Código QR generado y guardado en: {qr_path}")

def tomar_foto(nombre_articulo):
    # Captura de imagen usando OpenCV
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        messagebox.showerror("Error", "No se pudo acceder a la cámara.")
        return

    # Esperar a que la cámara esté lista
    messagebox.showinfo("Tomar Foto", "Presiona 'c' para tomar la foto.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        cv2.imshow('Captura de Imagen', frame)
        
        # Esperar a que el usuario presione 'c'
        if cv2.waitKey(1) & 0xFF == ord('c'):
            # Guardar la imagen
            photo_path = f"C:\\Users\\rreye\\OneDrive\\Documentos\\IET LA SALLE BAJIO\\IET 7mo Semestre\\Proyecto Semestral\\QR base datos\\{nombre_articulo}.jpg"
            cv2.imwrite(photo_path, frame)
            messagebox.showinfo("Éxito", f"Foto guardada en: {photo_path}")
            break

    cap.release()
    cv2.destroyAllWindows()

def actualizar_tableview():
    """Actualiza la tabla en la GUI 4 con los productos en la base de datos y muestra la cantidad total."""
    conn = conectar_base_datos()
    if conn:
        cursor = conn.cursor()
        query = "SELECT Nombre, Tipo, Cantidad FROM Productos01"
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        # Limpiar la tabla antes de actualizar
        gui4.tableWidget.clearContents()  
        gui4.tableWidget.setRowCount(0)  

        # Configurar el número de columnas y las etiquetas de cabecera
        gui4.tableWidget.setColumnCount(3)  # Asegúrate de que tienes el número correcto de columnas
        gui4.tableWidget.setHorizontalHeaderLabels(["Nombre", "Tipo", "Cantidad"])  # Etiquetas de cabecera
        
        total_cantidad = 0  

        for nombre, tipo, cantidad in resultados:
            row_position = gui4.tableWidget.rowCount()
            gui4.tableWidget.insertRow(row_position)  
            gui4.tableWidget.setItem(row_position, 0, QTableWidgetItem(nombre))  
            gui4.tableWidget.setItem(row_position, 1, QTableWidgetItem(tipo))  

            # Asegúrate de que cantidad sea un número válido
            cantidad_int = int(cantidad) if isinstance(cantidad, (int, str)) and cantidad.isdigit() else 0
            gui4.tableWidget.setItem(row_position, 2, QTableWidgetItem(str(cantidad_int)))  
            total_cantidad += cantidad_int  

        cursor.close()
        conn.close()
        
        # Actualizar el label_4 y progressBar
        gui4.label_4.setText(f"Cantidad Total: {total_cantidad}")
        gui4.progressBar.setValue(total_cantidad)










# Función para actualizar el QLCDNumber cuando se mueve el QSlider
def actualizar_lcd(value):
    gui5.lcdNumber.display(value)  # Asumiendo que tu QLCDNumber se llama lcdNumber

# Asegúrate de conectar la señal del QSlider al método que actualiza el QLCDNumber
gui5.Cantidad.valueChanged.connect(actualizar_lcd)

def actualizar_progressbar():
    """Actualiza la barra de progreso en la GUI 4 con el número total de productos."""
    conn = conectar_base_datos()
    if conn:
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM Productos01"
        cursor.execute(query)
        total_productos = cursor.fetchone()[0]
        
        # Actualiza la barra de progreso
        gui4.progressBar.setMaximum(5000)
        gui4.progressBar.setValue(total_productos)

        cursor.close()
        conn.close()


def agregar():
    gui4.hide()
    gui5.show()

def Salir():
    gui5.hide()
    gui4.show()

def Tabla():
    actualizar_progressbar()
    actualizar_tableview()

def btnRetirar_clicked():
    """Función para retirar productos de la base de datos."""
    nombre_producto = gui6.lineEdit.text().strip()  # Leer el nombre del producto
    cantidad_a_retirar = gui6.SliderRetirar.value()  # Obtener valor del slider

    # Mostrar la cantidad en el LCD Number
    gui6.lcdNumber.display(cantidad_a_retirar)

    # Verificar la UID del usuario
    uid_actual = leer_uid()  # Asegúrate de tener esta función
    if uid_actual is None:
        gui6.mensaje_error.setText("Error: No hay usuario en sesión.")
        return

    # Consultar la cantidad actual del producto en la base de datos
    conn = conectar_base_datos()
    if conn:
        cursor = conn.cursor()
        # Usa %s en lugar de ? para pymysql
        cursor.execute("SELECT Cantidad FROM Productos01 WHERE Nombre = %s", (nombre_producto,))
        resultado = cursor.fetchone()

        if resultado:  # Si se encuentra el producto
            cantidad_actual = int(resultado[0])

            # Verificar si la cantidad a retirar es menor o igual a la cantidad actual
            if cantidad_a_retirar <= cantidad_actual:
                nueva_cantidad = cantidad_actual - cantidad_a_retirar
                # Actualiza la cantidad en la base de datos
                cursor.execute("UPDATE Productos01 SET Cantidad = %s WHERE Nombre = %s", (nueva_cantidad, nombre_producto))
                conn.commit()
                messagebox.showinfo("Éxito", "Cantidad retirada correctamente.")
            else:
                gui6.mensaje_error.setText("Error: No hay suficiente cantidad para retirar.")
        else:
            gui6.mensaje_error.setText("Error: Producto no encontrado.")

        cursor.close()
        conn.close()
    else:
        gui6.mensaje_error.setText("Error: No se pudo conectar a la base de datos.")



# Conectar el botón al evento
gui6.btnRetirar.clicked.connect(btnRetirar_clicked)


def slider_value_changed(value):
    """Actualizar el lcdNumber cuando se mueve el slider."""
    gui6.lcdNumber.display(value)  # Muestra el valor del slider en el lcdNumber

# Conectar el slider al evento
gui6.SliderRetirar.valueChanged.connect(slider_value_changed)



def retirar():
    gui4.hide()
    gui6.show()

def Salir2():
    gui6.hide()
    gui4.show()


# Función para detectar el QR usando la cámara
# Función para detectar el QR usando la cámara
def detectar_qr():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        QMessageBox.critical(None, "Error", "No se pudo acceder a la cámara.")
        return

    QMessageBox.information(None, "Detección de QR", "Enfoca un código QR para escanearlo.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Decodificar los códigos QR en la imagen
        decoded_objects = pyzbar.decode(frame)
        for obj in decoded_objects:
            qr_data = obj.data.decode('utf-8')
            # Cerramos la cámara
            cap.release()
            cv2.destroyAllWindows()
            mostrar_datos_producto(qr_data)  # Mostrar datos del producto en gui7
            return
        
        cv2.imshow('Detección de QR', frame)
        
        # Salir del bucle si se presiona 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Función para mostrar datos del producto en gui7
# Modificar la función para mostrar datos del producto en gui7
def mostrar_datos_producto(qr_data):
    conn = conectar_base_datos()
    if conn:
        cursor = conn.cursor()
        # Asegúrate de que la consulta SQL se ajusta a tu estructura de base de datos
        query = "SELECT Nombre, Tipo, Cantidad FROM Productos01 WHERE Nombre = %s"
        cursor.execute(query, (qr_data,))
        result = cursor.fetchone()

        if result:
            nombre, tipo, cantidad = result
            gui7.label_2.setText(f"QR: {qr_data}")  # Mostrar QR en label_2
            gui7.label_3.setText(f"Foto: {nombre}.jpg")  # Mostrar la ruta de la foto en label_3
            
            # Cargar la imagen del QR
            qr_image_path = f"C:\\Users\\rreye\\OneDrive\\Documentos\\IET LA SALLE BAJIO\\IET 7mo Semestre\\Proyecto Semestral\\QR base datos\\{nombre}.png"
            if os.path.exists(qr_image_path):
                pixmap_qr = QPixmap(qr_image_path)
                gui7.label_2.setPixmap(pixmap_qr.scaled(150, 150, aspectRatioMode=True))  # Ajusta el tamaño como desees
            else:
                gui7.label_2.setText("QR no encontrado.")
            
            # Cargar la foto del producto
            foto_image_path = f"C:\\Users\\rreye\\OneDrive\\Documentos\\IET LA SALLE BAJIO\\IET 7mo Semestre\\Proyecto Semestral\\QR base datos\\{nombre}.jpg"
            if os.path.exists(foto_image_path):
                pixmap_foto = QPixmap(foto_image_path)
                gui7.label_3.setPixmap(pixmap_foto.scaled(150, 150, aspectRatioMode=True))  # Ajusta el tamaño como desees
            else:
                gui7.label_3.setText("Foto no encontrada.")
            
            # Actualizar la tabla con los datos del producto
            gui7.tableWidget.setRowCount(0)  # Limpiar la tabla
            gui7.tableWidget.setColumnCount(3)  # Asegúrate de que la tabla tiene 3 columnas
            gui7.tableWidget.setHorizontalHeaderLabels(["Nombre", "Tipo", "Cantidad"])  # Etiquetas de encabezado
            
            # Insertar datos en la tabla
            gui7.tableWidget.insertRow(0)
            gui7.tableWidget.setItem(0, 0, QTableWidgetItem(nombre))
            gui7.tableWidget.setItem(0, 1, QTableWidgetItem(tipo))
            gui7.tableWidget.setItem(0, 2, QTableWidgetItem(str(cantidad)))

            gui7.show()  # Mostrar gui7
        else:
            QMessageBox.warning(None, "Error", "Producto no encontrado.")
        
        cursor.close()
        conn.close()


# Función para eliminar el producto de la base de datos y del sistema de archivos
def eliminar_producto():
    nombre = gui7.tableWidget.item(0, 0).text()  # Obtener el nombre del producto de la tabla

    # Confirmar eliminación
    if QMessageBox.question(None, "Confirmación", f"¿Estás seguro de que deseas eliminar {nombre}?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
        conn = conectar_base_datos()
        if conn:
            cursor = conn.cursor()
            try:
                # Eliminar producto de la base de datos
                query = "DELETE FROM Productos01 WHERE Nombre = %s"
                cursor.execute(query, (nombre,))
                conn.commit()

                # Eliminar la imagen y el QR
                ruta_foto = f"C:\\Users\\rreye\\OneDrive\\Documentos\\IET LA SALLE BAJIO\\IET 7mo Semestre\\Proyecto Semestral\\QR base datos\\{nombre}.jpg"
                ruta_qr = f"C:\\Users\\rreye\\OneDrive\\Documentos\\IET LA SALLE BAJIO\\IET 7mo Semestre\\Proyecto Semestral\\QR base datos\\{nombre}.png"
                
                if os.path.exists(ruta_foto):
                    os.remove(ruta_foto)
                if os.path.exists(ruta_qr):
                    os.remove(ruta_qr)

                QMessageBox.information(None, "Éxito", f"{nombre} ha sido eliminado correctamente.")
                actualizar_progressbar()  # Actualizar la barra de progreso
                gui7.hide()  # Cerrar gui7
            except pymysql.MySQLError as err:
                QMessageBox.critical(None, "Error", f"No se pudo eliminar el producto: {err}")
            finally:
                cursor.close()
                conn.close()
        else:
            QMessageBox.critical(None, "Error", "No se pudo conectar a la base de datos.")


# Función para eliminar un producto
def eliminar_producto():
    nombre_producto = gui7.lineEdit2.text().strip()  # Obtener el nombre del producto

    if nombre_producto:
        conn = conectar_base_datos()
        if conn:
            cursor = conn.cursor()
            # Consulta para eliminar el producto
            query = "DELETE FROM Productos01 WHERE Nombre = %s"
            cursor.execute(query, (nombre_producto,))
            conn.commit()

            if cursor.rowcount > 0:  # Si se eliminó al menos un registro
                QMessageBox.information(None, "Éxito", f"Producto '{nombre_producto}' eliminado.")
                gui7.lineEdit2.clear()  # Limpiar el lineEdit
                actualizar_progress_bar()  # Actualizar la barra de progreso
                limpiar_tabla()  # Limpiar la tabla
            else:
                QMessageBox.warning(None, "Error", f"Producto '{nombre_producto}' no encontrado.")

            cursor.close()
            conn.close()
    else:
        QMessageBox.warning(None, "Advertencia", "Por favor, ingrese el nombre del producto.")



# Función para actualizar la progressBar (deberás definir cómo calcular el total)
def actualizar_progress_bar():
    # Lógica para calcular el total de productos y actualizar la progressBar
    conn = conectar_base_datos()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Productos01")
        total_productos = cursor.fetchone()[0]
        gui4.progressBar.setValue(total_productos)  # Asigna el total a la barra de progreso
        cursor.close()
        conn.close()

# Función para limpiar la tabla
def limpiar_tabla():
    gui4.tableWidget.setRowCount(0)  # Limpiar la tabla
    gui4.tableWidget.setColumnCount(0)  # Opción para limpiar las columnas si es necesario


def Salir3():
    gui7.hide()
    gui4.show()

def Salir4():
    gui4.hide()
    gui3.show()



    



def calibrar_producto():
    nombre_producto = gui9.lineEdit2.text().strip()  # Obtener el nombre del producto
    valor_slider = gui9.Slider.value()  # Obtener el valor actual del slider

    if nombre_producto:
        conn = conectar_base_datos()
        if conn:
            cursor = conn.cursor()

            # Consulta para obtener la cantidad actual del producto
            query = "SELECT Cantidad FROM Productos01 WHERE Nombre = %s"
            cursor.execute(query, (nombre_producto,))
            resultado = cursor.fetchone()

            if resultado:  # Si el producto existe
                # Convierte cantidad_actual a entero antes de realizar la suma
                cantidad_actual = int(resultado[0])  # Asegúrate de que sea un entero
                nueva_cantidad = cantidad_actual + valor_slider

                # Consulta para actualizar la cantidad del producto
                update_query = "UPDATE Productos01 SET Cantidad = %s WHERE Nombre = %s"
                cursor.execute(update_query, (nueva_cantidad, nombre_producto))
                conn.commit()

                QMessageBox.information(None, "Éxito", f"La cantidad del producto '{nombre_producto}' se ha actualizado a {nueva_cantidad}.")

                gui9.lineEdit2.clear()  # Limpiar el lineEdit
                gui9.lcdNumber.display(nueva_cantidad)  # Actualizar el LCD con la nueva cantidad
                
                limpiar_tabla()  # Limpiar la tabla si es necesario
            else:
                QMessageBox.warning(None, "Error", f"Producto '{nombre_producto}' no encontrado.")

            cursor.close()
            conn.close()
    else:
        QMessageBox.warning(None, "Advertencia", "Por favor, ingrese el nombre del producto.")

def actualizar_lcd(valor):
    gui9.lcdNumber.display(valor)  # Muestra el valor actual del slider en el lcdNumber



def conexion():
     broker = "9677ffc66171483a83133c060ddfbecc.s1.eu.hivemq.cloud"
     port = 8883  # Usar puerto seguro
     topic = "sensor/data"


    # Configuración del cliente MQTT
     cliente = mqtt.Client()
   
    # Configurar credenciales
     usuario = "Reyes8"  # Sustituye con tu nombre de usuario de HiveMQ Cloud
     contraseña = "Reyes1201"  # Sustituye con tu contraseña de HiveMQ Cloud
     cliente.username_pw_set(usuario, contraseña)
   
    # Habilitar TLS/SSL para HiveMQ
     cliente.tls_set()  # Configura automáticamente los certificados TLS predeterminados
   
    # Definir la función de callback cuando se conecta
     cliente.on_connect = on_connect
   
    # Conectar al broker con TLS/SSL
     print("Conectando al broker...")
     cliente.connect(broker, port, keepalive=60)
   
    # Iniciar el bucle de la red para gestionar la conexión y callbacks
     cliente.loop_start()


def Sensores():  
    gui3.hide()
    gui8.show()
    
 

def Salir5():
    gui8.hide()
    gui3.show()


   


# Función para leer y actualizar los valores del sensor
def leer_sensores(cliente_mqtt, puerto_serial, topico_mqtt):
    while True:
        try:
            line = puerto_serial.readline().decode('utf-8').strip()
            if "Temperatura:" in line and "Humedad:" in line:
                data = line.split(", ")
                temperatura = float(data[0].split(": ")[1].replace(" C", ""))
                humedad = float(data[1].split(": ")[1].replace(" %", ""))
                amp = round(random.uniform(0.0, 2.0), 2)

                # Actualizar los valores en la GUI (usar `after` para trabajar en el hilo principal)
                gui8.temp1.setText(f"Temperatura: {temperatura}°C")
                gui8.hum2.setText(f"Humedad: {humedad}%")
                gui8.amp2.setText(f"Amperaje: {amp}A")

                # Publicar datos en MQTT
                datos_sensor = {
                    "Temperatura": temperatura,
                    "Humedad": humedad,
                    "Amperaje": amp
                }
                cliente_mqtt.publish(topico_mqtt, json.dumps(datos_sensor))
                print(f"Datos enviados: {datos_sensor}")

                # Guardar datos en la base de datos
                conn = conectar_base_datos()
                if conn:
                    cursor = conn.cursor()
                    insert_query = """
                    INSERT INTO Datosalmacen01 (Temperatura, Humedad, Amperaje)
                    VALUES (%s, %s, %s)
                    """
                    try:
                        cursor.execute(insert_query, (temperatura, humedad, amp))
                        conn.commit()
                        print("Datos guardados en la base de datos.")
                    except Exception as db_err:
                        print(f"Error al guardar datos en la base de datos: {db_err}")
                    finally:
                        cursor.close()
                        conn.close()
                else:
                    print("No se pudo conectar a la base de datos.")

            time.sleep(5)  # Esperar 5 segundos antes de la próxima lectura

        except Exception as e:
            print(f"Error en la lectura del sensor: {e}")

# Función para iniciar la lectura en un hilo separado
def iniciar_lectura_sensores():
    # Configuración del cliente MQTT
    broker = "9677ffc66171483a83133c060ddfbecc.s1.eu.hivemq.cloud"
    port = 8883
    topic = "sensor/data"
    usuario = "Reyes8"
    contraseña = "Reyes1201"
    
    cliente = mqtt.Client()
    cliente.username_pw_set(usuario, contraseña)
    cliente.tls_set()
    cliente.connect(broker, port, keepalive=60)
    cliente.loop_start()

    # Configuración del puerto serial
    PORT = "COM4"
    BAUD_RATE = 9600
    try:
        ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
        ser.flushInput()
        print("Puerto serial iniciado correctamente.")
    except serial.SerialException as e:
        print(f"Error al abrir el puerto serial: {e}")
        return

    # Crear y arrancar el hilo para leer los sensores
    hilo_lectura = threading.Thread(target=leer_sensores, args=(cliente, ser, topic))
    hilo_lectura.daemon = True  # Permite cerrar el programa incluso si el hilo sigue activo
    hilo_lectura.start()

def retirarP():
    gui9.hide()
    gui7.show()

def AgregarP():
    gui7.hide()
    gui9.show()


# Ejecutar la función Sensar en un hilo separado
#threading.Thread(target=Sensar, daemon=True).start()
# Suponiendo que gui4 es tu instancia de la GUI
gui9.Slider.valueChanged.connect(actualizar_lcd)
#ui8.btnSensar.clicked.connect(Sensar)99*fffrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr
# Asignar la función al botón Calibrar
gui9.btnCalibrar.clicked.connect(calibrar_producto)
# Asignar la función al botón Alterar
#gui4.btnAlterar.clicked.connect(eliminar_producto)

# Conectar el botón en gui4
gui4.btnQr.clicked.connect(detectar_qr)  # Al presionar el botón de QR se llama a la función
gui7.btnEliminar.clicked.connect(eliminar_producto)  # Al presionar el botón de eliminar en gui7
gui7.actionSalir.triggered.connect(Salir3) #Salir del programa. 
# Conectar las señales de los botones
gui4.btnInspeccionar.clicked.connect(Tabla)
gui1.btnRegistrar.clicked.connect(registrar_principal)
gui2.btnRFID.clicked.connect(capturar_uid)
gui2.btnRegistrarUsuario.clicked.connect(registrar_usuario)
gui1.btnIngresar.clicked.connect(ingresar_usuario)
gui3.btnCerrarSesion.clicked.connect(cerrar_sesion)
gui3.btnInventario.clicked.connect(abrir_inventario)
gui5.btnAgregarArticulo.clicked.connect(agregar_producto)
gui4.Btn_Agregar.clicked.connect(agregar)
gui5.actionSalir.triggered.connect(Salir) #Salir del programa. 
gui9.Btn_retirar1.clicked.connect(retirar)
gui6.actionSalir.triggered.connect(Salir2) #Salir del programa. 
gui4.actionSalir.triggered.connect(Salir4) #Salir del programa. 
gui3.btnSensores.clicked.connect(Sensores)
gui8.actionSalir.triggered.connect(Salir5) #Salir del programa. 
gui7.Btn_Agregar1.clicked.connect(AgregarP)
gui9.actionSalir.triggered.connect(retirarP)
#gui8.Reanudar.clicked.connect(Sensar)
gui8.Reanudar.clicked.connect(iniciar_lectura_sensores)

# Ejecutar la aplicación
gui1.show()
app.exec_()
