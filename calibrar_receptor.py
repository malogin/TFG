import cv2 as cv
import qrcode
from pyzbar.pyzbar import decode
import time

def calibrar_receptor():
    error = ""

    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        #print("Cannot open camera")
        error = "camera"
        return error

    for i in range(1,41):
        terminar = False
        tiempoInicial = time.time()
        siguiente = False

        while not siguiente:
            tiempoActual= time.time()
            tiempoTranscurrido = tiempoActual-tiempoInicial

            if tiempoTranscurrido > 10:
                siguiente = True
                terminar = True

            ret,frame = cap.read()
            if not ret:
                #print("Error al capturar el fotograma de la cámara.")
                error = "frame"
                break

            qr_codes = decode(frame)

            for qr_code in qr_codes:
                qr_data = qr_code.data.decode('utf-8')

                if qr_data == "Calibrar" + str(i):

                    if i != 1:
                        cv.destroyAllWindows()

                    ACK = "ACK"+str(i)

                    qr = qrcode.QRCode(
                        version = 5,
                        error_correction = qrcode.constants.ERROR_CORRECT_L,
                        box_size= 10,
                        border= 4,
                    )

                    qr.add_data(ACK)
                    qr.make(fit=False)

                    img = qr.make_image(fill_color = "black", back_color = "white")

                    img.save("qr_ack_calibracion.png")

                    img2 = cv.imread("qr_ack_calibracion.png")
                    cv.imshow(f"ACK {i+1}", img2)
                    cv.moveWindow(f"ACK {i+1}", 450, 20)

                    siguiente = True
                    break

            key = cv.waitKey(1)
            if key == 27:
                break

        if terminar:
            break

    time.sleep(1)
    cv.destroyAllWindows()
    cap.release()
    return error
