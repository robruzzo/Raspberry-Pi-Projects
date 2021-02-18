import socket

HOST='10.10.10.199'
PORT = 14141

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, add = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                data = '00'
                conn.sendall(data)
            else:
                conn.sendall(data)
