from flask import Flask
from config import *
from util.email import Email
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from apscheduler.events import EVENT_JOB_ERROR


# 配置信息
class config:
    SCHEDULER_API_ENABLED = True  # 定时任务启用
    SQLALCHEMY_DATABASE_URI = fcf_database  # fcf框架地址
    SQLALCHEMY_BINDS = {
        "huobi": huobi_database  # huobi数据库地址
    }
    SQLALCHEMY_POOL_SIZE = 50  # 数据库连接池大小

def errorlisten(event):
    msg = f"错误类型: {event.exception}\n"
    msg += f"type: {type(event.exception)}\n"
    msg += f"错误信息: {event.traceback}"
    mail.send(msg)
    db.session.rollback()

app = Flask(__name__)
# 配置读取
app.config.from_object(config())
# 邮件
mail = Email()
# 数据库
db = SQLAlchemy(app)
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
    mail.send("testing ...")
    return "success"