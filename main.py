from box import Box
from stacking import Stacking
from processor import Processor
from optimize_finding import Container, process
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
    print('Remaining boxes:', processor.remaining_boxes)
    print('Output Stacking:')
    for stacking_type, stacking_amount in sorted(output_stacking.items(), key=lambda x: Stacking.get(x[0]).size[0]):
        stacking = Stacking.get(stacking_type)
        print(stacking.type_id, stacking.size, stacking_amount)


if __name__ == '__main__':
    main()
