# encoding:utf-8
import datetime


class Transaction:  # 交易
    def __init__(self,
                 payer,  # 付款方
                 recer,  # 收款方
                 money):  # 数字货币的数字
        self.payer = payer  # 付款方
        self.recer = recer  # 收款方
        self.money = money  # 数字货币的数字
        self.timestamp = datetime.datetime.now()  # 交易时间

    def __repr__(self):
        return str(self.payer) + " pay " + str(self.recer) + " " + str(self.money) + " " + str(self.timestamp)


if __name__ == "__main__":  # 单独模块测试
    t1 = Transaction("yincheng", "donghai", 0.00000000001)  # 交易类，后期需要整合公钥私钥
    print(t1)
