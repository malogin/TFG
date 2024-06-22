import qrcode
import cv2 as cv
from pyzbar.pyzbar import decode
import diccionario
import time

#version = 18
#input_path = "C:/Users/Manolo/Desktop/Archivos_originales/SampleText.txt"

def emisor(version, input_path):

    error = ""

    fragment_size = diccionario.diccionario_fragmentos[version]
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        #print("Cannot open camera")
        error = "camera"
        return error

    try:
        with open(input_path, 'rb') as file:
            file_data = bytearray(file.read())
    except FileNotFoundError:
        #print(f"Error: El archivo '{input_path}' no fue encontrado.")
        error = "fileNotFound"
    except Exception as e:
        #print(f"Error al leer el archivo: {e}")
        error = "cannotReadFile"

    # Dividir el archivo en fragmentos
    fragments = [file_data[i:i + fragment_size] for i in range(0,len(file_data), fragment_size)]
    n_fragments = int(len(file_data)/fragment_size)
    n_fragments_hex = hex(n_fragments)[2:].zfill(3)

    for i, fragment in enumerate(fragments):
        hex_string = fragment.hex()
        con_cabecera =n_fragments_hex + hex(i)[2:].zfill(3) + hex_string

        qr = qrcode.QRCode(
            version = version,
            error_correction = qrcode.constants.ERROR_CORRECT_L,
            box_size = diccionario.diccionario_box_size[version],
            border = 4,
        )
        qr.add_data(con_cabecera)
        qr.make(fit=False)

        img = qr.make_image(fill_color = "black", back_color = "white")

        img.save("codigo_qr.png")

        tiempoInicial = time.time()
        siguiente = False
        contTimeOut = 0

        while not siguiente:
            img2 = cv.imread("codigo_qr.png")

            cv.imshow(f"Codigo QR {i+1}", img2)
            cv.moveWindow(f"Codigo QR {i+1}", 450, 0)

            tiempoActual = time.time()
            tiempoTranscurrido = tiempoActual - tiempoInicial

            if tiempoTranscurrido > 10:
                contTimeOut+=1
                tiempoInicial = time.time()
                cv.destroyAllWindows()

                if contTimeOut == 5:
                    break

            ret, frame = cap.read()
            if not ret:
                #print("Error al capturar el fotograma de la cámara.")
                error = "frame"
                break

            qr_codes = decode(frame)

            for qr_code in qr_codes:
                qr_data = qr_code.data.decode('utf-8')

                if qr_data == "ACK"+str(i):
                    siguiente = True

            key = cv.waitKey(1)
            if key == 27: #Esc
                break

        cv.destroyAllWindows()

        if contTimeOut == 5:
            #print("Error en la transmisión: Time Out")
            error = "timeout"
            break


    cap.release()
    return error

#emisor(version,input_path)