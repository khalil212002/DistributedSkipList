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
        self.clients = {h: Client(f"{h}:{self.port}", True) for h in hosts}

    def getDataSite(self, data):
        all_sites = [env.NAME, *env.PEERS]
        for i, p in enumerate(all_sites):
            if i < len(env.RANGES):
                r = env.RANGES[i]
                if (r[0] is None or r[0] <= data) and (r[1] is None or r[1] >= data):
                    return p
        return env.NAME

    def search(self, data, isServer=False, hops=0):
        site = self.getDataSite(data)
        if isServer or env.NAME == site:
            res = super().search(data)
            return res, hops
        
        res, total_hops = self.clients[site].sendSearch(data, hops)
        return res, total_hops

    def insert(self, data, isServer=False, hops=0):
        site = self.getDataSite(data)
        if isServer or env.NAME == site:
            super().insert(data)
            return None, hops
        
        total_hops = self.clients[site].sendInsert(data, hops)
        return None, total_hops

    def delete(self, data, isServer=False, hops=0):
        site = self.getDataSite(data)
        if isServer or env.NAME == site:
            super().delete(data)
            return None, hops
        
        total_hops = self.clients[site].sendDelete(data, hops)
        return None, total_hops
