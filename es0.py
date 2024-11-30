import cv2
import socket
import struct
import time

ip = '192.168.1.9'  # Cambia a tu IP
puerto = 5555

def enviar_imagen(indice):
    cap = cv2.VideoCapture(indice)
    if not cap.isOpened():
        print("No se pudo abrir la cámara.")
        return

    # Conectar al servidor
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((ip, puerto))

    time.sleep(2)  # Espera para estabilizar la conexión

    while True:
        success, frame = cap.read()
        if not success:
            print("No se pudo leer el frame de la cámara.")
            break

        # Codificar el frame como JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        mensaje = buffer.tobytes()

        # Enviar el tamaño del frame primero
        cliente_socket.sendall(struct.pack("!I", len(mensaje)))

        # Luego enviar el frame
        cliente_socket.sendall(mensaje)

        # Esperar un segundo antes de enviar el siguiente frame
        time.sleep(1)

    cap.release()
    cliente_socket.close()

if __name__ == '__main__':
    enviar_imagen(0)  # Cambia el índice si necesitas usar otra cámara
