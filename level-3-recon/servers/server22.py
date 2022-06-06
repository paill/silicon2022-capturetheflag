
import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65422  # Port to listen on (non-privileged ports are > 1023)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            data = 'mwah HA HA ha HA ha ha ha\n'
            conn.sendall(data.encode())
