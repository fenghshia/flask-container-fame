from time import time
from copy import deepcopy
from setup import db
from setup import scheduler
from datetime import datetime
from huobi.util.ema import Ema
from huobi.api.market import Market
from huobi.util.params import Params
from huobi.api.position import Position as PositionApi
from huobi.util.position import *
from huobi.database.position import Position as PositionDatabase


# 策略
@scheduler.task(trigger="date", run_date=datetime.now(), id='eth strategy')
def run_eth_strategy():
    contract = "ETH-USDT"
    market = Market()
    params = Params()
    ema = Ema()
    s = time()
    while True:
        if time() - s > 0.1:
            s = time()
            # 获取市场数据
            market_data = market.kline(contract)
            if market_data == 400:
                continue
            # 同步市场时间
            params.market_date = datetime.fromtimestamp(market_data["ts"]/1000)
            # 最后两k线价格
            last_price = market_data["data"][-2]["close"]
            now_price = market_data["data"][-1]["close"]
            # 指标计算
            emas = ema.triple_ema(last_price, now_price)


# 全仓仓位获取
@scheduler.task(trigger="interval", seconds=1, id='cross position')
def run_cross():
    params = Params()
    pos = PositionApi().cross()
    if pos == 400:
        return
    sync_cross_position(pos, params)


# 逐仓仓位获取
@scheduler.task(trigger="interval", seconds=1, id='swap position')
def run_swap():
    params = Params()
    pos = PositionApi().swap()
    if pos == 400:
        return
    sync_swap_position(pos, params)


# 仓位写入数据库
@scheduler.task(trigger="interval", minutes=1, id='position to local')
def run_write_position():
    params = Params()
    # 全仓处理
    interface = deepcopy(params.cross_position)
    local_poss = PositionDatabase.query.filter(PositionDatabase.mode == "cross").all()
    if local_poss:
        for local_pos in local_poss:
            # 更新数据
            if local_pos.code in interface:
                PositionDatabase.query.filter(PositionDatabase.mode == "cross", PositionDatabase.code == local_pos.code).update(
                    {"volume": interface[local_pos.code]["volume"],
                     "hight_rate": interface[local_pos.code]["hight_rate"],
                     "direction": interface[local_pos.code]["direction"]})
                interface.pop(local_pos.code)
            # 删除数据
            else:
                db.session.delete(local_pos)
    # 新增数据
    for code in interface:
        db.session.add(PositionDatabase(
            mode = "cross",
            code = code,
            volume = interface[code]["volume"],
            hight_rate = interface[code]["hight_rate"],
            direction = interface[code]["direction"]))
    # 逐仓处理
    interface = deepcopy(params.swap_position)
    local_poss = PositionDatabase.query.filter(PositionDatabase.mode == "swap").all()
    if local_poss:
        for local_pos in local_poss:
            # 更新数据
            if local_pos.code in interface:
                PositionDatabase.query.filter(PositionDatabase.mode == "swap", PositionDatabase.code == local_pos.code).update(
                    {"volume": interface[local_pos.code]["volume"],
                     "hight_rate": interface[local_pos.code]["hight_rate"],
                     "direction": interface[local_pos.code]["direction"]})
                interface.pop(local_pos.code)
            # 删除数据
            else:
                db.session.delete(local_pos)
    # 新增数据
    for code in interface:
        db.session.add(PositionDatabase(
            mode = "swap",
            code = code,
            volume = interface[code]["volume"],
            hight_rate = interface[code]["hight_rate"],
            direction = interface[code]["direction"]))
    db.session.commit()

