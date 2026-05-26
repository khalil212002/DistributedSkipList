from skip_list import SkipList
from p2p import Server, Client
import time


class DistributedSkipList(SkipList):
    def __init__(self, maxLevels, port):
        super().__init__(maxLevels)
        self.port = port
        self.server = Server(port)
        self.server.onInsert(self._on_remote_insert)
        self.server.onSearch(self._on_remote_search)
        self.server.onDelete(self._on_remote_delete)

    def serveAndConnect(self, hosts):
        self.server.serve()
        time.sleep(5)
        peer_addresses = [f"{h}:{self.port}" for h in hosts]
        self.clients = [Client(h) for h in peer_addresses]

    def _on_remote_insert(self, data):
        return super().insert(data)

    def _on_remote_search(self, data):
        return super().search(data)

    def _on_remote_delete(self, data):
        return super().delete(data)

    def search(self, data):
        # TODO: Implement distributed search logic
        return super().search(data)

    def insert(self, data):
        # TODO: Implement distributed insert logic
        return super().insert(data)

    def delete(self, data):
        # TODO: Implement distributed delete logic
        return super().delete(data)
