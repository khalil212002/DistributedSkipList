import grpc, skiplist_pb2, skiplist_pb2_grpc
import pickle
from concurrent import futures


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.channel = grpc.insecure_channel(host + ":" + str(port))
        self.stub = skiplist_pb2_grpc.SkipListServiceStub(self.channel)

    def close(self):
        self.channel.close()

    def _send_request(self, action, data, hops):
        request = skiplist_pb2.SkipListRequest(
            action=action, data=pickle.dumps(data), hops=hops
        )
        return self.stub.SendRequest(request)

    def sendInsert(self, data, hops=1):
        response = self._send_request(skiplist_pb2.ACTION_INSERT, data=data, hops=hops)
        return response.code == skiplist_pb2.CODE_SUCCESS, None

    def sendDelete(self, data, hops=1):
        response = self._send_request(skiplist_pb2.ACTION_DELETE, data=data, hops=hops)
        return response.code == skiplist_pb2.CODE_SUCCESS, None

    def sendSearch(self, data, hops=1):
        response = self._send_request(skiplist_pb2.ACTION_SEARCH, data=data, hops=hops)
        if response.code == skiplist_pb2.CODE_SUCCESS:
            return True, pickle.loads(response.data)
        else:
            return False, (
                None if response.code == skiplist_pb2.CODE_NOT_FOUND else response.error
            )


class Server(skiplist_pb2_grpc.SkipListServiceServicer):
    def __init__(self, port):
        super().__init__()
        self.port = port
        self.onInsertFunc = None
        self.onSearchFunc = None
        self.onDeleteFunc = None

    def SendRequest(self, request, context):
        if request.action == skiplist_pb2.ACTION_INSERT:
            obj = pickle.loads(request.data)
            try:
                self.onInsertFunc(obj)
                return skiplist_pb2.SkipListResponse(
                    code=skiplist_pb2.CODE_SUCCESS, hops=request.hops + 1
                )
            except Exception as e:
                return skiplist_pb2.SkipListResponse(
                    code=skiplist_pb2.CODE_ERROR, error=str(e), hops=request.hops + 1
                )
        if request.action == skiplist_pb2.ACTION_DELETE:
            obj = pickle.loads(request.data)
            try:
                self.onDeleteFunc(obj)
                return skiplist_pb2.SkipListResponse(
                    code=skiplist_pb2.CODE_SUCCESS, hops=request.hops + 1
                )
            except Exception as e:
                return skiplist_pb2.SkipListResponse(
                    code=skiplist_pb2.CODE_ERROR, error=str(e), hops=request.hops + 1
                )
        if request.action == skiplist_pb2.ACTION_SEARCH:
            obj = pickle.loads(request.data)
            try:
                found = self.onSearchFunc(obj)
                if found is None:
                    return skiplist_pb2.SkipListResponse(
                        code=skiplist_pb2.CODE_NOT_FOUND, hops=request.hops + 1
                    )
                else:
                    return skiplist_pb2.SkipListResponse(
                        code=skiplist_pb2.CODE_SUCCESS,
                        hops=request.hops + 1,
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

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        skiplist_pb2_grpc.add_SkipListServiceServicer_to_server(self, server)
        server.add_insecure_port("[::]:" + str(self.port))
        server.start()
        server.wait_for_termination()
