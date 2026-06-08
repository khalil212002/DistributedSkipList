import os

PORT = None
MAX_LIST_HEIGHT = None
MAX_WORKERS = None
NAME = None
PEERS = None
RANGE = None


def parse_val(val):
    if val is None or val == "None" or val == "":
        return None
    try:
        return int(val)
    except ValueError:
        return val


def load():
    global PORT, MAX_LIST_HEIGHT, MAX_WORKERS, NAME, PEERS, RANGE
    PORT = int(os.getenv("PORT", "8000"))
    MAX_LIST_HEIGHT = int(os.getenv("MAX_LIST_HEIGHT", "10"))
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", "10"))
    NAME = os.getenv("NAME")
    PEERS = (parse_val(os.getenv("PEER_LOWER")), parse_val(os.getenv("PEER_HIGHER")))

    RANGE = (parse_val(os.getenv("RANGE_START")), parse_val(os.getenv("RANGE_END")))
