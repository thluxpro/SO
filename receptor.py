import socket
import struct

MULTICAST_GROUP = '224.1.1.1'
PORT = 5007

def start_multicast_receiver():
    # Crear socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    
    # Permitir reuso de la dirección
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Enlazar el socket al puerto
    sock.bind(('', PORT))

    # Unirse al grupo multicast
    group = socket.inet_aton(MULTICAST_GROUP)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"🟢 Nodo escuchando mensajes multicast en {MULTICAST_GROUP}:{PORT}...")
    
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"📩 Mensaje recibido desde {addr}: {data.decode()}")

if __name__ == '__main__':
    start_multicast_receiver()
