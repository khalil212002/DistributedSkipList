from functools import total_ordering


@total_ordering
class Store:
    def __init__(self, key, value):
        if not isinstance(key, (int, str)):
            raise Exception("Key shoud be only string or int")
        self.key = key if isinstance(key, int) else key.lower()
        self.value = value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.key == other
        if not isinstance(other, Store):
            return False
        return self.key == other.key

    def __lt__(self, other):
        if isinstance(other, float):
            return other != float("-inf")
        if isinstance(other, str):
            return self.key < other
        if not isinstance(other, Store):
            return NotImplemented

        k1, k2 = self.key, other.key
        if type(k1) != type(k2):
            return str(k1) < str(k2)
        return k1 < k2
