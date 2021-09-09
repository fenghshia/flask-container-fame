from huobi.database import *


# 此表用于记录接口异常的详细信息
class HuobiApiExceptionDetailLog(Model):
    __bind_key__ = "huobi"
    # 定义字段
    id = Column(Integer, primary_key=True, autoincrement=True)  # 编号自动生成
    url = Column(String(100))  # 异常的api地址
    date = Column(DateTime)  # 记录异常发生的原因
    exptype = Column(String(100))  # 记录异常类型
    data = Column(String(1000))  # 记录异常数据
    notify = Column(Boolean)  # 是否已经通知

    def __repr__(self) -> str:
        return '<HuobiApiExceptionDetailLog %r>' % self.exptype


# 此表用于记录已有异常的api
class HuobiApiExceptionLog(Model):
    __bind_key__ = "huobi"
    # 定义字段
    url = Column(String(100), primary_key=True)

    def __repr__(self) -> str:
        return '<HuobiApiExceptionLog %r>' % self.url
