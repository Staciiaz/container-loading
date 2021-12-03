from box import Box
from stacking import Stacking
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
    output_stacking = processor.process(input_boxes)
    print('Input Boxes:', input_boxes)
    print('Stacking:', output_stacking)
    print('Remaining boxes:', processor.remaining_boxes)


if __name__ == '__main__':
    main()
