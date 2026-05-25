class LinkedList2D:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None
        self.top = None
        self.bottom = None

    def add_next(self, node):
        if self.next is not None:
            self.next.prev = node
        node.next = self.next
        self.next = node
        node.prev = self

    def add_next_data(self, data):
        new_node = LinkedList2D(data)
        self.add_next(new_node)
        return new_node

    def add_prev(self, node):
        if self.prev is not None:
            self.prev.next = node
        node.prev = self.prev
        self.prev = node
        node.next = self

    def add_prev_data(self, data):
        new_node = LinkedList2D(data)
        self.add_prev(new_node)
        return new_node

    def add_top(self, node):
        if self.top is not None:
            self.top.bottom = node
        node.top = self.top
        self.top = node
        node.bottom = self

    def add_top_data(self, data):
        new_node = LinkedList2D(data)
        self.add_top(new_node)
        return new_node

    def add_bottom(self, node):
        if self.bottom is not None:
            self.bottom.top = node
        node.bottom = self.bottom
        self.bottom = node
        node.top = self

    def add_bottom_data(self, data):
        new_node = LinkedList2D(data)
        self.add_bottom(new_node)
        return new_node
