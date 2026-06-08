from skip_list import SkipList
from p2p import Server, Client
import time, env


class DistributedSkipList(SkipList):
    def __init__(self, maxLevels, port):
        super().__init__(maxLevels)
        self.port = port
        self.server = Server(port)
        self.server.onInsert(self.insert)
        self.server.onSearch(self.search)
        self.server.onDelete(self.delete)
        self.clients = {}

    def serveAndConnect(self, hosts):
        self.server.serve()
        time.sleep(5)
        self.clients = {h: Client(f"{h}:{self.port}") for h in hosts}

    def getDataSite(self, data):
        if env.RANGE[0] is not None and data < env.RANGE[0]:
            return env.PEERS[0]
        if env.RANGE[1] is not None and data > env.RANGE[1]:
            return env.PEERS[1]
        return env.NAME

    def search(self, data, hops=0):
        site = self.getDataSite(data)
        if env.NAME == site:
            res = super().search(data)
            return res, hops

        res, total_hops = self.clients[site].sendSearch(data, hops)
        return res, total_hops

    def insert(self, data, hops=0):
        site = self.getDataSite(data)
        if env.NAME == site:
            super().insert(data)
            return None, hops

        total_hops = self.clients[site].sendInsert(data, hops)
        return None, total_hops

    def delete(self, data, hops=0):
        site = self.getDataSite(data)
        if env.NAME == site:
            super().delete(data)
            return None, hops

        total_hops = self.clients[site].sendDelete(data, hops)
        return None, total_hops
