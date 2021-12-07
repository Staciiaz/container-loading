from stacking import Stacking
from container import Container
import math


class Processor:
    def __init__(self):
        self.__stacking = dict()
        self.__remaining_boxes = dict()

    @property
    def remaining_boxes(self):
        return dict(self.__remaining_boxes)

    def update(self, boxes):
        self.__remaining_boxes.update(boxes)

    def clear(self):
        self.__stacking.clear()
        self.__remaining_boxes.clear()

    def remove_boxes(self, box_type, amount):
        self.__remaining_boxes[box_type] -= amount
        if self.__remaining_boxes[box_type] <= 0:
            self.__remaining_boxes.pop(box_type)
        return box_type in self.__remaining_boxes

    def calculate_stacking(self):
        for stacking in Stacking.get_all():
            if min([0 if x not in self.__remaining_boxes else self.__remaining_boxes[x] for x in stacking.boxes]) > 0:
                stacking_amount = min([self.__remaining_boxes[x] // stacking.boxes[x] for x in stacking.boxes])
                if stacking_amount > 0:
                    self.__stacking[stacking.type_id] = stacking_amount
                    [self.remove_boxes(x, stacking_amount * stacking.boxes[x]) for x in stacking.boxes]
        return self.__stacking

    def calculate_container(self):
        container_volume = 237 * 1200  # [237 * 1200] container volume in 2d
        containers = [Container(container_volume)]
        for stacking_type, stacking_amount in sorted(self.__stacking.items(),
                                                     key=lambda x: Stacking.get(x[0]).volume_2d, reverse=True):
            stacking = Stacking.get(stacking_type)
            for _ in range(stacking_amount):
                best_fit_container = min([x for x in containers if x.available_volume >= stacking.volume_2d],
                                         key=lambda x: x.available_volume, default=None)
                if best_fit_container:
                    best_fit_container.use(stacking)
                else:
                    container = Container(container_volume)
                    container.use(stacking)
                    containers.append(container)
        return containers
