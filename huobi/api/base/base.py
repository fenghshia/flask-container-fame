
from setup import db
from huobi import Sign
from huobi import HuobiApiExceptionDetailLog
from requests import session
from datetime import datetime
from config.base import proxy
from config.huobi import url_timeout
from urllib3.exceptions import MaxRetryError
from requests.exceptions import Timeout
from requests.exceptions import ConnectionError


class BaseApi(Sign):

    def __init__(self):
        super().__init__()
        self.host = "api.hbdm.com"
        self.session = session()
        # 有无代理判断
        if proxy:
            self.session.proxies = proxy
        

    def request(self):
        # 初始化param
        if self.sign:
            param = self.param()
        else:
            param = self.param
        
        if self.request_method == "GET":
            return self.__get_request(param)
        elif self.request_method == "POST":
            return self.__post_request(param, self.data)

    # 基础post请求
    def __post_request(self, param=None, data=None):
        try:
            return self.session.post(
                url=f"https://{self.host}{self.url}",
                params=param,
                json=data,
                timeout=url_timeout
            )
        except Timeout:
            self.__log("URL Timeout")
        except MaxRetryError:
            self.__log("HTTPS Connection Pool")
        return 400

    # 基础get请求
    def __get_request(self, param=None):
        try:
            return self.session.get(
                url=f"https://{self.host}{self.url}",
                params=param,
                timeout=url_timeout
            )
        except Timeout:
            self.__log("URL Timeout")
        except MaxRetryError:
            self.__log("urllib3: HTTPS Connection Pool")
        except ConnectionError:
            self.__log("requests: HTTPS Connection Pool")
        return 400

    # 日志记录超时异常
    def __log(self, exptype):
        exp = HuobiApiExceptionDetailLog(url=self.url, date=datetime.now(), exptype=exptype, data=None, notify=False)
        db.session.add(exp)
        db.session.commit()
