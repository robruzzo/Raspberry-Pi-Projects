import socket
from gpiozero import LED
from time import sleep

led = LED(23)
socket_status=True
connection=True
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
host =''
port=1234
s.bind((host,port))
s.listen(1)

while socket_status:
  conn, addr = s.accept() 
  print('Got connection from', addr)
  connection=True
  while connection:
      data =conn.recv(1024)
      data=data.decode()
      if(data=='close'):
          print("Closing Connection")
          connection=False
          conn.close()
          break;
      if(data=='quit'):
          print("Ending server")
          connection=False
          socket_status=False
          break;
      else:
          print(data)
          data=data.encode()
          conn.send(data)

s.close()

