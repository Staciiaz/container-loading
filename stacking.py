from box import Box
from functools import reduce
from collections import Counter
import numpy as np


class Stacking:
    stacking_types = dict()

    def __init__(self, type_id, boxes):
        self.type_id = type_id
        self.boxes = boxes
        self.used_boxes = self.__count_boxes()
        self.size = self.__calculate_size()

    def __repr__(self):
        return '(type_id={0}, volume={1})'.format(self.type_id, self.volume)

    def __count_boxes(self):
        counter = Counter(reduce(lambda a, b: a + b, [reduce(lambda x, y: x + y, z.tolist()) for z in self.boxes]))
        return dict(counter)

    def __calculate_size(self):
        size = np.zeros((3,))
        size[0] = sum([Box.get(box_type).width for box_type in self.boxes[0][0]])
        size[1] = sum([Box.get(box_type).length for box_type in [x[0] for x in self.boxes[0]]])
        size[2] = sum([max([Box.get(box_type).height for box_type in reduce(lambda x, y: x + y, stacking.tolist())]) for stacking in self.boxes])
        return size

    @property
    def is_same_type(self):
        return len(self.boxes) == 1

    @property
    def width(self):
        return self.size[0]

    @property
    def length(self):
        return self.size[1]

    @property
    def height(self):
        return self.size[2]

    @property
    def volume_2d(self):
        return self.width * self.length

    @staticmethod
    def register(stacking_types):
        for stacking_type in stacking_types:
            Stacking.stacking_types[stacking_type] = Stacking(stacking_type, stacking_types[stacking_type])

    @staticmethod
    def get(stacking_type):
        return Stacking.stacking_types.get(stacking_type, None)

    @staticmethod
    def get_all():
        return Stacking.stacking_types.values()

    @staticmethod
    def initialize():
        Stacking.register({
            '201': [np.full((1, 1), 'MU'), np.full((1, 1), 'MU'), np.full((1, 1), 'HU')],
            '202': [np.full((2, 1), 'U'), np.full((1, 1), 'etc')],
            '203': [np.full((2, 1), 'MU'), np.full((1, 1), 'etc')],
            '204': [np.full((1, 2), 'etc'), np.full((1, 1), 'WUL01')],
            '205': [np.full((3, 1), 'HU'), np.full((1, 1), '2HUL')],
            '206': [np.full((3, 1), 'U'), np.full((3, 1), 'U'), np.full((1, 1), '2UL')],
            '207': [np.full((1, 1), 'WUL01'), np.full((1, 1), 'WUL03'), np.full((1, 1), 'WUL03')],
            '208': [np.full((3, 1), 'MU'), np.full((3, 1), 'MU'), np.full((1, 1), '2HUL')],
            '101': [np.full((1, 1), 'HU'), np.full((1, 1), 'HU')],
            '102': [np.full((1, 1), 'U'), np.full((1, 1), 'U'), np.full((1, 1), 'U')],
            '103': [np.full((1, 1), 'MU'), np.full((1, 1), 'MU'), np.full((1, 1), 'MU'), np.full((1, 1), 'MU')],
            '104': [np.full((1, 1), '2HUL'), np.full((1, 1), '2HUL')],
            '105': [np.full((1, 1), '2UL'), np.full((1, 1), '2UL'), np.full((1, 1), '2UL')],
            '106': [np.full((1, 1), 'WUL03'), np.full((1, 1), 'WUL03'), np.full((1, 1), 'WUL03')],
        })
