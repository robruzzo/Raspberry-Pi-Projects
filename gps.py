
import serial
from time import sleep

#ser = serial.Serial("/dev/ttyAMA0",9600) # Open port with 96k baud
ser = serial.Serial("/dev/ttyS0",9600) # Open port with 96k baud

x=0
byte=''
time=0
lat=0
latD=0
long=0
longD=0
quality=0
numSV=0


while x <20:
    while byte !='$':
        byte= ser.read()
    message = ser.readline()
    #print(message)
    if(message.strip().split(','))[0]=="$GPGGA":
        data=(message.strip().split(','))
        time=data[1]
        lat=data[2]
        latD=data[3]
        long=data[4]
        longD=data[5]
        quality=data[6]
        numSV=data[7]
        if numSV=='00':
            print("Signal too weak!")
            print(data)
        else:
            print("Time: ",time)
            print("Latitude: ",lat +" "+latD+ "  Longitude: "+long+" "+longD )
            print("Number of Satellites: ", numSV)
            print("Relative Strength: ",int(numSV)/12.0)
        x+=1

    
