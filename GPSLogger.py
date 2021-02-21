#from GPS_PAM_7Q import PAM_7Q_Interface
from GPS_PAM_7Q_P3 import PAM_7Q_Interface
import os
import threading

class GPSLogger(threading.Thread):
    def __init__(self, filename="GPS_LOG_", message="RMC",interface='2'):
        threading.Thread.__init__(self,target=self.logData)
        self.filename=filename
        self.message=message
        self.interface = interface
        self.logging=False
        #self.gps = PAM_7Q_Interface(self.interface)
        self.gps = PAM_7Q_Interface(self.interface)
        self.messagePosition ={"RMC":0, "VTG":1, "GGA":2, "GSA":3, "GLL":-1}
        
        i=0
        while os.path.exists(self.filename+"%s.txt" % i):
            i+=1
        self.gpsFile = open(self.filename+"%s.txt" % i, "w")
           
    def logData(self):
        self.logging=True
        messageNum = self.messagePosition[self.message]
        while self.logging:
            messages=self.gps.getMessage()
            if messageNum==-1:
                self.gpsFile.write(messages[len(messages)-1])
                print("Added Point")
            else:
                self.gpsFile.write(messages[messageNum])
                print("Added Point")
        print("Closing File")
        self.gpsFile.close()
        
    def join(self):
        self.logging=False
        threading.Thread.join(self)
        
        
        
            
            
            
        

