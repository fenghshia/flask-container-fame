# 仓位操作
from jsonpath import jsonpath


def sync_cross_position(pos, params):
    # 1. 已有仓位
    # 1.1. 同合约, 持仓张数不变 > 收益率更高 > 更新最高收益率
    # 1.2. 同合约, 持仓张数变化 > 更新张数, 更新最高收益率
    # 2. 没有仓位 > 更新仓位
    # 3. 多余仓位 > 删除仓位
    for contract in pos["data"]:
        # 已有仓位
        if contract["contract_code"] in params.cross_position:
            # 同合约, 持仓张数不变 > 收益率更高 > 更新最高收益率
            if contract["volume"] == params.cross_position[contract["contract_code"]]["volume"] and\
                contract["profit_rate"]*100 > params.cross_position[contract["contract_code"]]["hight_rate"]:
                params.cross_position[contract["contract_code"]]["hight_rate"] = contract["profit_rate"]*100
            # 同合约, 持仓张数增加 > 更新张数, 更新最高收益率
            elif contract["volume"] > params.cross_position[contract["contract_code"]]["volume"]:
                params.cross_position[contract["contract_code"]]["volume"] = contract["volume"]
                params.cross_position[contract["contract_code"]]["hight_rate"] = contract["profit_rate"]*100
        # 没有仓位
        else:
            position = {
                "volume": contract["volume"],  # 张数
                "hight_rate": contract["profit_rate"]*100,  # 最高收益率
                "direction": contract["direction"]  # 仓位方向
            }
            params.cross_position[contract["contract_code"]] = position
        # 删除多余仓位
        interface = jsonpath(pos["data"], "$..contract_code")
        local = params.cross_position.keys()
        for key in set(local).difference(interface):
            params.cross_position.pop(key)


def sync_swap_position(pos, params):
    for contract in pos["data"]:
        # 已有仓位
        if contract["contract_code"] in params.swap_position:
            # 同合约, 持仓张数不变 > 收益率更高 > 更新最高收益率
            if contract["volume"] == params.swap_position[contract["contract_code"]]["volume"] and\
                contract["profit_rate"]*100 > params.swap_position[contract["contract_code"]]["hight_rate"]:
                params.swap_position[contract["contract_code"]]["hight_rate"] = contract["profit_rate"]*100
            # 同合约, 持仓张数增加 > 更新张数, 更新最高收益率
            elif contract["volume"] > params.swap_position[contract["contract_code"]]["volume"]:
                params.swap_position[contract["contract_code"]]["volume"] = contract["volume"]
                params.swap_position[contract["contract_code"]]["hight_rate"] = contract["profit_rate"]*100
        # 没有仓位
        else:
            position = {
                "volume": contract["volume"],  # 张数
                "hight_rate": contract["profit_rate"]*100,  # 最高收益率
                "direction": contract["direction"]  # 仓位方向
            }
            params.swap_position[contract["contract_code"]] = position
        # 删除多余仓位
        interface = jsonpath(pos["data"], "$..contract_code")
        local = params.swap_position.keys()
        for key in set(local).difference(interface):
            params.swap_position.pop(key)

