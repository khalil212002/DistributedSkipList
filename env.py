import os

PORT = None
MAX_LIST_HEIGHT = None
MAX_WORKERS = None
NAME = None
PEERS = None


def load():
    global PORT, MAX_LIST_HEIGHT, MAX_WORKERS, NAME, PEERS
    PORT = int(os.getenv("PORT"))
    MAX_LIST_HEIGHT = int(os.getenv("MAX_LIST_HEIGHT"))
    MAX_WORKERS = int(os.getenv("MAX_LIST_HEIGHT"))
    NAME = os.getenv("NAME")
    PEERS = os.getenv("PEERS").split(",")
