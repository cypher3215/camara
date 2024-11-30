# pip install opencv-python-headless
import socket
import numpy as np
import cv2
import struct

ip = '192.168.1.10'  # Cambia a tu IP
puerto = 5555

def servidor():
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind((ip, puerto))
    servidor_socket.listen(1)

    print("Esperando conexión...")
    cliente_socket, _ = servidor_socket.accept()
    print("Cliente conectado.")

    data = b""
    payload_size = struct.calcsize("!I")  # Usar "!" para red orden

    while True:
        # Recibir tamaño del frame
        while len(data) < payload_size:
            packet = cliente_socket.recv(4096)
            if not packet:
                break
            data += packet

        if not data:
            break

        # Obtener el tamaño del frame
        packed_size = data[:payload_size]
        data = data[payload_size:]
        frame_size = struct.unpack("!I", packed_size)[0]

        # Recibir el frame
        while len(data) < frame_size:
            packet = cliente_socket.recv(4096)
            if not packet:
                break
            data += packet

        if len(data) < frame_size:
            break

        frame_data = data[:frame_size]
        data = data[frame_size:]

        # Procesar la imagen recibida
        nparr = np.frombuffer(frame_data, np.uint8)
        imagen = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if imagen is not None:
            cv2.imshow('Imagen recibida', imagen)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("No se pudo decodificar la imagen.")

    cliente_socket.close()
    servidor_socket.close()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    servidor()