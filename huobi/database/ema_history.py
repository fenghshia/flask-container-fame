from huobi.database import *


class EmaHistory(Model):
    __bind_key__ = "huobi"
    # 定义字段
    date = Column(DateTime, primary_key=True)  # 日期检索
    ema1 = Column(DECIMAL(10, 2))  # ema1指标
    ema2 = Column(DECIMAL(10, 2))  # ema2指标
    ema3 = Column(DECIMAL(10, 2))  # ema3指标
    dema = Column(DECIMAL(10, 2))  # 二重ema指标
    tema = Column(DECIMAL(10, 2))  # 三重ema指标
    price = Column(DECIMAL(10, 2))  # 计算用的价格
    correct = Column(Boolean)  # 是否修正

    def __repr__(self) -> str:
        return '<EmaHistory %r>' % self.date
