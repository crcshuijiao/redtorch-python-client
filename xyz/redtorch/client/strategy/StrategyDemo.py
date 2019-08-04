import uuid

from xyz.redtorch.client.strategy.StrategyTemplate import StrategyTemplate
from xyz.redtorch.pb.core_enum_pb2 import PriceTypeEnum, DirectionEnum, OffsetEnum


class StrategyDemo(StrategyTemplate):

    def __init__(self, strategyId):
        super().__init__(strategyId)
        self.tickCount = 0
        self.preOrderId = None
        self.preOriginOrderId = None

    def onInit(self):
        self.subscribe("au1912@SHFE@FUTURES", gatewayId="52a91f77-c3a7-42ac-a4fe-7a605b99ff4a")

    def onTick(self, tick):
        print("收到Tick,数据源ID %s" % tick.dataSourceId)

        self.tickCount += 1

        if str(self.tickCount)[-1] == "3":
            originOrderId = str(uuid.uuid4())
            orderId = self.submitOrder("au1912@SHFE@FUTURES", PriceTypeEnum.LIMIT, DirectionEnum.LONG, OffsetEnum.OPEN,
                                       "094948@CNY@52a91f77-c3a7-42ac-a4fe-7a605b99ff4a", tick.upperLimit, 1,
                                       originOrderId=originOrderId)
            print("===========================================originOrderId")
            print(originOrderId)
            print("=================================================orderId")
            print(orderId)

        if str(self.tickCount)[-1] == "5":
            originOrderId = str(uuid.uuid4())
            orderId = self.submitOrder("au1912@SHFE@FUTURES", PriceTypeEnum.LIMIT, DirectionEnum.SHORT,
                                       OffsetEnum.CLOSE_TODAY, "094948@CNY@52a91f77-c3a7-42ac-a4fe-7a605b99ff4a",
                                       tick.lowerLimit, 1, originOrderId=originOrderId)
            print("===========================================originOrderId")
            print(originOrderId)
            print("=================================================orderId")
            print(orderId)

        if str(self.tickCount)[-1] == "7":
            originOrderId = str(uuid.uuid4())
            orderId = self.submitOrder("au1912@SHFE@FUTURES", PriceTypeEnum.LIMIT, DirectionEnum.LONG, OffsetEnum.OPEN,
                                       "094948@CNY@52a91f77-c3a7-42ac-a4fe-7a605b99ff4a", tick.lowerLimit, 1,
                                       originOrderId=originOrderId)
            print("===========================================originOrderId")
            print(originOrderId)
            print("=================================================orderId")
            print(orderId)
            self.preOriginOrderId = originOrderId
            self.preOrderId = orderId

        if str(self.tickCount)[-1] == "9":
            self.cancelOrder(originOrderId=self.preOriginOrderId)

    def onTrade(self, trade):
        print("收到成交信息")
        print(trade)

    def onOrder(self, order):
        print("收到委托信息")
        print(order)
