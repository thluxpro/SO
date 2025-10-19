import socket
import struct
import threading

MULTICAST_GROUP = '224.1.1.1'
MULTICAST_PORT = 5007
EXTERNAL_PORT = 6000  # Puerto para recibir mensajes externos
TTL = 1  # Solo red local

def multicast_sender(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    ttl_bin = struct.pack('b', TTL)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)
    sock.sendto(message.encode(), (MULTICAST_GROUP, MULTICAST_PORT))
    sock.close()
    print(f"📢 Mensaje reenviado al grupo multicast: {message}")

def handle_external_client(conn, addr):
    print(f"🌐 Cliente externo conectado desde {addr}")
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f"📥 Mensaje recibido del cliente externo: {data}")
            multicast_sender(data)
    except ConnectionResetError:
        print("🔌 Cliente desconectado")
    finally:
        conn.close()

def start_coordinator():
    # Crear socket TCP para recibir mensajes externos
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('', EXTERNAL_PORT))
    server_sock.listen(5)
    
    print(f"🚀 Coordinador activo")
    print(f"🔊 Escuchando mensajes externos en TCP puerto {EXTERNAL_PORT}")
    print(f"📡 Reenviando mensajes al grupo {MULTICAST_GROUP}:{MULTICAST_PORT}")

    while True:
        conn, addr = server_sock.accept()
        thread = threading.Thread(target=handle_external_client, args=(conn, addr))
        thread.start()

if __name__ == '__main__':
    start_coordinator()
