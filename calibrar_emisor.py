import qrcode
import cv2 as cv
from pyzbar.pyzbar import decode
import time
import diccionario

def calibrar_emisor():
    error = ""
    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        #print("Cannot open camera")
        error = "camera"
        version = None
        return version, error

    mensaje = "Calibrar"

    for i in range (1,41):
        qr =  qrcode.QRCode(
            version=min(i,40),
            error_correction = qrcode.constants.ERROR_CORRECT_L,
            #box_size=max((16 - 0.5*i), 4),
            box_size=diccionario.diccionario_box_size[i],
            border=4,
        )
        qr.add_data(mensaje + str(i))
        qr.make(fit=False)

        img = qr.make_image(fill_color = "black", back_color = "white")

        img.save("calibrar_qr.png")

        terminar = False
        tiempo_inicial = time.time()
        siguiente = False

        while not siguiente:
            tiempo_actual = time.time()
            tiempo_transcurrido = tiempo_actual - tiempo_inicial

            if tiempo_transcurrido > 10:
                siguiente = True
                terminar = True

            img2 = cv.imread("calibrar_qr.png")

            cv.imshow(f"QR Version {i}", img2)
            cv.moveWindow(f"QR Version {i}", 450, 0)

            ret, frame = cap.read()
            if not ret:
                #print("Error al capturar el fotograma de la cámara.")
                error = "frame"
                version = None
                cv.destroyAllWindows()
                return version, error

            qr_codes = decode(frame)

            for qr_code in qr_codes:
                qr_data = qr_code.data.decode('utf-8')

                if qr_data == "ACK"+str(i):
                    siguiente = True

            key = cv.waitKey(1)
            if key == 27:  # Esc
                break

        cv.destroyAllWindows()
        if terminar:
            break
    if i == 1 or i == 40:
        version=i
    else:
        version=i-1

    #print(F"Calibración terminada, versión óptima: {version}")

    cap.release()

    return version, error