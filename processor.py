from stacking import Stacking


class Processor:
    def __init__(self):
        self.__stacking = dict()
        self.__remaining_boxes = dict()

    @property
    def remaining_boxes(self):
        return dict(self.__remaining_boxes)

    def clear(self):
        self.__stacking.clear()
        self.__remaining_boxes.clear()

    def remove_boxes(self, box_type, amount):
        self.__remaining_boxes[box_type] -= amount
        if self.__remaining_boxes[box_type] <= 0:
            self.__remaining_boxes.pop(box_type)
        return box_type in self.__remaining_boxes

    def process(self, boxes):
        self.__remaining_boxes.update(boxes)
        for stacking in Stacking.get_all():
            if min([0 if x not in self.__remaining_boxes else self.__remaining_boxes[x] for x in stacking.boxes]) > 0:
                stacking_amount = min([self.__remaining_boxes[x] // stacking.boxes[x] for x in stacking.boxes])
                if stacking_amount > 0:
                    self.__stacking[stacking.type_id] = stacking_amount
                    [self.remove_boxes(x, stacking_amount * stacking.boxes[x]) for x in stacking.boxes]
        return self.__stacking
