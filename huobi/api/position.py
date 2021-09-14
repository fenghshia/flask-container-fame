from setup import db
from datetime import datetime
from threading import Lock
from huobi.api import HuobiApiExceptionDetailLog
from huobi.api.base.base import BaseApi


class Position(BaseApi):

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
            self.sign = True
            self.init_flag = True

    # 逐仓持仓
    def swap(self):
        with self._instance_lock:
            self.request_method = "POST"
            self.url = "/linear-swap-api/v1/swap_position_info"
            self.data = None
            res = self.request()
        if res == 400:
            return res
        else:
            res = res.json()
            return res

    # 全仓持仓
    def cross(self):
        with self._instance_lock:
            self.request_method = "POST"
            self.url = "/linear-swap-api/v1/swap_cross_position_info"
            self.data = None
            res = self.request()
        if res == 400:
            return res
        else:
            res = res.json()
            return res
