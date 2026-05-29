import grpc, skiplist_pb2, skiplist_pb2_grpc
import pickle
from concurrent import futures
import env


class Client:
    def __init__(self, host, isServer=False):
        self.host = host
        self.isServer = isServer
        self.channel = grpc.insecure_channel(host)
        self.stub = skiplist_pb2_grpc.SkipListServiceStub(self.channel)

    def close(self):
        self.channel.close()

    def _send_request(self, action, data, hops):
        request = skiplist_pb2.SkipListRequest(
            action=action, data=pickle.dumps(data), hops=hops, isServer=self.isServer
        )
        return self.stub.SendRequest(request)

    def sendInsert(self, data, hops=1):
        response = self._send_request(skiplist_pb2.ACTION_INSERT, data=data, hops=hops)
        if response.code == skiplist_pb2.CODE_ERROR:
            raise Exception(response.error)
        return response.hops

    def sendDelete(self, data, hops=1):
        response = self._send_request(skiplist_pb2.ACTION_DELETE, data=data, hops=hops)
        if response.code == skiplist_pb2.CODE_ERROR:
            raise Exception(response.error)
        return response.hops

    def sendSearch(self, data, hops=1):
        response = self._send_request(skiplist_pb2.ACTION_SEARCH, data=data, hops=hops)
        if response.code == skiplist_pb2.CODE_ERROR:
            raise Exception(response.error)
        if response.code == skiplist_pb2.CODE_NOT_FOUND:
            return None, response.hops
        return pickle.loads(response.data), response.hops


class Server(skiplist_pb2_grpc.SkipListServiceServicer):
    def __init__(self, port):
        super().__init__()
        self.port = port
        self.onInsertFunc = None
        self.onSearchFunc = None
        self.onDeleteFunc = None

    def SendRequest(self, request, context):
        isServer = request.isServer if request.HasField("isServer") else False
        if request.action == skiplist_pb2.ACTION_INSERT:
            obj = pickle.loads(request.data)
            try:
                _, final_hops = self.onInsertFunc(obj, isServer, request.hops)
                return skiplist_pb2.SkipListResponse(
                    code=skiplist_pb2.CODE_SUCCESS, hops=final_hops
                )
            except Exception as e:
                return skiplist_pb2.SkipListResponse(
                    code=skiplist_pb2.CODE_ERROR, error=str(e), hops=request.hops + 1
                )
        if request.action == skiplist_pb2.ACTION_DELETE:
            obj = pickle.loads(request.data)
            try:
                _, final_hops = self.onDeleteFunc(obj, isServer, request.hops)
                return skiplist_pb2.SkipListResponse(
                    code=skiplist_pb2.CODE_SUCCESS, hops=final_hops
                )
            except Exception as e:
                return skiplist_pb2.SkipListResponse(
                    code=skiplist_pb2.CODE_ERROR, error=str(e), hops=request.hops + 1
                )
        if request.action == skiplist_pb2.ACTION_SEARCH:
            obj = pickle.loads(request.data)
            try:
                found, final_hops = self.onSearchFunc(obj, isServer, request.hops)
                if found is None:
                    return skiplist_pb2.SkipListResponse(
                        code=skiplist_pb2.CODE_NOT_FOUND, hops=final_hops
                    )
                else:
                    return skiplist_pb2.SkipListResponse(
                        code=skiplist_pb2.CODE_SUCCESS,
                        hops=final_hops,
                        data=pickle.dumps(found),
                    )
            except Exception as e:
                return skiplist_pb2.SkipListResponse(
                    code=skiplist_pb2.CODE_ERROR, error=str(e), hops=request.hops + 1
                )

    def onInsert(self, callback):
        self.onInsertFunc = callback

    def onSearch(self, callback):
        self.onSearchFunc = callback

    def onDelete(self, callback):
        self.onDeleteFunc = callback

    def serve(self):
        if None in [self.onDeleteFunc, self.onInsertFunc, self.onSearchFunc]:
            raise Exception("Should init callbacks before running server")

        self.server = grpc.server(
            futures.ThreadPoolExecutor(max_workers=env.MAX_WORKERS)
        )
        skiplist_pb2_grpc.add_SkipListServiceServicer_to_server(self, self.server)
        self.server.add_insecure_port("[::]:" + str(self.port))
        self.server.start()

    def wait(self):
        self.server.wait_for_termination()
