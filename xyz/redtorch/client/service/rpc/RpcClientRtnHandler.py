from xyz.redtorch.client.service.ClientTradeCacheService import ClientTradeCacheService
from xyz.redtorch.client.strategy.StrategyEngine import StrategyEngine
import logging as logger


class RpcClientRtnHandler:
    @staticmethod
    def onRpcOrderRtn(rpcOrderRtn):
        ClientTradeCacheService.storeOrder(rpcOrderRtn.order)
        StrategyEngine.onOrder(rpcOrderRtn.order)

    @staticmethod
    def onRpcTradeRtn(rpcTradeRtn):
        ClientTradeCacheService.storeTrade(rpcTradeRtn.trade)
        StrategyEngine.onTrade(rpcTradeRtn.trade)

    @staticmethod
    def onRpcPositionRtn(rpcPositionRtn):
        ClientTradeCacheService.storePosition(rpcPositionRtn.position)

    @staticmethod
    def onRpcAccountRtn(rpcAccountRtn):
        ClientTradeCacheService.storeAccount(rpcAccountRtn.account)

    @staticmethod
    def onRpcContractRtn(rpcContractRtn):
        ClientTradeCacheService.storeContract(rpcContractRtn.contract)

    @staticmethod
    def onRpcTickRtn(rpcTickRtn):
        ClientTradeCacheService.storeTick(rpcTickRtn.tick)
        StrategyEngine.onTick(rpcTickRtn.tick)

    @staticmethod
    def onRpcNoticeRtn(rpcNoticeRtn):
        logger.info("收到通知信息%s", rpcNoticeRtn.notice)
