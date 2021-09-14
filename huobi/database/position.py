from huobi.database import *


class Position(Model):
    __bind_key__ = "huobi"
    # 定义字段
    id = Column(Integer, primary_key=True, autoincrement=True)  # 编号自动生成
    mode = Column(String(10))  # 全仓/逐仓模式
    code = Column(String(10))  # 合约代码
    volume = Column(Float)  # 持仓张数
    hight_rate = Column(Float)  # 最高收益率
    direction = Column(String(10))  # 持仓方向

    def __repr__(self) -> str:
        return '<Position %r>' % self.code
