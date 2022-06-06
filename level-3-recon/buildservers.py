
def code(data, port):
    if port < 10:
        port = "0"+str(port)
    else:
        port = str(port)
    text = r"""
import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 654"""+port+"""  # Port to listen on (non-privileged ports are > 1023)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            data = '"""+data+"""\\n'
            conn.sendall(data.encode())
"""
    return text

with open("encodings.txt", "r") as f:
    for num, line in enumerate(f):
        print(f"su -c 'python3 /app/server{num}.py &' goomba")
        with open(f"servers/server{num}.py", "w") as w:
            w.write(code(line.strip(), num))
