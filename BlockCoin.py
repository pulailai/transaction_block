# encoding:utf-8
from Block import InvalidBlock, Block
from Record import Record
from Transaction import Transaction


class BlockCoin:  # 区块链
    def __init__(self):  # 初始化
        self.blocklist = []  # 装载所有的区块

    def add_block(self, block):  # 增加区块
        if len(self.blocklist) > 0:
            block.prev_hash = self.blocklist[-1].hash  # 区块链的哈希
        block.seal()  # 密封
        block.validate()  # 校验
        self.blocklist.append(block)  # 增加区块

    def validate(self):  # 校验
        for i, block in enumerate(self.blocklist):
            try:
                block.validate()
            except InvalidBlock as e:
                raise InvalidBlockCoin("区块校验错误,区块索引{}".format(i))

    def __repr__(self):  # 字符串格式化
        return "Dada_BlockCoin:{}".format(len(self.blocklist))  # 获取长度


class InvalidBlockCoin(Exception):  # blockcoin异常
    def __init__(self, *arg, **kargs):
        Exception.__init__(self, *arg, **kargs)


if __name__ == "__main__":
    try:
        t1 = Transaction("yincheng", "tanweinimei", 0.000001)
        t2 = Transaction("yincheng", "tanweinijie", 0.000002)
        t3 = Transaction("yincheng", "tanweinige", 0.000003)
        t4 = Transaction("yincheng", "tanweinidi", 0.000004)
        t5 = Transaction("yincheng", "tanweinidie", 0.000005)
        t6 = Transaction("yincheng", "tanweininiang", 0.000006)

        m1 = Record(t1)
        m2 = Record(t2)
        m3 = Record(t3)  # 交易记录
        m4 = Record(t4)  # 交易记录
        m5 = Record(t5)  # 交易记录
        m6 = Record(t6)  # 交易记录

        yin1 = Block(m1, m2)
        yin1.seal()

        yin2 = Block(m3, m4)
        yin2.seal()

        yin3 = Block(m5, m6)
        yin3.seal()

        # 纂改区块
        yin3.messagelist.append(m1)

        mydada = BlockCoin()  # 区块链
        mydada.add_block(yin1)  # 增加区块
        mydada.add_block(yin2)
        mydada.add_block(yin3)
        mydada.validate()  # 校验
        print(mydada)
    except Exception as e:
        print(e)
