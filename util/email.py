import smtplib
from threading import Lock
from email.utils import formataddr
from config.base import Config
from config.base import email_code, subtitle
from email.header import Header
from email.mime.text import MIMEText


class Email:

    _instance_lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        configer = Config()
        self.receiver = configer.read("EmailReceiver")

    def send(self, msg, receiver=None):
        if not receiver:
            receiver = self.receiver
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login("754587525@qq.com", email_code)
        msg=MIMEText(msg, 'plain', 'utf-8')
        msg['Subject'] = Header(subtitle, 'utf-8')
        msg['From'] = formataddr(["火币量化交易平台-QuantBit", '754587525@qq.com'])
        msg['To'] = formataddr(["使用者", "754587525@qq.com"])
        server.sendmail('754587525@qq.com', receiver, msg.as_string())
        server.quit()
