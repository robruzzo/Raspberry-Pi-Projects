from GPS_PAM_7Q import PAM_7Q_Interface
from time import sleep

x=0

#Create an instance of the PAM_7Q_Interface object
gps = PAM_7Q_Interface('2')

'''
Comment and uncomment each section to test functions accordingly
'''

#These can be used to test to make sure all the messages are received and printed

'''
RMC=gps.getRMCData()
gps.printRMC(RMC)

  
VTG=gps.getVTGData()
gps.printVTG(VTG)
   
GGA = gps.getGGAData()
gps.printGGA(GGA)

GSA = gps.getGSAData()
gps.printGSA(GSA)

GLL=gps.getGLLData()
gps.printGLL(GLL)
'''

#This part will grab all of the available messages and dump them all to the screen raw
'''
messages =[]

while x<1:
    messages = gps.getMessage()

    for i in range(len(messages)):
        print(messages[i].strip().split(','))
        print("\n")    
    x+=1
'''


#This part will test the getAllData function
RMC, VTG, GGA, GSA, GLL = gps.getAllData()

gps.printRMC(RMC)
gps.printVTG(VTG)
gps.printGGA(GGA)
gps.printGSA(GSA)
gps.printGLL(GLL)


