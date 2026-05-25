from linked_list_2d import LinkedList2D
import random


class SkipList:
    def __init__(self, maxLevels):
        self.maxLevels = maxLevels
        self.root = LinkedList2D(float("-inf"))
        self.height = 1

    def search(self, data):
        cur = self.root

        while cur:
            while cur.next and cur.next.data < data:
                cur = cur.next

            if cur.next and cur.next.data == data:
                return cur.next.data

            cur = cur.bottom

        return None

    def insert(self, data):
        node_levels = self._get_random_length() + 1

        while self.height < node_levels:
            new_root = LinkedList2D(float("-inf"))
            new_root.bottom = self.root
            self.root.top = new_root
            self.root = new_root
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

                if last_new_node:
                    last_new_node.bottom = curr_node
                    curr_node.top = last_new_node
                last_new_node = curr_node

            if cur.bottom:
                cur = cur.bottom

    def _get_random_length(self):
        # currently 50/50 chance of update can change weights to change this
        r = "".join(random.choices(["1", "0"], weights=[1, 1], k=self.maxLevels - 1))
        return len(r.split("0", 1)[0])
