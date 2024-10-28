#importar librerias
import cv2
import numpy as np
from PyQt5 import QtWidgets, uic 
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap

#Configuraciones iniciales
app = QtWidgets.QApplication([])
gui = uic.loadUi('GUI_VISION.ui')
cap = cv2.VideoCapture(0)
proceso = 'normal'
video_activo = False

#funciones de apoyo
def display_image(img, label): #argumentos entre parentesis
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #convertimos de BGR a RGB
    h, w, ch = img.shape #pedir tamaño de nuestra imagen
    byte_per_line = ch * w
    qimg = QImage(img.data, w, h, byte_per_line, QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(qimg)
    label.setPixmap(pixmap) #asignar el pixmap al qlabel
    label.setScaledContents(True) #Se escala automaticamente

def detect_edge(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #IMAGEN A ESCALA DE GRISES 
    edges = cv2.Canny(gray, 100, 200)
    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR) #PODERLO MOSTRAR EN EL VIDEO EN VIVO

def aplly_filter(frame): 
    return cv2.GaussianBlur(frame, (15,15), 0)

def display_red_channel(frame):
    img_red = frame[:, :, 2]  # Extraer el canal rojo
    return cv2.merge([np.zeros_like(img_red), np.zeros_like(img_red), img_red])  # Mantener solo el canal rojo

def convert_to_grayscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convertir a escala de grises

def binarize_image(frame, threshold=127):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convertir a escala de grises
    _, binary_image = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)  # Binarización
    return cv2.cvtColor(binary_image, cv2.COLOR_GRAY2BGR)  # Convertir de nuevo a BGR para mostrar

def set_edge_detection_mode():
    global proceso
    proceso = 'bordes'

def set_filter_mode():
    global proceso 
    proceso = 'filtro'

def set_red_channel_mode():
    global proceso
    proceso = 'canal_rojo'

def set_grayscale_mode():
    global proceso
    proceso = 'escala_grises'

def set_binarization_mode():
    global proceso
    proceso = 'binarizacion'

def set_normal_mode():
    global proceso
    proceso = 'normal'

#creacion de hilo 
class VideoThread(QThread):
    changePixmap = pyqtSignal(np.ndarray)
    changePixmapProcessado = pyqtSignal(np.ndarray) #frame original

    def run(self):
        global proceso, video_activo
        video_activo = True
        while video_activo: 
            ret, frame = cap.read()
            if ret:
                self.changePixmap.emit(frame) #emite el frame original
                if proceso == 'bordes':
                    processed_frame = detect_edge(frame)
                elif proceso == 'filtro':
                    processed_frame = aplly_filter(frame)
                elif proceso == 'canal_rojo':
                    processed_frame = display_red_channel(frame)
                elif proceso == 'escala_grises':
                    processed_frame = convert_to_grayscale(frame)
                elif proceso == 'binarizacion':
                    processed_frame = binarize_image(frame)
                else: 
                    processed_frame = frame
                self.changePixmapProcessado.emit(processed_frame) #pix map procesado

    def stop(self): 
        global video_activo
        video_activo = False
        self.quit()
        self.wait()

# Creación de instancia del hilo sin iniciar
worker = VideoThread()

#acciones complementarias
worker.changePixmap.connect(lambda frame: display_image(frame, gui.lbl_original)) 
worker.changePixmapProcessado.connect(lambda frame: display_image(frame, gui.lbl_procesado))

# Función para iniciar el video
def iniciar_video():
    if not worker.isRunning():
        worker.start()

# Función para detener el video
def detener_video():
    if worker.isRunning():
        worker.stop()
        cap.release()
        gui.lbl_original.clear()
        gui.lbl_procesado.clear()

# Conectar botones a las funciones
gui.inciar_video.clicked.connect(iniciar_video)
gui.Bordes.clicked.connect(set_edge_detection_mode)
gui.Gaussiano.clicked.connect(set_filter_mode)
gui.CanalRojo.clicked.connect(set_red_channel_mode)  # Nuevo botón Canal Rojo
gui.Grises.clicked.connect(set_grayscale_mode)  # Nuevo botón Escala de Grises
gui.Binario.clicked.connect(set_binarization_mode)  # Nuevo botón Binarización
gui.actionSAlir.triggered.connect(detener_video)

gui.show()
app.exec()
