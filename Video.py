import cv2

cam = cv2.VideoCapture(0) #0 por la camra local 

if not cam.isOpened():
    print("No se puede abrir la camara") #chequeos de calidad que si funcione
    exit()

while True:
    ret, frame = cam.read()
    if not ret: 
        print("No se recibio el fotograma") 
        break 

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #aplicar filtro
    bordes= cv2.Canny(gray, 100, 200)
    cv2.imshow('video en vivo', frame)
    cv2.imshow('bordes deteccion',bordes)

    cv2.imshow('Video en vivo', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cam.release
cv2.destroyAllWindows()

