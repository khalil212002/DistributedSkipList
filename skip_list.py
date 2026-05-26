from linked_list_2d import LinkedList2D
import random


class SkipList:
    def __init__(self, maxLevels):
        self.maxLevels = maxLevels
        self.root = LinkedList2D(float("-inf"))
        self.height = 1

    def _search_node(self, data):
        cur = self.root

        while cur:
            while cur.next and cur.next.data < data:
                cur = cur.next

            if cur.next and cur.next.data == data:
                return cur.next

            cur = cur.bottom

        return None

    def search(self, data):
        node = self._search_node(data)
        return node.data if node is not None else None

    def insert(self, data):
        existing_node = self._search_node(data)
        if existing_node:
            while existing_node:
                existing_node.data = data
                existing_node = existing_node.bottom
            return

        node_levels = self._get_random_length() + 1

        while self.height < node_levels:
            new_root = LinkedList2D(float("-inf"))
            self.root.add_top(new_root)
            self.root = self.root.top
            self.height += 1

        cur = self.root
        last_new_node = None

        for level in range(self.height, 0, -1):
            while cur.next and cur.next.data < data:
                cur = cur.next

            if level <= node_levels:
                if cur.next and cur.next.data == data:
                    curr_node = cur.next
                else:
                    curr_node = cur.add_next_data(data)

                if last_new_node and last_new_node.bottom != curr_node:
                    last_new_node.add_bottom(curr_node)
                last_new_node = curr_node

            if cur.bottom:
                cur = cur.bottom

    def delete(self, data):
        cur = self._search_node(data)
        if cur is None:
            return
        while cur is not None:
            if cur.prev:
                cur.prev.next = cur.next
            if cur.next:
                cur.next.prev = cur.prev
            cur = cur.bottom

    def _get_random_length(self):
        # currently 50/50 chance of update can change weights to change this
        r = "".join(random.choices(["1", "0"], weights=[1, 1], k=self.maxLevels - 1))
        return len(r.split("0", 1)[0])
