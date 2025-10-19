import socket
import struct

MULTICAST_GROUP = '224.1.1.1'
PORT = 5007
TTL = 1  # Sólo red local

def cliente_externo():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    ttl_bin = struct.pack('b', TTL)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)

    print("🌐 Cliente externo listo para enviar mensajes al grupo multicast.")
    while True:
        mensaje = input("Ingrese el mensaje a enviar al grupo: ")
        sock.sendto(f"EXTERNO: {mensaje}".encode(), (MULTICAST_GROUP, PORT))
        print("✅ Mensaje enviado desde el cliente externo.")

if __name__ == '__main__':
    cliente_externo()
