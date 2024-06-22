import cv2 as cv
import qrcode
from pyzbar.pyzbar import decode
import time

def testVelocidadReceptor():
    error = ""

    tiempoTotalTrxACK = 0

    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        error = "camera"
        return error

    for i in range(10):
        data = i

        ACK = "ACK"+str(i)

        siguiente = False

        while not siguiente:
            ret, frame = cap.read()
            if not ret:
                error= "frame"
                break

            qr_codes = decode(frame)

            for qr_code in qr_codes:
                qr_data = qr_code.data.decode('utf-8')

                if qr_data == str(data):

                    if qr_data != 0:
                        cv.destroyAllWindows()

                    tiempoInicial = time.time()

                    qr = qrcode.QRCode(
                        version=5,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4,
                    )

                    qr.add_data(ACK)
                    qr.make(fit=False)

                    img = qr.make_image(fill_color="black", back_color="white")

                    img.save("qr_test_receptor.png")

                    img2 = cv.imread("qr_test_receptor.png")

                    cv.imshow(f"ACK {i}", img2)
                    cv.moveWindow(f"ACK {i}", 450, 20)

                    tiempoIntermedio = time.time()

                    siguiente = True
                    tiempoTrxACK = tiempoIntermedio-tiempoInicial
                    tiempoTotalTrxACK += tiempoTrxACK

            key = cv.waitKey(1)
            if key == 27:
                tiempoTrxACK = tiempoIntermedio - tiempoInicial
                tiempoTotalTrxACK += tiempoTrxACK
                break

    time.sleep(1)
    cv.destroyAllWindows()
    cap.release()
    mediaTiempoTrxACK = round(tiempoTotalTrxACK/10, 2)

    return error, mediaTiempoTrxACK