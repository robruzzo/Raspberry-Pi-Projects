
import serial
from time import sleep

'''
Port - Set depending on how your raspberry pi is configured and what generation it is:
1: /dev/ttyAMA0
2: /dev/ttyS0

Baud: typically 9600

Output - NMEA 0183 V2.3 Sentences:
RMC - Recommended minimum data for GPS
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

class PAM_7Q_Interface:
    def __init__(self, port):
        #Define setup parameters
        self.port = port
        self.baud = 9600
        
        #Data Variables
        self.byte=''           #Byte to determine if sentences are being transmitted

        if self.port =='1':
            self.ser = serial.Serial("/dev/ttyAMA0",self.baud)
        if self.port =='2':
            self.ser = serial.Serial("/dev/ttyS0",self.baud)
        else:
            print("Port Must Be 1, or 2, see class definition for details")
            print("Port: "+self.port)
    
    def getMessage(self):
        loop_start = False
        messages = []
        while self.byte !='$':
            self.byte= self.ser.read()
        while loop_start==False:
            message= self.ser.readline()
            if (message.strip().split(','))[0]=="$GPRMC":
                loop_start=True
                messages.append(message)
                while loop_start:
                    message = self.ser.readline()
                    if (message.strip().split(','))[0]=="$GPRMC":
                        break
                    else:
                        messages.append(message)
                    
        return messages
        
    def getRMCData(self, messages=None):
        message = []
        if messages is not None:
            message = messages
        else:
            message = self.getMessage()
        RMC = message[0]
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
        message = []
        if messages is not None:
            message = messages
        else:
            message = self.getMessage()
        VTG = message[1]
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
        message = []
        if messages is not None:
            message = messages
        else:
            message = self.getMessage()
        GGA = message[2]
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
        message = []
        if messages is not None:
            message = messages
        else:
            message = self.getMessage()
        GSA = message[3]
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
        
        message = []
        if messages is not None:
            message = messages
        else:
            message = self.getMessage()
        GLL = message[len(message)-1]
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
    '''
    
    def getAllData(self):
        messages = self.getMessage()
        RMC=self.getRMCData(messages)
        VTG=self.getVTGData(messages)
        GGA=self.getGGAData(messages)
        GSA=self.getGSAData(messages)
        GLL=self.getGLLData(messages)
        
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
        self.printPrefix(GLL["Suffix"])
        print("Status: "+ GLL["Status"])
        print("Latitude: "+GLL["Latitude"]+" "+GLL["Hemisphere_Lat"])
        print("Longitude: "+GLL["Longitude"]+" "+GLL["Hemisphere_Lon"])
        print("Time: " + GLL["Time"])
        print("PosMode: "+GLL["PosMode"])
        print("Checksum: "+GLL["Checksum"]+"\n")
        
        