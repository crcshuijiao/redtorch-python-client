import uuid
import logging as logger
from xyz.redtorch.client.Config import Config
import time

from xyz.redtorch.client.service.rpc.RpcClientProcessService import RpcClientProcessService
from xyz.redtorch.client.service.rpc.RpcClientRspHandler import RpcClientRspHandler
from xyz.redtorch.pb.core_enum_pb2 import CommonStatusEnum
from xyz.redtorch.pb.core_field_pb2 import CommonReqField, CancelOrderReqField
from xyz.redtorch.pb.core_rpc_pb2 import RpcId, RpcSubscribeReq, RpcUnsubscribeReq, RpcSubmitOrderReq, \
    RpcCancelOrderReq, RpcSearchContractReq, RpcGetAccountListReq, RpcGetMixContractListReq, RpcGetPositionListReq, \
    RpcGetOrderListReq, RpcGetTradeListReq, RpcGetTickListReq


class RpcClientApiService:
    @staticmethod
    def subscribe(contract, gatewayId=None, reqId=None, sync=False):
        if not reqId:
            reqId = str(uuid.uuid4())
        operatorId = Config.operatorId
        sourceNodeId = Config.nodeId

        commonReq = CommonReqField()
        commonReq.sourceNodeId = sourceNodeId
        commonReq.targetNodeId = 0
        commonReq.operatorId = operatorId
        commonReq.reqId = reqId

        rpcSubscribeReq = RpcSubscribeReq()

        rpcSubscribeReq.commonReq.CopyFrom(commonReq)
        rpcSubscribeReq.contract.CopyFrom(contract)

        if gatewayId:
            rpcSubscribeReq.gatewayId = gatewayId

        if sync:
            RpcClientRspHandler.registerWaitReqId(reqId)

        sendResult = RpcClientProcessService.sendRoutineCoreRpc(0, rpcSubscribeReq.SerializeToString(), reqId,
                                                                RpcId.SUBSCRIBE_REQ)

        if sync and not sendResult:
            RpcClientRspHandler.unregisterWaitReqId(reqId)
            return False

        if sync:
            startTime = time.time()
            while True:
                if time.time() - startTime < Config.rpcTimeOut:
                    rpcSubscribeRsp = RpcClientRspHandler.getAndRemoveRpcSubscribeRsp(reqId)
                    if not rpcSubscribeRsp:
                        rpcExceptionRsp = RpcClientRspHandler.getAndRemoveRpcExceptionRsp(reqId);
                        if rpcExceptionRsp:
                            logger.error("订阅错误,请求ID: %s, 远程错误回报 %s", reqId, rpcExceptionRsp.info)
                            return False
                        time.sleep(0.02)
                    else:
                        commonRsp = rpcSubscribeRsp.commonRsp
                        requestStatus = commonRsp.requestStatus
                        if requestStatus == CommonStatusEnum.SUCCESS:
                            return True
                        elif requestStatus == CommonStatusEnum.INFO:
                            logger.info("订阅错误,请求ID:%s,远程信息回报:%s", reqId, commonRsp.info)
                            return True
                        elif requestStatus == CommonStatusEnum.WARN:
                            logger.warning("订阅错误,请求ID:%s,远程警告回报:%s", reqId, commonRsp.info)
                            return True
                        elif requestStatus == CommonStatusEnum.ERROR:
                            logger.error("订阅错误,请求ID:%s,远程错误回报:%s", reqId, commonRsp.info)
                            return False
                        else:
                            logger.error("订阅错误,请求ID:%s,未知的请求状态", reqId)
                            return False
                else:
                    RpcClientRspHandler.unregisterWaitReqId(reqId)
                    logger.error("订阅错误,请求ID: %s,等待回报超时", reqId)
                    return False

    @staticmethod
    def unsubscribe(contract, gatewayId=None, reqId=None, sync=False):
        if not reqId:
            reqId = str(uuid.uuid4())
        operatorId = Config.operatorId
        sourceNodeId = Config.nodeId

        commonReq = CommonReqField()
        commonReq.sourceNodeId = sourceNodeId
        commonReq.targetNodeId = 0
        commonReq.operatorId = operatorId
        commonReq.reqId = reqId

        rpcUnsubscribeReq = RpcUnsubscribeReq()

        rpcUnsubscribeReq.commonReq.CopyFrom(commonReq)
        rpcUnsubscribeReq.contract.CopyFrom(contract)

        if gatewayId:
            rpcUnsubscribeReq.gatewayId = gatewayId

        if sync:
            RpcClientRspHandler.registerWaitReqId(reqId)

        sendResult = RpcClientProcessService.sendRoutineCoreRpc(0, rpcUnsubscribeReq.SerializeToString(), reqId,
                                                                RpcId.UNSUBSCRIBE_REQ)

        if sync and not sendResult:
            RpcClientRspHandler.unregisterWaitReqId(reqId)
            return False

        if sync:
            startTime = time.time()
            while True:
                if time.time() - startTime < Config.rpcTimeOut:
                    rpcUnsubscribeRsp = RpcClientRspHandler.getAndRemoveRpcUnsubscribeRsp(reqId)
                    if not rpcUnsubscribeRsp:
                        rpcExceptionRsp = RpcClientRspHandler.getAndRemoveRpcExceptionRsp(reqId);
                        if rpcExceptionRsp:
                            logger.error("取消订阅错误,请求ID: %s, 远程错误回报 %s", reqId, rpcExceptionRsp.info)
                            return False
                        time.sleep(0.02)
                    else:
                        commonRsp = rpcUnsubscribeRsp.commonRsp
                        requestStatus = commonRsp.requestStatus
                        if requestStatus == CommonStatusEnum.SUCCESS:
                            return True
                        elif requestStatus == CommonStatusEnum.INFO:
                            logger.info("取消订阅错误,请求ID:%s,远程信息回报:%s", reqId, commonRsp.info)
                            return True
                        elif requestStatus == CommonStatusEnum.WARN:
                            logger.warning("取消订阅错误,请求ID:%s,远程警告回报:%s", reqId, commonRsp.info)
                            return True
                        elif requestStatus == CommonStatusEnum.ERROR:
                            logger.error("取消订阅错误,请求ID:%s,远程错误回报:%s", reqId, commonRsp.info)
                            return False
                        else:
                            logger.error("取消订阅错误,请求ID:%s,未知的请求状态", reqId)
                            return False
                else:
                    RpcClientRspHandler.unregisterWaitReqId(reqId)
                    logger.error("取消订阅错误,请求ID: %s,等待回报超时", reqId)
                    return False

    @staticmethod
    def submitOrder(submitOrderReq, reqId=None, sync=False):
        if not reqId:
            reqId = str(uuid.uuid4())
        operatorId = Config.operatorId
        sourceNodeId = Config.nodeId

        commonReq = CommonReqField()
        commonReq.sourceNodeId = sourceNodeId
        commonReq.targetNodeId = 0
        commonReq.operatorId = operatorId
        commonReq.reqId = reqId

        rpcSubmitOrderReq = RpcSubmitOrderReq()

        rpcSubmitOrderReq.commonReq.CopyFrom(commonReq)
        rpcSubmitOrderReq.submitOrderReq.CopyFrom(submitOrderReq)

        if sync:
            RpcClientRspHandler.registerWaitReqId(reqId)

        sendResult = RpcClientProcessService.sendRoutineCoreRpc(0, rpcSubmitOrderReq.SerializeToString(), reqId,
                                                                RpcId.SUBMIT_ORDER_REQ)

        if sync and not sendResult:
            RpcClientRspHandler.unregisterWaitReqId(reqId)
            return None

        if sync:
            startTime = time.time()
            while True:
                if time.time() - startTime < Config.rpcTimeOut:
                    rpcSubmitOrderRsp = RpcClientRspHandler.getAndRemoveRpcSubmitOrderRsp(reqId)
                    if not rpcSubmitOrderRsp:
                        rpcExceptionRsp = RpcClientRspHandler.getAndRemoveRpcExceptionRsp(reqId);
                        if rpcExceptionRsp:
                            logger.error("提交定单错误,请求ID: %s, 远程错误回报 %s", reqId, rpcExceptionRsp.info)
                            return None
                        time.sleep(0.02)
                    else:
                        commonRsp = rpcSubmitOrderRsp.commonRsp
                        requestStatus = commonRsp.requestStatus
                        if requestStatus == CommonStatusEnum.SUCCESS:
                            return rpcSubmitOrderRsp.orderId
                        elif requestStatus == CommonStatusEnum.INFO:
                            logger.info("提交定单错误,请求ID:%s,远程信息回报:%s", reqId, commonRsp.info)
                            return rpcSubmitOrderRsp.orderId
                        elif requestStatus == CommonStatusEnum.WARN:
                            logger.warning("提交定单错误,请求ID:%s,远程警告回报:%s", reqId, commonRsp.info)
                            return rpcSubmitOrderRsp.orderId
                        elif requestStatus == CommonStatusEnum.ERROR:
                            logger.error("提交定单错误,请求ID:%s,远程错误回报:%s", reqId, commonRsp.info)
                            return None
                        else:
                            logger.error("提交定单错误,请求ID:%s,未知的请求状态", reqId)
                            return None
                else:
                    RpcClientRspHandler.unregisterWaitReqId(reqId)
                    logger.error("提交定单错误,请求ID: %s,等待回报超时", reqId)
                    return None

    @staticmethod
    def cancelOrder(orderId=None, originOrderId=None, reqId=None, sync=False):
        if not reqId:
            reqId = str(uuid.uuid4())
        operatorId = Config.operatorId
        sourceNodeId = Config.nodeId

        commonReq = CommonReqField()
        commonReq.sourceNodeId = sourceNodeId
        commonReq.targetNodeId = 0
        commonReq.operatorId = operatorId
        commonReq.reqId = reqId

        cancelOrderReq = CancelOrderReqField()
        if not orderId and not originOrderId:
            logger.error("定单ID和原始定单ID不可同时为空")
            return False
        if originOrderId:
            cancelOrderReq.originOrderId = originOrderId
        if orderId:
            cancelOrderReq.orderId = orderId

        rpcCancelOrderReq = RpcCancelOrderReq()
        rpcCancelOrderReq.commonReq.CopyFrom(commonReq)
        rpcCancelOrderReq.cancelOrderReq.CopyFrom(cancelOrderReq)

        if sync:
            RpcClientRspHandler.registerWaitReqId(reqId)

        sendResult = RpcClientProcessService.sendRoutineCoreRpc(0, rpcCancelOrderReq.SerializeToString(), reqId,
                                                                RpcId.CANCEL_ORDER_REQ)

        if sync and not sendResult:
            RpcClientRspHandler.unregisterWaitReqId(reqId)
            return False

        if sync:
            startTime = time.time()
            while True:
                if time.time() - startTime < Config.rpcTimeOut:
                    rpcCancelOrderRsp = RpcClientRspHandler.getAndRemoveRpcCancelOrderRsp(reqId)
                    if not rpcCancelOrderRsp:
                        rpcExceptionRsp = RpcClientRspHandler.getAndRemoveRpcExceptionRsp(reqId);
                        if rpcExceptionRsp:
                            logger.error("撤销定单错误,请求ID: %s, 远程错误回报 %s", reqId, rpcExceptionRsp.info)
                            return False
                        time.sleep(0.02)
                    else:
                        commonRsp = rpcCancelOrderRsp.commonRsp
                        requestStatus = commonRsp.requestStatus
                        if requestStatus == CommonStatusEnum.SUCCESS:
                            return True
                        elif requestStatus == CommonStatusEnum.INFO:
                            logger.info("撤销定单错误,请求ID:%s,远程信息回报:%s", reqId, commonRsp.info)
                            return True
                        elif requestStatus == CommonStatusEnum.WARN:
                            logger.warning("撤销定单错误,请求ID:%s,远程警告回报:%s", reqId, commonRsp.info)
                            return True
                        elif requestStatus == CommonStatusEnum.ERROR:
                            logger.error("撤销定单错误,请求ID:%s,远程错误回报:%s", reqId, commonRsp.info)
                            return False
                        else:
                            logger.error("撤销定单错误,请求ID:%s,未知的请求状态", reqId)
                            return False
                else:
                    RpcClientRspHandler.unregisterWaitReqId(reqId)
                    logger.error("撤销定单错误,请求ID: %s,等待回报超时", reqId)
                    return False

    @staticmethod
    def searchContract(contract, reqId=None, sync=False):
        if not reqId:
            reqId = str(uuid.uuid4())
        operatorId = Config.operatorId
        sourceNodeId = Config.nodeId

        commonReq = CommonReqField()
        commonReq.sourceNodeId = sourceNodeId
        commonReq.targetNodeId = 0
        commonReq.operatorId = operatorId
        commonReq.reqId = reqId

        rpcSearchContractReq = RpcSearchContractReq()

        rpcSearchContractReq.commonReq.CopyFrom(commonReq)
        rpcSearchContractReq.contract.CopyFrom(contract)

        if sync:
            RpcClientRspHandler.registerWaitReqId(reqId)

        sendResult = RpcClientProcessService.sendRoutineCoreRpc(0, rpcSearchContractReq.SerializeToString(), reqId,
                                                                RpcId.SEARCH_CONTRACT_REQ)

        if sync and not sendResult:
            RpcClientRspHandler.unregisterWaitReqId(reqId)
            return False

        if sync:
            startTime = time.time()
            while True:
                if time.time() - startTime < Config.rpcTimeOut:
                    rpcSearchContractRsp = RpcClientRspHandler.getAndRemoveRpcSearchContractRsp(reqId)
                    if not rpcSearchContractRsp:
                        rpcExceptionRsp = RpcClientRspHandler.getAndRemoveRpcExceptionRsp(reqId);
                        if rpcExceptionRsp:
                            logger.error("搜寻合约错误,请求ID: %s, 远程错误回报 %s", reqId, rpcExceptionRsp.info)
                            return False
                        time.sleep(0.02)
                    else:
                        commonRsp = rpcSearchContractRsp.commonRsp
                        requestStatus = commonRsp.requestStatus
                        if requestStatus == CommonStatusEnum.SUCCESS:
                            return True
                        elif requestStatus == CommonStatusEnum.INFO:
                            logger.info("搜寻合约错误,请求ID:%s,远程信息回报:%s", reqId, commonRsp.info)
                            return True
                        elif requestStatus == CommonStatusEnum.WARN:
                            logger.warning("搜寻合约错误,请求ID:%s,远程警告回报:%s", reqId, commonRsp.info)
                            return True
                        elif requestStatus == CommonStatusEnum.ERROR:
                            logger.error("搜寻合约错误,请求ID:%s,远程错误回报:%s", reqId, commonRsp.info)
                            return False
                        else:
                            logger.error("搜寻合约错误,请求ID:%s,未知的请求状态", reqId)
                            return False
                else:
                    RpcClientRspHandler.unregisterWaitReqId(reqId)
                    logger.error("搜寻合约错误,请求ID: %s,等待回报超时", reqId)
                    return False

    @staticmethod
    def getAccountList(reqId=None, sync=False):
        if not reqId:
            reqId = str(uuid.uuid4())
        operatorId = Config.operatorId
        sourceNodeId = Config.nodeId

        commonReq = CommonReqField()
        commonReq.sourceNodeId = sourceNodeId
        commonReq.targetNodeId = 0
        commonReq.operatorId = operatorId
        commonReq.reqId = reqId

        rpcGetAccountListReq = RpcGetAccountListReq()

        rpcGetAccountListReq.commonReq.CopyFrom(commonReq)

        if sync:
            RpcClientRspHandler.registerWaitReqId(reqId)

        sendResult = RpcClientProcessService.sendRoutineCoreRpc(0, rpcGetAccountListReq.SerializeToString(), reqId,
                                                                RpcId.GET_ACCOUNT_LIST_REQ)

        if sync and not sendResult:
            RpcClientRspHandler.unregisterWaitReqId(reqId)
            return None

        if sync:
            startTime = time.time()
            while True:
                if time.time() - startTime < Config.rpcTimeOut:
                    rpcGetAccountListRsp = RpcClientRspHandler.getAndRemoveRpcGetAccountListRsp(reqId)
                    if not rpcGetAccountListRsp:
                        rpcExceptionRsp = RpcClientRspHandler.getAndRemoveRpcExceptionRsp(reqId)
                        if rpcExceptionRsp:
                            logger.error("获取账户列表错误,请求ID: %s, 远程错误回报 %s", reqId, rpcExceptionRsp.info)
                            return None
                        time.sleep(0.02)
                    else:
                        commonRsp = rpcGetAccountListRsp.commonRsp
                        requestStatus = commonRsp.requestStatus
                        if requestStatus == CommonStatusEnum.SUCCESS:
                            return rpcGetAccountListRsp.account
                        elif requestStatus == CommonStatusEnum.INFO:
                            logger.info("获取账户列表错误,请求ID:%s,远程信息回报:%s", reqId, commonRsp.info)
                            return rpcGetAccountListRsp.account
                        elif requestStatus == CommonStatusEnum.WARN:
                            logger.warning("获取账户列表错误,请求ID:%s,远程警告回报:%s", reqId, commonRsp.info)
                            return rpcGetAccountListRsp.account
                        elif requestStatus == CommonStatusEnum.ERROR:
                            logger.error("获取账户列表错误,请求ID:%s,远程错误回报:%s", reqId, commonRsp.info)
                            return None
                        else:
                            logger.error("获取账户列表错误,请求ID:%s,未知的请求状态", reqId)
                            return None
                else:
                    RpcClientRspHandler.unregisterWaitReqId(reqId)
                    logger.error("获取账户列表错误,请求ID: %s,等待回报超时", reqId)
                    return None

    @staticmethod
    def getMixContractList(reqId=None, sync=False):
        if not reqId:
            reqId = str(uuid.uuid4())
        operatorId = Config.operatorId
        sourceNodeId = Config.nodeId

        commonReq = CommonReqField()
        commonReq.sourceNodeId = sourceNodeId
        commonReq.targetNodeId = 0
        commonReq.operatorId = operatorId
        commonReq.reqId = reqId

        rpcGetMixContractListReq = RpcGetMixContractListReq()

        rpcGetMixContractListReq.commonReq.CopyFrom(commonReq)

        if sync:
            RpcClientRspHandler.registerWaitReqId(reqId)

        sendResult = RpcClientProcessService.sendRoutineCoreRpc(0, rpcGetMixContractListReq.SerializeToString(), reqId,
                                                                RpcId.GET_MIX_CONTRACT_LIST_REQ)

        if sync and not sendResult:
            RpcClientRspHandler.unregisterWaitReqId(reqId)
            return None

        if sync:
            startTime = time.time()
            while True:
                if time.time() - startTime < Config.rpcTimeOut:
                    rpcGetMixContractListRsp = RpcClientRspHandler.getAndRemoveRpcGetMixContractListRsp(reqId)
                    if not rpcGetMixContractListRsp:
                        rpcExceptionRsp = RpcClientRspHandler.getAndRemoveRpcExceptionRsp(reqId)
                        if rpcExceptionRsp:
                            logger.error("获取混合合约列表错误,请求ID: %s, 远程错误回报 %s", reqId, rpcExceptionRsp.info)
                            return None
                        time.sleep(0.02)
                    else:
                        commonRsp = rpcGetMixContractListRsp.commonRsp
                        requestStatus = commonRsp.requestStatus
                        if requestStatus == CommonStatusEnum.SUCCESS:
                            return rpcGetMixContractListRsp.contract
                        elif requestStatus == CommonStatusEnum.INFO:
                            logger.info("获取混合合约列表错误,请求ID:%s,远程信息回报:%s", reqId, commonRsp.info)
                            return rpcGetMixContractListRsp.contract
                        elif requestStatus == CommonStatusEnum.WARN:
                            logger.warning("获取混合合约列表错误,请求ID:%s,远程警告回报:%s", reqId, commonRsp.info)
                            return rpcGetMixContractListRsp.contract
                        elif requestStatus == CommonStatusEnum.ERROR:
                            logger.error("获取混合合约列表错误,请求ID:%s,远程错误回报:%s", reqId, commonRsp.info)
                            return None
                        else:
                            logger.error("获取混合合约列表错误,请求ID:%s,未知的请求状态", reqId)
                            return None
                else:
                    RpcClientRspHandler.unregisterWaitReqId(reqId)
                    logger.error("获取混合合约列表错误,请求ID: %s,等待回报超时", reqId)
                    return None

    @staticmethod
    def getPositionList(reqId=None, sync=False):
        if not reqId:
            reqId = str(uuid.uuid4())
        operatorId = Config.operatorId
        sourceNodeId = Config.nodeId

        commonReq = CommonReqField()
        commonReq.sourceNodeId = sourceNodeId
        commonReq.targetNodeId = 0
        commonReq.operatorId = operatorId
        commonReq.reqId = reqId

        rpcGetPositionListReq = RpcGetPositionListReq()

        rpcGetPositionListReq.commonReq.CopyFrom(commonReq)

        if sync:
            RpcClientRspHandler.registerWaitReqId(reqId)

        sendResult = RpcClientProcessService.sendRoutineCoreRpc(0, rpcGetPositionListReq.SerializeToString(), reqId,
                                                                RpcId.GET_POSITION_LIST_REQ)

        if sync and not sendResult:
            RpcClientRspHandler.unregisterWaitReqId(reqId)
            return None

        if sync:
            startTime = time.time()
            while True:
                if time.time() - startTime < Config.rpcTimeOut:
                    rpcGetPositionListRsp = RpcClientRspHandler.getAndRemoveRpcGetPositionListRsp(reqId)
                    if not rpcGetPositionListRsp:
                        rpcExceptionRsp = RpcClientRspHandler.getAndRemoveRpcExceptionRsp(reqId)
                        if rpcExceptionRsp:
                            logger.error("获取持仓列表错误,请求ID: %s, 远程错误回报 %s", reqId, rpcExceptionRsp.info)
                            return None
                        time.sleep(0.02)
                    else:
                        commonRsp = rpcGetPositionListRsp.commonRsp
                        requestStatus = commonRsp.requestStatus
                        if requestStatus == CommonStatusEnum.SUCCESS:
                            return rpcGetPositionListRsp.position
                        elif requestStatus == CommonStatusEnum.INFO:
                            logger.info("获取持仓列表错误,请求ID:%s,远程信息回报:%s", reqId, commonRsp.info)
                            return rpcGetPositionListRsp.position
                        elif requestStatus == CommonStatusEnum.WARN:
                            logger.warning("获取持仓列表错误,请求ID:%s,远程警告回报:%s", reqId, commonRsp.info)
                            return rpcGetPositionListRsp.position
                        elif requestStatus == CommonStatusEnum.ERROR:
                            logger.error("获取持仓列表错误,请求ID:%s,远程错误回报:%s", reqId, commonRsp.info)
                            return None
                        else:
                            logger.error("获取持仓列表错误,请求ID:%s,未知的请求状态", reqId)
                            return None
                else:
                    RpcClientRspHandler.unregisterWaitReqId(reqId)
                    logger.error("获取持仓列表错误,请求ID: %s,等待回报超时", reqId)
                    return None

    @staticmethod
    def getOrderList(reqId=None, sync=False):
        if not reqId:
            reqId = str(uuid.uuid4())
        operatorId = Config.operatorId
        sourceNodeId = Config.nodeId

        commonReq = CommonReqField()
        commonReq.sourceNodeId = sourceNodeId
        commonReq.targetNodeId = 0
        commonReq.operatorId = operatorId
        commonReq.reqId = reqId

        rpcGetOrderListReq = RpcGetOrderListReq()

        rpcGetOrderListReq.commonReq.CopyFrom(commonReq)

        if sync:
            RpcClientRspHandler.registerWaitReqId(reqId)

        sendResult = RpcClientProcessService.sendRoutineCoreRpc(0, rpcGetOrderListReq.SerializeToString(), reqId,
                                                                RpcId.GET_ORDER_LIST_REQ)

        if sync and not sendResult:
            RpcClientRspHandler.unregisterWaitReqId(reqId)
            return None

        if sync:
            startTime = time.time()
            while True:
                if time.time() - startTime < Config.rpcTimeOut:
                    rpcGetOrderListRsp = RpcClientRspHandler.getAndRemoveRpcGetOrderListRsp(reqId)
                    if not rpcGetOrderListRsp:
                        rpcExceptionRsp = RpcClientRspHandler.getAndRemoveRpcExceptionRsp(reqId)
                        if rpcExceptionRsp:
                            logger.error("获取定单列表错误,请求ID: %s, 远程错误回报 %s", reqId, rpcExceptionRsp.info)
                            return None
                        time.sleep(0.02)
                    else:
                        commonRsp = rpcGetOrderListRsp.commonRsp
                        requestStatus = commonRsp.requestStatus
                        if requestStatus == CommonStatusEnum.SUCCESS:
                            return rpcGetOrderListRsp.order
                        elif requestStatus == CommonStatusEnum.INFO:
                            logger.info("获取定单列表错误,请求ID:%s,远程信息回报:%s", reqId, commonRsp.info)
                            return rpcGetOrderListRsp.order
                        elif requestStatus == CommonStatusEnum.WARN:
                            logger.warning("获取定单列表错误,请求ID:%s,远程警告回报:%s", reqId, commonRsp.info)
                            return rpcGetOrderListRsp.order
                        elif requestStatus == CommonStatusEnum.ERROR:
                            logger.error("获取定单列表错误,请求ID:%s,远程错误回报:%s", reqId, commonRsp.info)
                            return None
                        else:
                            logger.error("获取定单列表错误,请求ID:%s,未知的请求状态", reqId)
                            return None
                else:
                    RpcClientRspHandler.unregisterWaitReqId(reqId)
                    logger.error("获取定单列表错误,请求ID: %s,等待回报超时", reqId)
                    return None

    @staticmethod
    def getTradeList(reqId=None, sync=False):
        if not reqId:
            reqId = str(uuid.uuid4())
        operatorId = Config.operatorId
        sourceNodeId = Config.nodeId

        commonReq = CommonReqField()
        commonReq.sourceNodeId = sourceNodeId
        commonReq.targetNodeId = 0
        commonReq.operatorId = operatorId
        commonReq.reqId = reqId

        rpcGetTradeListReq = RpcGetTradeListReq()

        rpcGetTradeListReq.commonReq.CopyFrom(commonReq)

        if sync:
            RpcClientRspHandler.registerWaitReqId(reqId)

        sendResult = RpcClientProcessService.sendRoutineCoreRpc(0, rpcGetTradeListReq.SerializeToString(), reqId,
                                                                RpcId.GET_TRADE_LIST_REQ)

        if sync and not sendResult:
            RpcClientRspHandler.unregisterWaitReqId(reqId)
            return None

        if sync:
            startTime = time.time()
            while True:
                if time.time() - startTime < Config.rpcTimeOut:
                    rpcGetTradeListRsp = RpcClientRspHandler.getAndRemoveRpcGetTradeListRsp(reqId)
                    if not rpcGetTradeListRsp:
                        rpcExceptionRsp = RpcClientRspHandler.getAndRemoveRpcExceptionRsp(reqId)
                        if rpcExceptionRsp:
                            logger.error("获取成交列表错误,请求ID: %s, 远程错误回报 %s", reqId, rpcExceptionRsp.info)
                            return None
                        time.sleep(0.02)
                    else:
                        commonRsp = rpcGetTradeListRsp.commonRsp
                        requestStatus = commonRsp.requestStatus
                        if requestStatus == CommonStatusEnum.SUCCESS:
                            return rpcGetTradeListRsp.trade
                        elif requestStatus == CommonStatusEnum.INFO:
                            logger.info("获取成交列表错误,请求ID:%s,远程信息回报:%s", reqId, commonRsp.info)
                            return rpcGetTradeListRsp.trade
                        elif requestStatus == CommonStatusEnum.WARN:
                            logger.warning("获取成交列表错误,请求ID:%s,远程警告回报:%s", reqId, commonRsp.info)
                            return rpcGetTradeListRsp.trade
                        elif requestStatus == CommonStatusEnum.ERROR:
                            logger.error("获取成交列表错误,请求ID:%s,远程错误回报:%s", reqId, commonRsp.info)
                            return None
                        else:
                            logger.error("获取成交列表错误,请求ID:%s,未知的请求状态", reqId)
                            return None
                else:
                    RpcClientRspHandler.unregisterWaitReqId(reqId)
                    logger.error("获取成交列表错误,请求ID: %s,等待回报超时", reqId)
                    return None

    @staticmethod
    def getTickList(reqId=None, sync=False):
        if not reqId:
            reqId = str(uuid.uuid4())
        operatorId = Config.operatorId
        sourceNodeId = Config.nodeId

        commonReq = CommonReqField()
        commonReq.sourceNodeId = sourceNodeId
        commonReq.targetNodeId = 0
        commonReq.operatorId = operatorId
        commonReq.reqId = reqId

        rpcGetTickListReq = RpcGetTickListReq();

        rpcGetTickListReq.commonReq.CopyFrom(commonReq)

        if sync:
            RpcClientRspHandler.registerWaitReqId(reqId)

        sendResult = RpcClientProcessService.sendRoutineCoreRpc(0, rpcGetTickListReq.SerializeToString(), reqId,
                                                                RpcId.GET_TICK_LIST_REQ)

        if sync and not sendResult:
            RpcClientRspHandler.unregisterWaitReqId(reqId)
            return None

        if sync:
            startTime = time.time()
            while True:
                if time.time() - startTime < Config.rpcTimeOut:
                    rpcGetTickListRsp = RpcClientRspHandler.getAndRemoveRpcGetTickListRsp(reqId)
                    if not rpcGetTickListRsp:
                        rpcExceptionRsp = RpcClientRspHandler.getAndRemoveRpcExceptionRsp(reqId)
                        if rpcExceptionRsp:
                            logger.error("获取Tick列表错误,请求ID: %s, 远程错误回报 %s", reqId, rpcExceptionRsp.info)
                            return None
                        time.sleep(0.02)
                    else:
                        commonRsp = rpcGetTickListRsp.commonRsp
                        requestStatus = commonRsp.requestStatus
                        if requestStatus == CommonStatusEnum.SUCCESS:
                            return rpcGetTickListRsp.tick
                        elif requestStatus == CommonStatusEnum.INFO:
                            logger.info("获取Tick列表错误,请求ID:%s,远程信息回报:%s", reqId, commonRsp.info)
                            return rpcGetTickListRsp.tick
                        elif requestStatus == CommonStatusEnum.WARN:
                            logger.warning("获取Tick列表错误,请求ID:%s,远程警告回报:%s", reqId, commonRsp.info)
                            return rpcGetTickListRsp.tick
                        elif requestStatus == CommonStatusEnum.ERROR:
                            logger.error("获取Tick列表错误,请求ID:%s,远程错误回报:%s", reqId, commonRsp.info)
                            return None
                        else:
                            logger.error("获取Tick列表错误,请求ID:%s,未知的请求状态", reqId)
                            return None
                else:
                    RpcClientRspHandler.unregisterWaitReqId(reqId)
                    logger.error("获取Tick列表错误,请求ID: %s,等待回报超时", reqId)
                    return None
