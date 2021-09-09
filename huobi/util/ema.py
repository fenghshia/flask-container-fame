from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta
from threading import Lock
from setup import db
from huobi import EmaHistory


class Ema:

    _instance_lock = Lock()
    init_flag = False

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with cls._instance_lock:
                cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        if not self.init_flag:
            # 平滑参数
            self.α = Decimal('0.2')
            # ema取值精度, 小数点后2位
            self.precision = Decimal("0.00")
            self.init_flag = True

    # ema算法
    def __ema(self, price, last_ema):
        # 四舍五入算法
        return (self.α * price + (Decimal("1.0") - self.α) * last_ema).quantize(self.precision, ROUND_HALF_UP)
    
    # dema算法
    def __dema(self, ema1, ema2):
        return (Decimal("2.0") * ema1 - ema2).quantize(self.precision, ROUND_HALF_UP)
    
    # tema算法
    def __tema(self, ema1, ema2, ema3):
        return (Decimal("3.0") * (ema1 - ema2) + ema3).quantize(self.precision, ROUND_HALF_UP)

    # 反转ema2算法
    def __revers_dema(self, ema, dema):
        return (Decimal("2.0") * Decimal(ema) - Decimal(dema)).quantize(self.precision, ROUND_HALF_UP)

    # 反转ema3算法
    def __revers_tema(self, ema1, ema2, tema):
        return (Decimal(tema) - Decimal("3.0") * (Decimal(ema1) - Decimal(ema2))).quantize(self.precision, ROUND_HALF_UP)

    # 三重ema算法
    def triple_ema(self, last_price, now_price, now):
        '''
        param: price为列表, 其中存放两个参数, 第一个是前一小时的收盘价格, 第二个是当前的实时价格
        '''
        # 当前时间的前一个小时
        last_time = self.__round_hour(now + timedelta(hours = -1))
        last_ema = EmaHistory.query.filter(EmaHistory.date == last_time).all()
        # 空数据补充
        if not last_ema:
            self.__replenish(last_time, last_price)
            last_ema = EmaHistory.query.filter(EmaHistory.date == last_time).all()[0]
        else:
            last_ema = last_ema[0]
        # 当前指标计算
        now_ema1 = self.__ema(Decimal(now_price), last_ema.ema1)
        now_ema2 = self.__ema(now_ema1, last_ema.ema2)
        now_ema3 = self.__ema(now_ema2, last_ema.ema3)
        # 未来一小时ema指标
        pre_ema1 = self.__ema(Decimal(now_price), now_ema1)
        pre_ema2 = self.__ema(now_ema1, now_ema2)
        pre_ema3 = self.__ema(now_ema2, now_ema3)
        return {
            "last": {"ema": last_ema.ema1,
                     "tema": last_ema.tema},
            "now": {"ema": now_ema1,
                    "tema": self.__tema(now_ema1, now_ema2, now_ema3)},
            "pre": {"ema": pre_ema1,
                    "tema": self.__tema(pre_ema1, pre_ema2, pre_ema3)}
        }
    
    # 上一个小事数据补齐
    def __replenish(self, time: datetime, price: str):
        '''
        传入: time-补齐时间, price-补齐价格
        写入数据库: date, ema1, ema2, ema3, dema, tema, price, correct
        '''
        # 查询补齐时间的前一条数据
        last_time = time + timedelta(hours=-1)
        last_ema = EmaHistory.query.filter(EmaHistory.date == last_time).all()[0]
        # db.session.close()
        # 前两小事ema1算出前一小时ema1
        ema1 = self.__ema(Decimal(price), last_ema.ema1)
        # 前两小事ema2算出前一小时ema2
        ema2 = self.__ema(ema1, last_ema.ema2)
        # 前两小事ema3算出前一小时ema3
        ema3 = self.__ema(ema2, last_ema.ema3)
        # 算出前一小时dema
        dema = self.__dema(ema1, ema2)
        # 算出前一小时tema
        tema = self.__tema(ema1, ema2, ema3)
        db.session.add(EmaHistory(date=time, ema1=ema1, ema2=ema2, ema3=ema3, dema=dema, tema=tema, price=price, correct=False))
        db.session.commit()
        # db.session.close()

    # 外部数据矫正
    def revers_supplement(self, date: datetime, ema1: str, dema: str, tema: str):
        '''
        传入: date, ema1, dema, tema
        写入数据库: date, ema1, ema2, ema3, dema, tema, correct
        '''
        date = self.__round_hour(date)
        # 补算数据
        ema2 = self.__revers_dema(ema1, dema)
        ema3 = self.__revers_tema(ema1, ema2, tema)
        # 查询是否有数据
        res = EmaHistory.query.filter(EmaHistory.date == date).all()
        # db.session.close()
        if res:
            EmaHistory.query.filter(EmaHistory.date == date).update(
                {"ema1": ema1, "ema2": ema2, "ema3": ema3, "dema": dema, "tema": tema, "correct": True}
            )
        # 新增数据
        else:
            db.session.add(EmaHistory(date=date, ema1=ema1, ema2=ema2, ema3=ema3, dema=dema, tema=tema, correct=True))
        db.session.commit()
        # db.session.close()

    # 时间取整函数: 精确度(小时)
    def __round_hour(self, time):
        return datetime(time.year, time.month, time.day, time.hour)
