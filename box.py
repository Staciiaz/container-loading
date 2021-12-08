import numpy as np


class Box:
    box_types = dict()

    def __init__(self, type_id, size):
        self.type_id = type_id
        self.size = np.array(size)

    def __repr__(self):
        return '(type_id={0}, size={1})'.format(self.type_id, self.size)

    @property
    def width(self):
        return self.size[0]

    @property
    def length(self):
        return self.size[1]

    @property
    def height(self):
        return self.size[2]

    @staticmethod
    def register(box_types):
        for box_type in box_types:
            Box.box_types[box_type] = Box(box_type, box_types[box_type])

    @staticmethod
    def get(box_type):
        return Box.box_types.get(box_type, None)

    @staticmethod
    def initialize():
        Box.register({
            '2HUL': [110, 180, 109],
            '2UL': [110, 180, 73],
            'WUL01': [222, 152, 85],
            'WUL03': [222, 152, 73],
            'HU': [112, 76, 109],
            'U': [112, 76, 73],
            'MU': [112, 76, 54],
            'etc': [110, 150, 150]
        })
