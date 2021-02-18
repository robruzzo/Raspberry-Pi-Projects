import socket
import time

host="192.168.0.1"
port=1234


s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
message="Hello"
message=message.encode()
s.send(message)

time.sleep(2)

message="ledon"
message=message.encode()
s.send(message)

time.sleep(2)

message="quit"
message=message.encode()
s.send(message)
s.close()
