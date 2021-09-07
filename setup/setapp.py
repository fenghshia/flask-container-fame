from flask import Flask
# from config.config import uri
# from service.email import Email
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from apscheduler.events import EVENT_JOB_ERROR
from config.base import email_code
from flask_mail import Mail, Message


# 配置信息
class config:
    SCHEDULER_API_ENABLED = True  # 定时任务启用
    # SQLALCHEMY_DATABASE_URI = uri  # 数据库地址
    SQLALCHEMY_POOL_SIZE = 50  # 数据库连接池大小

    # 邮件配置
    MAIL_SERVER = "smtp.qq.com"
    MAIL_PORT = 465
    MAIL_USE_TSL = True
    MAIL_USE_SSL = True
    MAIL_USEERNAME = "754587525@qq.com"
    MAIL_PASSWORD = email_code
    MAIL_DEFAULT_SENDER = ("FCF", "754587525@qq.com")

def errorlisten(event):
    msg = f"错误类型: {event.exception}\n"
    msg += f"type: {type(event.exception)}\n"
    msg += f"错误信息: {event.traceback}"
    # Email().send(msg)
    # db.session.rollback()

app = Flask(__name__)
# 配置读取
app.config.from_object(config())
# 邮件
mail = Mail(app)
# 数据库
# db = SQLAlchemy(app)
# 定时任务
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.add_listener(errorlisten, EVENT_JOB_ERROR)
scheduler.start()

# 允许跨域访问
@app.after_request
def after_request(res):
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res

@app.route("/emailtest", methods=["GET"])
def email_test():
    msg = Message(subject="Flask-Container-Frame email test", recipients=["754587525@qq.com"], body='testing')
    mail.send(msg)
    return "success"