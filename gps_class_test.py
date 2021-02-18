from GPS_PAM_7Q import PAM_7Q_Interface
from time import sleep

x=0

#Create an instance of the PAM_7Q_Interface object
gps = PAM_7Q_Interface('2')

#These can be used to test to make sure all the messages are received and printed


RMC=gps.getRMC_Data()
gps.printRMC(RMC)

  
VTG=gps.getVTG_Data()
gps.printVTG(VTG)
   
GGA = gps.getGGA_Data()
gps.printGGA(GGA)

GSA = gps.getGSA_Data()
gps.printGSA(GSA)

GLL=gps.getGLL_Data()
gps.printGLL(GLL)


#This part will grab all of the available messages and dump them all to the screen raw

messages =[]

while x<1:
    messages = gps.get_message()

    for i in range(len(messages)):
        print(messages[i].strip().split(','))
        print("\n")    
    x+=1
   
 
