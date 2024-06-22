import cv2 as cv
import qrcode
from pyzbar.pyzbar import decode
from binascii import unhexlify
import time

#output_file = "C:/Users/Manolo/Desktop/Archivos_reconstruidos/SampleTextReconstruido.txt"

def receptor(output_file):

    error= ""

    datos_reconstruidos = b''

    cont = 0

    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        #print("Cannot open camera")
        error = "camera"
        return error

    tiempoEnvio= time.time()

    terminar = False
    while not terminar:
        tiempoInicial = time.time()
        siguiente = False
        contTimeOut = 0

        while not siguiente:
            ret,frame = cap.read()
            if not ret:
                #print("Error al capturar el fotograma de la cámara.")
                error = "frame"
                break

            tiempoActual = time.time()
            tiempoTranscurrido = tiempoActual - tiempoInicial

            if tiempoTranscurrido > 10:
                contTimeOut+=1
                tiempoInicial=time.time()

                if contTimeOut == 5:
                    error = "timeout"
                    siguiente=True
                    terminar=True

            qr_codes = decode(frame)

            for qr_code in qr_codes:
                qr_data = qr_code.data.decode('utf-8')

                n_fragmentos = qr_data[0:3]
                fragmento = qr_data[3:6]

                if int(n_fragmentos,16) == int(fragmento,16):
                    datos_reconstruidos += unhexlify(qr_data[6:])
                    terminar = True

                if cont == int(fragmento,16):
                    if cont != 0:
                        cv.destroyAllWindows()

                    ACK = "ACK" + str(int(fragmento,16))

                    qr = qrcode.QRCode(
                        version = 5,
                        error_correction = qrcode.constants.ERROR_CORRECT_L,
                        box_size = 10,
                        border = 4,
                    )

                    qr.add_data(ACK)
                    qr.make(fit=False)

                    img = qr.make_image(fill_color = "black", back_color = "white")

                    img.save("qr_ack.png")
                    img2 = cv.imread("qr_ack.png")
                    cv.imshow(f"ACK {int(fragmento,16)+1}", img2)
                    cv.moveWindow(f"ACK {int(fragmento,16)+1}", 450,20)

                    datos_reconstruidos += unhexlify(qr_data[6:])
                    siguiente = True

                    cont += 1
                    break

            key = cv.waitKey(1)
            if key == 27:   #break
                break

    cap.release()

    if datos_reconstruidos:
        try:
            with open(output_file, 'wb') as archivo:
                archivo.write(datos_reconstruidos)
                tiempoFinal = time.time()
                tiempoTotal = tiempoFinal-tiempoEnvio
                print(tiempoTotal)
                cv.destroyAllWindows()

            #print(f"Archivo reconstruido y guardado en '{output_file}'")

        except Exception as e:
            #print(f"Error al reconstruir el archivo: {e}")
            error = "reconstruir"
    return error

#receptor(output_file)