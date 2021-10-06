

class Status:
    """shape move status in square"""

    def __init__(self):
        # some numbers
        # shape should rotate
        self.rotate = False
        # shape should move left
        self.left = False
        # shape should move right
        self.right = False
        # shape should move down
        self.down = False

    def reset(self):
        self.__init__()

