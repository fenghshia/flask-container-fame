import setup
from huobi import *
from datetime import datetime


if __name__ == "__main__":
    Ema().revers_supplement(
        datetime(2021, 9, 10, 4),
        "3479.17",
        "3439.91",
        "3465.04"
    )
    setup.app.run(
        # host = "0.0.0.0",
        # host = "192.168.100.214",
        # host = "192.168.1.110",
        host = "10.146.0.2",
        port = 9000,
        debug = False
    )
