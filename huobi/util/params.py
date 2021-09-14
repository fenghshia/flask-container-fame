# 存放火币量化交易的公共数据
from threading import Lock
from huobi.database.position import Position


class Params:

    _instance_lock = Lock()
    init_flag = False

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        if not self.init_flag:
            self.init_flag = True
            # 市场时间
            self.market_date = False
            # 逐仓信息
            self.swap_position = dict()
            swap = Position.query.filter(Position.mode == "swap").all()
            if swap:
                for contract in swap:
                    position = {
                        "volume": contract.volume,  # 张数
                        "hight_rate": contract.hight_rate,  # 最高收益率
                        "direction": contract.direction  # 仓位方向
                    }
                    self.swap_position[contract.code] = position
            # 全仓信息
            self.cross_position = dict()
            cross = Position.query.filter(Position.mode == "cross").all()
            if cross:
                for contract in cross:
                    position = {
                        "volume": contract.volume,  # 张数
                        "hight_rate": contract.hight_rate,  # 最高收益率
                        "direction": contract.direction  # 仓位方向
                    }
                    self.cross_position[contract.code] = position
