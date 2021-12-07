from box import Box
from stacking import Stacking
from container import Container
from processor import Processor
import os


def read_input(file_name):
    boxes = dict()
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            for line in file:
                data = line.replace('\n', '').split(' ')
                boxes[data[0]] = int(data[1])
    return boxes


def main():
    Box.initialize()
    Stacking.initialize()
    input_boxes = read_input('data/input_boxes.txt')
    processor = Processor()
    print('Input Boxes:', input_boxes)
    processor.update(input_boxes)
    output_stacking = processor.calculate_stacking()
    print('Remaining boxes:', processor.remaining_boxes)
    print('Output Stacking:', output_stacking)
    containers = processor.calculate_container()
    print('Container amount:', len(containers))
    for i, container in enumerate(containers):
        # print('Container', i, '>', 'Used Volume:', container.used_volume / container.volume * 100, '%')
        print('Container', i, '>', container)


if __name__ == '__main__':
    main()
