from box import Box
from stacking import Stacking


class Processor:
    def __init__(self):
        self.__remaining_boxes = dict()

    @property
    def remaining_boxes(self):
        return dict(self.__remaining_boxes)

    def clear(self):
        self.__remaining_boxes.clear()

    def remove_remaining_boxes(self, box_type, amount):
        self.__remaining_boxes[box_type] -= amount
        if self.__remaining_boxes[box_type] <= 0:
            self.__remaining_boxes.pop(box_type)
        return box_type in self.__remaining_boxes

    def process(self, boxes):
        self.__remaining_boxes.update(boxes)
        output_stacking = dict()
        for stacking in Stacking.get_all():
            if min([0 if x not in self.__remaining_boxes else self.__remaining_boxes[x] for x in stacking.boxes]) > 0:
                output_stacking[stacking.type_id] = min([self.__remaining_boxes[x] // stacking.boxes[x] for x in stacking.boxes])
                [self.remove_remaining_boxes(x, output_stacking[stacking.type_id] * stacking.boxes[x]) for x in stacking.boxes]
        return output_stacking


def main():
    Box.initialize()
    Stacking.initialize()
    input_boxes = {
        'HU': 21,
        'U': 30,
        'MU': 42
    }
    processor = Processor()
    output_stacking = processor.process(input_boxes)
    print('Stacking:', output_stacking)
    print('Remaining boxes:', processor.remaining_boxes)


if __name__ == '__main__':
    main()
