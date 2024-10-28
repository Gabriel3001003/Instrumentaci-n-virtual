#importar librerias 
import cv2 

img = cv2.imread("YUKAMAKIS.jpeg")
cv2.imshow("Imagen referencia", img)

#rescaladod e imagen
img_res = cv2.resize(img, (400,200), interpolation=cv2.INTER_CUBIC)
cv2.imshow('Imagen rescalada', img_res)

#separacion de canales
img_red= img[:,:,2]
cv2.imshow('Canal Rojo', img_red) #Leer los colores en la imagen canal rojo

img_green= img[:,:,1]
cv2.imshow('Canal Verde', img_green) #Leer los colores en la imagen canal verde

img_blue= img[:,:,0]
cv2.imshow('Canal azul', img_blue) #Leer los colores en la imagen canal azul

#filtro
blur = cv2.GaussianBlur(img, (3,3), 0)
cv2.imshow("imagen suavizada", blur)

bordes = cv2.Canny(img, 100, 200)
cv2.imshow("bordes", bordes)


contornos,_ = cv2.findContours(bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
for contorno in contornos:
    area = cv2.contourArea(contorno)
    print("Área del contorno:", area)


tamaño = img.shape
print(tamaño)
cv2.waitKey(0) #parte del codigo ara cerrar con una tecla 
cv2.destroyAllWindows