# encoding:utf-8

import datetime
import hashlib

from Transaction import Transaction


class Record:  # 交易记录类
    def __init__(self, data):  # 初始化
        self.hash = None  # 自身的哈希
        self.prev_hash = None  # 上一个信息记录的哈希
        self.timestamp = datetime.datetime.now()  # 交易时间
        self.data = data  # 交易信息
        self.payload_hash = self._hash_payload()  # 交易后的哈希

    def _hash_payload(self):  # 对于交易时间与交易数据进行哈希计算
        return hashlib.sha256((str(self.timestamp) + str(self.data)).encode("utf-8")).hexdigest()  # 取得数据的哈希

    def _hash_record(self):  # 对于交易进行锁定
        return hashlib.sha256((str(self.prev_hash) + str(self.payload_hash)).encode("utf-8")).hexdigest()  # 取得数据的哈希

    def seal(self):  # 密封
        self.hash = self._hash_record()  # 对应数据锁定，对于交易前的链锁定

    def validate(self):  # 验证数据是否被修改
        if self.payload_hash != self._hash_payload():  # 判断是否有人修改
            raise InvalidRecord("交易数据与时间被修改" + str(self))
        if self.hash != self._hash_record():  # 判断消息链
            raise InvalidRecord("交易的哈希链接被修改" + str(self))
        return "数据正常" + str(self)

    def __repr__(self):  # 返回对象的基本信息
        mystr = "hash:{} ,prev_hash:{},data:{}".format(self.hash, self.prev_hash, self.data)
        return mystr

    def link(self, Record):
        self.prev_hash = Record.hash  # 链接


class InvalidRecord(Exception):  # 异常类型
    def __init__(self, *args, **kwargs):  # 参数
        Exception.__init__(self, *args, **kwargs)


if __name__ == "__main__":  # 单独模块测试
    try:
        t1 = Transaction("yincheng", "donghainimei", 0.000001)
        t2 = Transaction("yincheng", "donghainijie", 0.000002)
        t3 = Transaction("yincheng", "donghainige", 0.000003)
        t4 = Transaction("yincheng", "donghainidi", 0.000004)

        m1 = Record(t1)
        m2 = Record(t2)
        m3 = Record(t3)  # 交易记录
        m4 = Record(t4)  # 交易记录
        m1.seal()
        m2.link(m1)  # 链接
        m2.seal()
        m3.link(m2)  # 链接
        m3.seal()  # 交易记录密封
        m4.link(m3)  # 链接
        m4.seal()  # 交易记录密封

        # 修改数据,模拟纂改
        m2.data = "update data "
        m2.prev_hash = "update data"

        print(m1)
        print(m2)
        print(m3)  # 显示信息
        print(m4)  # 显示信息
        m1.validate()
        m2.validate()
        m3.validate()  # 校验
        m4.validate()
    except InvalidRecord as e:
        print(e)
