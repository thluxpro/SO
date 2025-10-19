import socket
import struct
import threading

MULTICAST_GROUP = '224.1.1.1'
PORT = 5007
TTL = 1  # Solo red local

def receptor(nodo_nombre):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', PORT))

    grupo_binario = socket.inet_aton(MULTICAST_GROUP)
    mreq = struct.pack('4sL', grupo_binario, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"🟢 [{nodo_nombre}] escuchando mensajes en {MULTICAST_GROUP}:{PORT}")

    while True:
        data, addr = sock.recvfrom(1024)
        print(f"\n📩 [{nodo_nombre}] recibió -> {data.decode()} (desde {addr})")

def emisor(nodo_nombre):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    ttl_bin = struct.pack('b', TTL)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)

    print(f"✉ [{nodo_nombre}] puede enviar mensajes al grupo. Escriba y presione ENTER.")

    while True:
        mensaje = input("> ")
        mensaje_final = f"{nodo_nombre}: {mensaje}"
        sock.sendto(mensaje_final.encode(), (MULTICAST_GROUP, PORT))
        print(f"✅ Mensaje enviado: {mensaje_final}")

if __name__ == '__main__':
    nodo_nombre = input("Ingrese el nombre de este nodo (ej: Nodo1, Nodo2, Nodo3): ")

    # Iniciar receptor en un hilo independiente
    threading.Thread(target=receptor, args=(nodo_nombre,), daemon=True).start()

    # Iniciar emisor
    emisor(nodo_nombre)

