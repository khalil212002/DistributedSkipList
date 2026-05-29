from skip_list import SkipList
from p2p import Server, Client
import time, env


class DistributedSkipList(SkipList):
    def __init__(self, maxLevels, port):
        super().__init__(maxLevels)
        self.port = port
        self.server = Server(port)
        self.server.onInsert(self._on_remote_insert)
        self.server.onSearch(self._on_remote_search)
        self.server.onDelete(self._on_remote_delete)
        self.clients = {}

    def serveAndConnect(self, hosts):
        self.server.serve()
        time.sleep(5)
        self.clients = {h: Client(f"{h}:{self.port}") for h in hosts}

    def getDataSite(self, data):
        all_sites = [env.NAME, *env.PEERS]
        for i, p in enumerate(all_sites):
            if i < len(env.RANGES):
                r = env.RANGES[i]
                if (r[0] is None or r[0] <= data) and (r[1] is None or r[1] >= data):
                    return p
        return env.NAME

    def _on_remote_insert(self, data):
        return super().insert(data)

    def _on_remote_search(self, data):
        return super().search(data)

    def _on_remote_delete(self, data):
        return super().delete(data)

    def search(self, data):
        site = self.getDataSite(data)
        if env.NAME == site:
            res = super().search(data)
            return (True, res) if res is not None else (False, None)
        return self.clients[site].sendSearch(data)

    def insert(self, data):
        site = self.getDataSite(data)
        if env.NAME == site:
            res = super().search(data)
            return (True, res) if res is not None else (False, None)
        return self.clients[site].sendInsert(data)

    def delete(self, data):
        site = self.getDataSite(data)
        if env.NAME == site:
            res = super().search(data)
            return (True, res) if res is not None else (False, None)
        return self.clients[site].sendDelete(data)
