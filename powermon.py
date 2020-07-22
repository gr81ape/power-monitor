import psutil
import time

while True:
    batteryStatus = psutil.sensors_battery()
    print(batteryStatus)
    time.sleep(1)