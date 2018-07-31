# encoding:utf-8
import datetime  # 时间日期类，
import hashlib  # 信息安全加密解密

from Record import Record, InvalidRecord
from Transaction import Transaction


class Block:
    def __init__(self, *args):  # 初始化
        self.messagelist = []  # 存储多个交易记录
        self.timestamp = None  # 存储多个纪录最终锁定的时间
        self.hash = None  # 当前的哈希散列
        self.prev_hash = None  # 上一块的哈希散列
        if args:
            for arg in args:
                self.add_message(arg)

    def add_message(self, message):  # 增加交易信息
        # 区分第一条与后面多条,是否需要链接
        if len(self.messagelist) > 0:
            message.link(self.messagelist[-1])  # 链接
        message.seal()  # 密封
        message.validate()  # 校验
        self.messagelist.append(message)  # 追加记录

    def link(self, block):  # 区块链链接
        self.prev_hash = block.hash

    def seal(self):  # 密封
        self.timestamp = datetime.datetime.now()  # 密封确定当前时间
        self.hash = self._hash_block()  # 密封当前的哈希值

    def _hash_block(self):  # 密封 上一块哈希，时间线，交易记录的最后一个
        return hashlib.sha256((str(self.prev_hash) + \
                               str(self.timestamp) + \
                               str(self.messagelist[-1].hash)).encode("utf-8")).hexdigest()

    def validate(self):  # 校验
        for i, message in enumerate(self.messagelist):  # 每个交易记录校验一下
            message.validate()  # 每一条校验一下
            if i > 0 and message.prev_hash != self.messagelist[i - 1].hash:
                raise InvalidBlock(("无效block,交易记录被修改为在第{}条记录".format(i) + str(self)))

    def __repr__(self):  # 类的对象描述
        return "money block= hash:{},prehash:{},len:{},time:{}". \
            format(self.hash, self.prev_hash, len(self.messagelist), self.timestamp)


class InvalidBlock(Exception):  # block异常
    def __init__(self, *arg, **kargs):
        Exception.__init__(self, *arg, **kargs)


if __name__ == "__main__":
    try:
        t1 = Transaction("yincheng", "tanweinimei", 0.000001)
        t2 = Transaction("yincheng", "tanweinijie", 0.000002)
        t3 = Transaction("yincheng", "tanweinige", 0.000003)
        t4 = Transaction("yincheng", "tanweinidi", 0.000004)

        m1 = Record(t1)
        m2 = Record(t2)
        m3 = Record(t3)  # 交易记录
        m4 = Record(t4)  # 交易记录

        yin = Block(m1, m2, m3)  # 一口气加入4条记录
        yin.seal()  # 密封

        # m3.data="update" #直接秀应该messgae
        yin.messagelist[2] = m1

        print(yin.validate())
        print(yin)
    except InvalidRecord as e:  # 消息被修改
        print(e)
    except  InvalidBlock as e:  # 区块被修改
        print(e)
