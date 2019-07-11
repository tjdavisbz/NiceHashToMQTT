from forex_python.bitcoin import BtcConverter


class NicehashData:
    hashratesuffix = float(0)
    balance = float(0)
    balanceUSD = float(0)

    def __init__(self, name, hashrate, hashratesuffix, balance):
        b = BtcConverter()
        self.name = name
        self.hashrate = hashrate
        self.hashratesuffix = hashratesuffix
        self.balance = balance
        self.balanceUSD = b.get_latest_price('USD') * float(self.balance)


class NicehashDataList:
    nicehashdatalist = []

    def __init__(self, nicehashdatalist):
        self.nicehashdatalist = nicehashdatalist

    def append(self,nicehashdata):
        self.nicehashdatalist.append(nicehashdata)

    def clear(self):
        self.nicehashdatalist = []

    def hashratetotal(self):
        hashratetotal = 0.00
        for nicehashdata in self.nicehashdatalist:
            hashrate = float(nicehashdata.hashrate)
            if nicehashdata.hashratesuffix == "kH":
                hashrate = hashrate / 1000
            elif nicehashdata.hashratesuffix == "GH":
                hashrate = hashrate * 1000
            elif nicehashdata.hashratesuffix == "GH":
                hashrate = hashrate * 1000000
            elif nicehashdata.hashratesuffix == "sol":
                hashrate = hashrate / 1000000
            hashratetotal = hashratetotal + float(hashrate)
        return hashratetotal

    def balancetotal(self):
        balancetotal = 0.00
        for nicehashdata in self.nicehashdatalist:
            balancetotal = balancetotal + float(nicehashdata.balance)
        return balancetotal

    def balanceusdtotal(self):
        balanceusdtotal = 0.00
        for nicehashdata in self.nicehashdatalist:
            balanceusdtotal = balanceusdtotal + float(nicehashdata.balanceUSD)
        return balanceusdtotal
