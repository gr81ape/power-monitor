import psutil
import time
import logging
from logging.handlers import TimedRotatingFileHandler
import smtplib

def start_power_mon():
    logger = logging.getLogger("power-monitor")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    logger.setLevel(logging.INFO)
    handler = TimedRotatingFileHandler("powermon.log", when="midnight", interval=1, backupCount=30)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    while True:
        batteryStatus = psutil.sensors_battery()
        if batteryStatus:
            if batteryStatus.power_plugged:
                logger.info("Power OK")
            else:
                logger.error("Power unavailable")
        else:
            logger.error("No battery status available")
        time.sleep(5)

def send_alert_email():
    print("Not implemented yet")

if __name__ == "__main__":
    start_power_mon()