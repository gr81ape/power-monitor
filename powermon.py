import argparse
import logging
from logging.handlers import TimedRotatingFileHandler
import psutil
import smtplib
import ssl
import time

class PowerMonitor:
    def __init__(self, account_email, password, recipient_email, mail_server):
        self.account_email = account_email
        self.password = password
        self.recipient_email = recipient_email
        self.mail_server = mail_server
        self.plugged_in = True
        self.logger = logging.getLogger("power-monitor")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.logger.setLevel(logging.INFO)
        handler = TimedRotatingFileHandler("powermon.log", when="midnight", interval=1, backupCount=30)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def set_power_state(self, state):
        if self.plugged_in != state:
            self.plugged_in = state
            if state:
                self.send_alert_email("Power restored.")
            else:
                self.send_alert_email("Power outage detected!")

    def start_power_mon(self):
        while True:
            batteryStatus = psutil.sensors_battery()
            if batteryStatus:
                if batteryStatus.power_plugged:
                    self.logger.info("Power OK")
                    self.set_power_state(True)
                else:
                    self.logger.error("Power unavailable")
                    self.set_power_state(False)
            else:
                self.logger.error("No battery status available")
                self.set_power_state(False)
            time.sleep(5)

    def send_alert_email(self, body):
        self.logger.info("Sending email for status change")
        # Set up the required parameters for the email
        subject = "Power state change at home"
        email_text = """From: %s\nTo: %s\nSubject: %s\n

        %s
        """ % (self.account_email, self.recipient_email, subject, body)

        # Make the SMTP connection and send the email
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        connection = smtplib.SMTP(self.mail_server, 587)
        connection.ehlo()
        connection.starttls(context=context)
        connection.ehlo()
        connection.login(self.account_email, self.password)
        connection.sendmail(self.account_email, self.recipient_email, email_text)
        connection.close()
        self.logger.info("Email sent")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('account_email', metavar='account_email', type=str, help='The account to use for sending emails over SMTP.')
    parser.add_argument('password', metavar='password', type=str, help='The password to use for sending emails.')
    parser.add_argument('recipient_email', metavar='recipient_email', type=str, help='The target recipient e-mail address for power status updates.')
    parser.add_argument('mail_server', metavar='mail_server', type=str, help='Mail server address.')
    args = parser.parse_args()
    powerMonitor = PowerMonitor(args.account_email, args.password, args.recipient_email, args.mail_server)
    powerMonitor.start_power_mon()