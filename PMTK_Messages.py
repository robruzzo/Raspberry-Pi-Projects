import serial
startBaud=9600
baud = 9600
baudrate=str(baud)
bytesize = serial.EIGHTBITS
#Data Variables
byte=''           #Byte to determine if sentences are being transmitted
ser = serial.Serial("/dev/ttyS0",baudrate=startBaud, bytesize=bytesize, timeout=1)



def createBaudRatePacket(baudrate):
    packet="PMTK251"+","+baudrate
    check=checksum(packet)[2:]
    if len(check)==1:
        check="0"+check
    output="$"+packet+"*"+check+"\r\n"
    output=output.upper()
    output=str.encode(output)
    return output
    
def createTestPacket():
    packet="PMTK000"
    check=checksum(packet)[2:]
    if len(check)==1:
        check="0"+check
    output="$"+packet+"*"+check+"\r\n"
    output=output.upper()
    output=str.encode(output)
    return output

def createNMEAOutputPacket(GPGLL=0, GPRMC=1, GPVTG=0, GPGGA=1, GPGSA=0, GPGSV=0, GPGRS=0, GPGST=0,GPZDA=0, MCHN=0, DTM=0,Default=False):
    if Default:
        packet="PMTK314,-1"
    else:
        packet="PMTK314"+","+str(GPGLL)+","+str(GPRMC)+","+str(GPVTG)+","+str(GPGGA)+","+str(GPGSA)+","+str(GPGSV)+","+str(GPGRS)+","+str(GPGST)+",0,0,0,0,0,0,0,0,0,"+str(GPZDA)+","+str(MCHN)+","+str(DTM)
    check=checksum(packet)[2:]
    if len(check)==1:
        check="0"+check
    output="$"+packet+"*"+check+"\r\n"
    output=output.upper()
    output=str.encode(output)
    return output


def checksum(packet):
    checksum = 0
    for el in packet:
        checksum ^= ord(el)
    return hex(checksum)
    
def sendPacket(packet):
    ser.flush()
    ser.write(packet)
    ser.flush()
    print("Sent output, awaiting response...")

def awaitResponse(i):
    x=0
    responded = False
    #ser.flushInput()
    while x<i:
        response=ser.readline()
        print(response)
        if len(response)>1:
            response=response.decode()
            if response.strip().split(',')[0][1:5]=="PMTK":
                break
        x+=1
    if len(response)>1:
        if response.strip().split(',')[0][1:8]=="PMTK001":
            command=response.strip().split(',')[1]
            response_flag=response.strip().split(',')[2][0]
            if response_flag=="0":
                response_text="Invalid command or packet"
            if response_flag=="1":
                response_text="Unsupported command or packet type"
            if response_flag=="2":
                response_text="Valid command and packet, but action failed"
            if response_flag=="3":
                response_text="Valid command and packet, action succeeded"
            print("Command: "+command+"  Response: "+response_text)
    else:
        print("ERROR: FAILED TO ACKNOWLEDGE")
 
def grabAndPrintData(num):
    x=0
    ser.flushInput()
    while x < num:
        response=ser.readline()
        if len(response)>1:
            response=response.decode()
            if response.strip().split(',')[0][0]=="$":
                print(response)
        x+=1
