import json
import hmac
import base64
from config import *
from urllib import parse
from hashlib import sha256
from datetime import datetime


class Sign:
    
    def __get_param(self):
        return {
            "AccessKeyId": api_code["access"],
            "SignatureMethod": "HmacSHA256",
            "SignatureVersion": "2",
            "Timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        }
    
    def __param_to_str(self, d_param: dict):
        s_param = f"{self.request_method}\n{self.host}\n{self.url}\n"
        for k in d_param:
            if k == "Timestamp":
                s_param += f"{k}={self.__url_encode(d_param[k])}&"
            else:
                s_param += f"{k}={d_param[k]}&"
        return s_param[:-1]
    
    def __url_encode(self, s: str):
        s = s.encode("utf-8")
        return parse.quote(s)

    def __get_sign(self, s_param: str):
        secret = api_code['secret'].encode("utf-8")
        s_param = s_param.encode("utf-8")
        signature = base64.b64encode(hmac.new(secret, s_param, digestmod=sha256).digest())
        return signature.decode('utf-8')

    def param(self):
        d_param = self.__get_param()
        s_param = self.__param_to_str(d_param)
        signature = self.__get_sign(s_param)
        d_param["Signature"] = signature
        return d_param



if __name__ == "__main__":
    Sign()
