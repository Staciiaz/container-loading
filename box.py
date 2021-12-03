import numpy as np


class Box:
    box_types = dict()

    def __init__(self, type_id, volume):
        self.type_id = type_id
        self.volume = np.array(volume)

    def __repr__(self):
        return '(type_id={0}, volume={1})'.format(self.type_id, self.volume)

    @property
    def width(self):
        return self.volume[0]

    @property
    def length(self):
        return self.volume[1]

    @property
    def height(self):
        return self.volume[2]

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
            'WUL01': [1515, 2220, 85],
            'WUL03': [1515, 2220, 73],
            'HU': [76, 112, 109],
            'U': [76, 112, 73],
            'MU': [76, 112, 54],
            'H/D+p': [110, 150, 150]
        })
