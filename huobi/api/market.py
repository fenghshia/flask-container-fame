from setup import db
from huobi import HuobiApiExceptionDetailLog
from datetime import datetime
from threading import Lock
from huobi import BaseApi


class Market(BaseApi):

    _instance_lock = Lock()
    init_flag = False

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        if not self.init_flag:
            super().__init__()
            self.sign = False
            self.init_flag = True

    # 获取一小时k线, 数据按照最新到以前的顺序排
    def kline(self, contract_code):
        self.request_method = "GET"
        self.url = "/linear-swap-ex/market/history/kline"
        self.param = {
            "contract_code": contract_code,
            "period": "4hour",
            "size": "25"
        }
        res = self.request()
        if res == 400:
            return res
        else:
            res = res.json()
            try:
                data = res['data']
            except KeyError:
                exp = HuobiApiExceptionDetailLog(
                    url=self.url,
                    date=datetime.fromtimestamp(res["ts"]/1000),  # 记录市场时间
                    exptype="data error",
                    data=str(res),
                    notify=False
                )
                db.session.add(exp)
                db.session.commit()
                return 400
            return res
