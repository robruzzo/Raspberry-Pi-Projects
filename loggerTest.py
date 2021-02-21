from GPSLogger import GPSLogger
import time

logger = GPSLogger(message="VTG")
logger.start()

time.sleep(10)

logger.join()