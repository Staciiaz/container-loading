from box import Box
from functools import reduce
from collections import Counter
import numpy as np


class Stacking:
    stacking_types = dict()

    def __init__(self, type_id, stacking_list):
        self.type_id = type_id
        self.__stacking_list = stacking_list
        self.__volume = self.__calculate_volume()
        self.__boxes = self.__count_boxes()

    def __repr__(self):
        return '(type_id={0}, volume={1})'.format(self.type_id, self.volume)

    def __count_boxes(self):
        counter = Counter(reduce(lambda a, b: a + b, [reduce(lambda x, y: x + y, z.tolist()) for z in self.__stacking_list]))
        return dict(counter)

    def __calculate_volume(self):
        volume = np.zeros((3,))
        volume[0] = sum([Box.get(box_type).width for box_type in self.__stacking_list[0][0]])
        volume[1] = sum([Box.get(box_type).length for box_type in [x[0] for x in self.__stacking_list[0]]])
        volume[2] = sum([max([Box.get(box_type).height for box_type in reduce(lambda x, y: x + y, stacking.tolist())]) for stacking in self.__stacking_list])
        return volume

    @property
    def is_same_type(self):
        return len(self.boxes) == 1

    @property
    def volume(self):
        return self.__volume

    @property
    def boxes(self):
        return self.__boxes

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
            'Mix_1': [np.full((1, 1), 'MU'), np.full((1, 1), 'MU'), np.full((1, 1), 'HU')],
            'Mix_2': [np.full((2, 1), 'U'), np.full((1, 1), 'H/D+p')],
            'Mix_3': [np.full((2, 1), 'MU'), np.full((1, 1), 'H/D+p')],
            'Mix_4': [np.full((1, 2), 'H/D+p'), np.full((1, 1), 'WUL01')],
            'Mix_5': [np.full((1, 3), 'HU'), np.full((1, 1), '2HUL')],
            'Mix_6': [np.full((1, 3), 'U'), np.full((1, 3), 'U'), np.full((1, 1), '2UL')],
            'Mix_7': [np.full((1, 1), 'WUL01'), np.full((1, 1), 'WUL03'), np.full((1, 1), 'WUL03')],
            'Mix_8': [np.full((1, 3), 'MU'), np.full((1, 3), 'MU'), np.full((1, 1), '2HUL')],
            'Same_HU': [np.full((1, 1), 'HU'), np.full((1, 1), 'HU')],
            'Same_U': [np.full((1, 1), 'U'), np.full((1, 1), 'U'), np.full((1, 1), 'U')],
            'Same_MU': [np.full((1, 1), 'MU'), np.full((1, 1), 'MU'), np.full((1, 1), 'MU'), np.full((1, 1), 'MU')],
            'Same_2HUL': [np.full((1, 1), '2HUL'), np.full((1, 1), '2HUL')],
            'Same_2UL': [np.full((1, 1), '2UL'), np.full((1, 1), '2UL'), np.full((1, 1), '2UL')],
            'Same_WUL03': [np.full((1, 1), 'WUL03'), np.full((1, 1), 'WUL03'), np.full((1, 1), 'WUL03')]
        })
