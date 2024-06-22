import qrcode
import cv2 as cv
from pyzbar.pyzbar import decode
import diccionario
import time

def testVelocidadEmisor(version):

    error = ""

    tiempoTotal=0
    tiempoTotalTrx=0

    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        error = "camera"
        return error

    for i in range (10):
        data = i

        tiempoInicial = time.time()

        qr = qrcode.QRCode(
            version = version,
            error_correction = qrcode.constants.ERROR_CORRECT_L,
            box_size = diccionario.diccionario_box_size[version],
            border=4,
        )

        qr.add_data(data)
        qr.make(fit=False)

        img = qr.make_image(fill_color = "black", back_color = "white")
        img.save("qr_test_emisor.png")

        tiempoIntermedio = time.time()

        siguiente = False

        while not siguiente:
            img2 = cv.imread("qr_test_emisor.png")

            cv.imshow(f"Codigo QR {i+1}", img2)
            cv.moveWindow(f"Codigo QR {i+1}", 450, 0)

            ret, frame = cap.read()
            if not ret:
                error = "frame"
                break

            qr_codes = decode(frame)

            for qr_code in qr_codes:
                qr_data = qr_code.data.decode('utf-8')

                if qr_data == "ACK"+str(i):
                    siguiente = True
                    tiempoActual = time.time()
                    tiempoProp = tiempoActual-tiempoInicial
                    tiempoTrx = tiempoIntermedio-tiempoInicial
                    tiempoTotal += tiempoProp
                    tiempoTotalTrx += tiempoTrx

            key = cv.waitKey(1)
            if key == 27: #Esc
                tiempoActual = time.time()
                tiempoProp = tiempoActual - tiempoInicial
                tiempoTrx = tiempoIntermedio - tiempoInicial
                tiempoTotal += tiempoProp
                tiempoTotalTrx += tiempoTrx
                break

        cv.destroyAllWindows()

    cap.release()
    mediaTiempo = tiempoTotal/10
    mediaTiempoTrx = tiempoTotalTrx/10
    mediaVelocidad = round((8*diccionario.diccionario_byte_size[version])/mediaTiempo,2)

    return error, mediaTiempo, mediaTiempoTrx, mediaVelocidad

#error, mediaTiempo = testVelocidadEmisor(18)

#print(mediaTiempo)