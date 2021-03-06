#Written for python 3.x
import serial
from time import sleep
import io

'''
Port - Set depending on how your raspberry pi is configured and what generation it is:
1: /dev/ttyAMA0
2: /dev/ttyS0

Baud: typically 9600

Output - NMEA 0183 V2.3 Sentences:
RMC - Recommended minimum data for GPS (message[0])
VTG - Vector track and speed over the ground
GGA - Fix Information
GSA - Overall Satellite Data
GSV - Detailed sattelite Data x4
GLL - Latitude/Longitude Data

Position Fix Flags:

Status (GLL, RMC): V = Invalid, A = Data valid
Quality (GGA): 0 = No Fix, 1= Autonomous GNSS Fix, 2 = Differential GNN Fix, 6= Estimated/Dead Reckoning Fix
navMode (GSA): 1 = No Fix, 2 = 2D Fix, 3 = 3D Fix
posMode (GLL, RMC, VTG, GNS) : N = No Fix, E = Estimated/Dead Reckoning Fix, A= Autonomous GNSS Fix, D = Differential GNSS Fix
'''

class SIM33EAU:
    def __init__(self, port,baud,GLL=0,RMC=1,VTG=1,GGA=1,GSA=1,GSV=1,GRS=0,GST=0,ZDA=0,MCHN=0,DTM=0):
        #Define setup parameters
        self.port = port
        self.baud = baud
        self.bytesize = serial.EIGHTBITS
        #Data Variables
        self.byte=''           #Byte to determine if sentences are being transmitted
        '''
        Set defaults, in this case all items that are in the default message group are set to 1
        to change configuration, set all values that are needed in the NMEA message group to 1-5,
        and all others to 0. 1 Means it will be output every iteration, 5 means it will be output
        every 5 iterations (less frequent).Then run the UpdateNMEAOutputMessage method to change the configuration
        '''
        self.GLL=GLL
        self.RMC=RMC
        self.VTG=VTG
        self.GGA=GGA
        self.GSA=GSA
        self.GSV=GSV
        self.GRS=GRS
        self.GST=GST
        self.ZDA=ZDA
        self.MCHN=MCHN
        self.DTM=DTM
        
        self.messageCount=5

        
        if self.port =='1':
            self.ser = serial.Serial("/dev/ttyAMA0",baudrate=self.baud, bytesize=self.bytesize, timeout=1)
        if self.port =='2':
            self.ser = serial.Serial("/dev/ttyS0",baudrate=self.baud, bytesize=self.bytesize, timeout=1)
            
        self.UpdateNMEAOutputMessage()
        
    def getNumMessages(self):
        self.messageCount=0
        if self.GLL>0:
            self.messageCount+=1
        if self.RMC>0:
            self.messageCount+=1
        if self.VTG>0:
            self.messageCount+=1
        if self.GGA>0:
            self.messageCount+=1
        if self.GSA>0:
            self.messageCount+=1
        if self.GSV>0:
            self.messageCount+=1
        if self.GRS>0:
            self.messageCount+=1
        if self.GST>0:
            self.messageCount+=1
        if self.ZDA>0:
            self.messageCount+=1
        if self.MCHN>0:
            self.messageCount+=1
        if self.DTM>0:
            self.messageCount+=1
            
    def getMessage(self):
        loop_start = False
        messages = []
        msgNum=0
        while loop_start==False:
            message= self.ser.readline()
            message=message.decode("utf-8")
            if message[0]=='$':
                if (message.strip().split(','))[0][3:]=="PMT":
                    loop_start=False
                else:
                    loop_start=True
                    messages.append(message)
                    msgNum+=1
                    while loop_start:
                        if msgNum<self.messageCount:
                            message = self.ser.readline()
                            message=message.decode("utf-8")
                            messages.append(message)
                            msgNum+=1
                        else:
                            break
        return messages
        
    def getRMCData(self, messages=None):
        message = []
        if self.RMC==0:
            print("RMC Messages are not enabled, please enable it and try again")
            return None 
        if messages is not None:
            message = messages
        else:
            message = self.getMessage()
        for msg in message:
            RMC = msg
            if(RMC.strip().split(','))[0][3:]=="RMC":
                data=(RMC.strip().split(','))
                RMC_Data = {
                "Suffix":data[0][1:3],
                "Time":data[1],
                "Status":data[2],
                "Latitude":data[3],
                "Hemisphere_Lat":data[4],
                "Longitude":data[5],
                "Hemisphere_Lon":data[6],
                "Speed_Knots":data[7],
                "Heading_Degrees":data[8],
                "Date":data[9],
                "Magnetic_Var_Deg":data[10],
                "Magnetic_Var_EW":data[11],
                "PosMode":data[12][:1],
                "Checksum":data[12][2:]
                }
        return RMC_Data
    
    def getVTGData(self, messages=None):
        if self.VTG==0:
            print("VTG messages are not enabled, please enable it and try again")
            return None
        message = []
        if messages is not None:
            message = messages
        else:
            message = self.getMessage()
        for msg in message:
            VTG = msg
            if(VTG.strip().split(','))[0][3:]=="VTG":
                data=(VTG.strip().split(','))
                VTG_Data = {
                "Suffix":data[0][1:3],
                "Course_1":data[1],     #Heading, Degrees
                "Reference_1":data[2],  #True or Magnetic
                "Course_2":data[3],     #Heading, Degrees
                "Reference_2":data[4],  #True or Magnetic
                "Speed_1":data[5],      
                "Speed_1_Units":data[6], #N = Knots
                "Speed_2":data[7],
                "Speed_2_Units":data[8], #K=Kilometers/Hr
                "PosMode":data[9][:1],
                "Checksum":data[9][2:]
                }
        
        return VTG_Data
        
    
    def getGGAData(self, messages=None):
        if self.GGA==0:
            print("GGA messages are not enabled, please enable it and try again")
            return None
        message = []
        if messages is not None:
            message = messages
        else:
            message = self.getMessage()
        for msg in message:
            GGA = msg
            if(GGA.strip().split(','))[0][3:]=="GGA":
                data=(GGA.strip().split(','))
                GGA_Data = {
                "Suffix":data[0][1:3],
                "Time":data[1],
                "Latitude":data[2],
                "Hemisphere_Lat":data[3],
                "Longitude":data[4],
                "Hemisphere_Lon":data[5],
                "Position_Fix_Ind":data[6],
                "Satellites_Used":data[7], #0-12
                "HDOP":data[8],            #Horizontal Dilution of Precision
                "MSL_Altitude":data[9],
                "MSL_Units":data[10],
                "Geoid_Separation":data[11],
                "Geo_Sep_Units":data[12],
                "AgeOfDiffCorr":data[13],  #Null when DGPS Not Used
                "DiffRefStationID":data[14].split('*')[0], #Null when DGPS Not Used
                "Checksum":data[14].split('*')[1]
                }
        
        return GGA_Data
    
    def getGSAData(self, messages=None):
        if self.GSA==0:
            print("GSA messages are not enabled, please enable it and try again")
            return None
        message = []
        if messages is not None:
            message = messages
        else:
            message = self.getMessage()
        for msg in message:
            GSA = msg
            if(GSA.strip().split(','))[0][3:]=="GSA":
                data=(GSA.strip().split(','))
                GSA_Data = {
                "Suffix":data[0][1:3],
                "OpMode":data[1],        #A = 2D Automatic, M= Manual - forced
                "NavMode":data[2],       #1. Fix Not available, 2. 2D <4 Sat 3. 3D >3 Sat
                "SatUsedCh1":data[3],     #Sattelite used for Channel 1
                "SatUsedCh2":data[4],     #Sattelite used for Channel 2
                "SatUsedCh3":data[5],     #Sattelite used for Channel 3
                "SatUsedCh4":data[6],     #Sattelite used for Channel 4
                "SatUsedCh5":data[7],     #Sattelite used for Channel 5
                "SatUsedCh6":data[8],     #Sattelite used for Channel 6
                "SatUsedCh7":data[9],     #Sattelite used for Channel 7
                "SatUsedCh8":data[10],    #Sattelite used for Channel 8
                "SatUsedCh9":data[11],    #Sattelite used for Channel 9
                "SatUsedCh10":data[12],   #Sattelite used for Channel 10
                "SatUsedCh11":data[13],   #Sattelite used for Channel 11
                "SatUsedCh12":data[14],   #Sattelite used for Channel 12
                "PDOP":data[15],          #Position Dilution of Precision
                "HDOP":data[16],          #Horizontal Dilution of Precision
                "VDOP":data[17].split('*')[0],          #Vertical Dilution of Precision
                "Checksum":data[17].split('*')[1]      #Checksum
                }
        
        return GSA_Data
    
    
    def getGLLData(self, messages=None):
        if self.GLL==0:
            print("GLL messages are not enabled, please enable it and try again")
            return None
        message = []
        if messages is not None:
            message = messages
        else:
            message = self.getMessage()
        for msg in message:
            GLL = msg
            if(GLL.strip().split(','))[0][3:]=="GLL":
                data=(GLL.strip().split(','))
                GLL_Data = {
                "Suffix":data[0][1:3],
                "Latitude":data[1],
                "Hemisphere_Lat":data[2],
                "Longitude":data[3],
                "Hemisphere_Lon":data[4],
                "Time":data[5],
                "Status":data[6],
                "PosMode":data[7][:1],
                "Checksum":data[7][2:]
                }
        return GLL_Data
                
    '''
    #FUTURE: If practical use
    def getGSV_Data(self):
        message = []
        message = self.get_message()
        GSVMessQty = len(message)-5
        #print("Number of GSV Messages: {}".format(GSVMessQty))
        for i in range(4,len(message)-1):
            GSV = message[i]               
            if(GSV.strip().split(','))[0][3:]=="GSV":
                data=(GSV.strip().split(','))
                numSats=int(data[3])
                print(numSats)
                numSatsMod=numSats%4
                print(numSatsMod)
                #ADD the Rest Here
    '''
    
    def getAllData(self):
        messages = self.getMessage()
        RMC=self.getRMCData(messages)
        VTG=self.getVTGData(messages)
        GGA=self.getGGAData(messages)
        GSA=self.getGSAData(messages)
        #GLL=self.getGLLData(messages)
        
        return RMC, VTG, GGA, GSA, GLL
        
    #Printing Functions
    
    def printPrefix(self, Suffix):
        if Suffix=="GP":
            print("GPS Global Navigation System")
        if Suffix=="GN":
            print("GNSS Global Navigation System")
        if Suffix=="GL":
            print("GLONASS Global Navigation System")
        if Suffix=="GA":
            print("GALILEO Global Navigation System")
        if Suffix=="BD":
            print("BEIDOU Global Navigation System")
        
    
    def printRMC(self, RMC):
        if self.RMC==0:
            print("RMC messages are not enabled, please enable it and try again")
        else:
            print("-----RMC Data-----")
            self.printPrefix(RMC["Suffix"])
            print("Time: " + RMC["Time"])
            print("Status: "+ RMC["Status"])
            print("Latitude: "+RMC["Latitude"]+" "+RMC["Hemisphere_Lat"])
            print("Longitude: "+RMC["Longitude"]+" "+RMC["Hemisphere_Lon"])
            print("Speed in Knots: "+RMC["Speed_Knots"])
            print("Heading in Degrees: " +RMC["Heading_Degrees"])
            print("Date: "+RMC["Date"])
            print("Magnetic Variation: "+RMC["Magnetic_Var_Deg"]+" "+RMC["Magnetic_Var_EW"])
            print("PosMode: "+RMC["PosMode"])
            print("Checksum: "+RMC["Checksum"]+"\n")
        
    def printVTG(self, VTG):
        if self.VTG==0:
            print("VTG messages are not enabled, please enable it and try again")
        else:
            print("-----VTG Data-----")
            self.printPrefix(VTG["Suffix"])
            print("Course_1: " + VTG["Course_1"])
            print("Reference_1: "+ VTG["Reference_1"])
            print("Course_2: " + VTG["Course_2"])
            print("Reference_2: "+ VTG["Reference_2"])
            print("Speed_1: " + VTG["Speed_1"]+" "+VTG["Speed_1_Units"])
            print("Speed_2: " + VTG["Speed_2"]+" "+VTG["Speed_2_Units"])
            print("PosMode: "+VTG["PosMode"])
            print("Checksum: "+VTG["Checksum"]+"\n")
        
    def printGGA(self, GGA):
        if self.GGA==0:
            print("GGA messages are not enabled, please enable it and try again")
        else:
            print("-----GGA Data-----")
            self.printPrefix(GGA["Suffix"])
            print("Time: " + GGA["Time"])
            print("Latitude: "+GGA["Latitude"]+" "+GGA["Hemisphere_Lat"])
            print("Longitude: "+GGA["Longitude"]+" "+GGA["Hemisphere_Lon"])
            print("Position Fix Indicator: "+GGA["Position_Fix_Ind"])
            print("Satellites Used: "+GGA["Satellites_Used"])
            print("Horizontal Dilution of Precision: " +GGA["HDOP"])
            print("Mean Sea Level Altitude: "+GGA["MSL_Altitude"]+" "+GGA["MSL_Units"])
            print("Geoid Separation: "+GGA["Geoid_Separation"]+" "+GGA["Geo_Sep_Units"])
            print("Age of Differential Correlation: " +GGA["AgeOfDiffCorr"])
            print("Differential Reference Station ID: "+GGA["DiffRefStationID"])
            print("Checksum: "+GGA["Checksum"]+"\n")
        
    def printGSA(self, GSA):
        if self.GSA==0:
            print("GSA messages are not enabled, please enable it and try again")
        else:
            print("-----GSA Data-----")
            self.printPrefix(GSA["Suffix"])
            print("Operational Mode: " + GSA["OpMode"])
            print("Navigational Mode: " + GSA["NavMode"])
            print("Satellite Used Ch1: "+GSA["SatUsedCh1"])
            print("Satellite Used Ch2: "+GSA["SatUsedCh2"])
            print("Satellite Used Ch3: "+GSA["SatUsedCh3"])
            print("Satellite Used Ch4: "+GSA["SatUsedCh4"])
            print("Satellite Used Ch5: "+GSA["SatUsedCh5"])
            print("Satellite Used Ch6: "+GSA["SatUsedCh6"])
            print("Satellite Used Ch7: "+GSA["SatUsedCh7"])
            print("Satellite Used Ch8: "+GSA["SatUsedCh8"])
            print("Satellite Used Ch9: "+GSA["SatUsedCh9"])
            print("Satellite Used Ch10: "+GSA["SatUsedCh10"])
            print("Satellite Used Ch11: "+GSA["SatUsedCh11"])
            print("Satellite Used Ch12: "+GSA["SatUsedCh12"])
            print("Position Dilution of Precision: "+GSA["PDOP"])
            print("Vertical Dilution of Precision: "+GSA["VDOP"])
            print("Horizontal Dilution of Precision: "+GSA["HDOP"])
            print("Checksum: "+GSA["Checksum"]+"\n")
        
    def printGLL(self, GLL):
        if ((GLL==None) or (self.GLL==0)):
            print("No Data or GLL not enabled")
        else:
            print("-----GLL Data-----")
            self.printPrefix(GLL["Suffix"])
            print("Status: "+ GLL["Status"])
            print("Latitude: "+GLL["Latitude"]+" "+GLL["Hemisphere_Lat"])
            print("Longitude: "+GLL["Longitude"]+" "+GLL["Hemisphere_Lon"])
            print("Time: " + GLL["Time"])
            print("PosMode: "+GLL["PosMode"])
            print("Checksum: "+GLL["Checksum"]+"\n")
        
    def createBaudRatePacket(self,baudrate):
        baudrate = str(baudrate)
        packet="PMTK251"+","+baudrate
        check=self.checksum(packet)[2:]
        if len(check)==1:
            check="0"+check
        output="$"+packet+"*"+check+"\r\n"
        output=output.upper()
        output=str.encode(output)
        return output
    
    def createTestPacket(self):
        packet="PMTK000"
        check=checksum(packet)[2:]
        if len(check)==1:
            check="0"+check
        output="$"+packet+"*"+check+"\r\n"
        output=output.upper()
        output=str.encode(output)
        return output

    def UpdateNMEAOutputMessage(self,Default=False):
        if Default:
            packet="PMTK314,-1"
            self.GLL=0
            self.RMC=1
            self.VTG=1
            self.GGA=1
            self.GSA=1
            self.GSV=1
            self.GST=0
            self.GRS=0
            self.ZDA=0
            self.MCHN=0
            self.DTM=0
        else:
            packet="PMTK314"+","+str(self.GLL)+","+str(self.RMC)+","+str(self.VTG)+","+str(self.GGA)+","+str(self.GSA)+","+str(self.GSV)+","+str(self.GRS)+","+str(self.GST)+",0,0,0,0,0,0,0,0,0,"+str(self.ZDA)+","+str(self.MCHN)+","+str(self.DTM)
        check=self.checksum(packet)[2:]
        if len(check)==1:
            check="0"+check
        output="$"+packet+"*"+check+"\r\n"
        output=output.upper()
        output=str.encode(output)
        self.sendPacket(output)
        self.awaitResponse(20)
        self.getNumMessages()
        


    def checksum(self,packet):
        checksum = 0
        for el in packet:
            checksum ^= ord(el)
        return hex(checksum)
    
    def sendPacket(self,packet):
        self.ser.flush()
        self.ser.write(packet)
        self.ser.flush()
        print("Sent output, awaiting response...")

    def awaitResponse(self,i):
        x=0
        responded = False
        #ser.flushInput()
        while x<i:
            response=self.ser.readline()
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
 
    def grabAndPrintData(self,num):
        x=0
        #self.ser.flushInput()
        while x < num:
            response=self.ser.readline()
            if len(response)>1:
                response=response.decode()
                if len(response)>1:
                    #print(response)
                    if response.strip().split(',')[0][0]=="$":
                        print(response)
            x+=1
            
    def changeBaudRate(self,baudrate):
        self.baud=baudrate
        baudRatePacket=self.createBaudRatePacket(self.baud)
        self.sendPacket(baudRatePacket)
        self.ser.baudrate=self.baud
