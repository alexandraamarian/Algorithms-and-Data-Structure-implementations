class AVLNode:
    def __init__(self, key=0, value=None):
        self.key = key
        self.value = value
        self.parent = None
        self.left = None
        self.right = None
        self.height = 0

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value

    def get_parent(self):
        return self.parent

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_height(self):
        return self.height

    def to_string(self):
        return "key:" + str(self.key) + ", value: " + str(self.value)
