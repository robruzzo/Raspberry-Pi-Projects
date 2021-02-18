from GPS_PAM_7Q import PAM_7Q_Interface
from time import sleep

gps = PAM_7Q_Interface('2')

messages =[]

'''
RMC=gps.getRMC_Data()
gps.printRMC(RMC)
    
VTG=gps.getVTG_Data()
gps.printVTG(VTG)
   
GGA = gps.getGGA_Data()
gps.printGGA(GGA)

GSA = gps.getGSA_Data()
gps.printGSA(GSA)
'''

messages = gps.get_message()

for i in range(len(messages)):
    print(messages[i].strip().split(','))
    print("\n")    

gps.getGSV_Data() 
