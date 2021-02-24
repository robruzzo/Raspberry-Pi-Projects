import serial
startBaud=9600
baud = 9600
baudrate=str(baud)
bytesize = serial.EIGHTBITS
#Data Variables
byte=''           #Byte to determine if sentences are being transmitted
ser = serial.Serial("/dev/ttyS0",baudrate=startBaud, bytesize=bytesize, timeout=1)

def checksum(packet):
    checksum = 0
    for el in packet:
        checksum ^= ord(el)
    return hex(checksum)

def createBaudRatePacket(baudrate):
    packet="PMTK251"+","+baudrate
    check=checksum(packet)[2:]
    output="$"+packet+"*"+check+"\r\n"
    output=output.upper()
    output=str.encode(output)
    return output
    
def sendPacket(packet):
    print(packet)
    ser.write(packet)
    ser.flush()
    print("Sent output, awaiting response...")

def awaitResponse(i):
    x=0
    responded = False
    while x<i:
        response=ser.readline()
        print(response)
        response=response.decode()
        if response.strip().split(',')[0][1:5]=="PMTK":
            break
        x+=1
    if response.strip().split(',')[0][1:5]=="PMTK":
        command=response.strip().split(',')[1]
        response_flag=response.strip().split(',')[2][0]
        print("Command: "+command+"  Response: "+response_flag)
    else:
        print("ERROR: FAILED TO ACKNOWLEDGE")
    
    
def createTestPacket():
    packet="PMTK000"
    check=checksum(packet)[2:]
    output="$"+packet+"*"+check+"\r\n"
    output=output.upper()
    output=str.encode(output)
    return output

testPacket=createTestPacket()
sendPacket(testPacket)
awaitResponse(30)

baudPacket = createBaudRatePacket(baudrate)
print(baudPacket)
sendPacket(baudPacket)
ser.baudrate=baud
awaitResponse(30)


testPacket=createTestPacket()
sendPacket(testPacket)
awaitResponse(30)

'''
baudPacket = createBaudRatePacket(baudrate)
testPacket=createTestPacket()
print(baudPacket)
print(testPacket)
'''