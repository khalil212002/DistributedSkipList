import os

PORT = None
MAX_LIST_HEIGHT = None
MAX_WORKERS = None
NAME = None
PEERS = None
RANGES = None


def load():
    global PORT, MAX_LIST_HEIGHT, MAX_WORKERS, NAME, PEERS, RANGES
    PORT = int(os.getenv("PORT", "8000"))
    MAX_LIST_HEIGHT = int(os.getenv("MAX_LIST_HEIGHT", "10"))
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", "10"))
    NAME = os.getenv("NAME")
    peers_str = os.getenv("PEERS", "")
    PEERS = [p.strip() for p in peers_str.split(",") if p.strip()]
    
    RANGES = []
    if NAME:
        val = os.getenv(NAME)
        RANGES.append(eval(val) if val else (None, None))
    
    for p in PEERS:
        val = os.getenv(p)
        RANGES.append(eval(val) if val else (None, None))
