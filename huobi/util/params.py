# 存放火币量化交易的公共数据
from threading import Lock


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