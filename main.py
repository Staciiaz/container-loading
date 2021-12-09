from box import Box
from stacking import Stacking
from container import ContainerSection
from processor import Processor
import os


def read_input(file_name):
    data_dict = dict()
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            for line in file:
                data = line.replace('\n', '').split(' ')
                data_dict[data[0]] = int(data[1])
    return data_dict


def main():
    Box.initialize()
    Stacking.initialize()
    input_boxes = read_input('data/input_boxes.txt')
    input_containers = read_input('data/input_containers.txt')
    processor = Processor()
    print('Input Boxes:', input_boxes)
    remaining_boxes, containers = processor.calculate(input_boxes)
    print('Remaining boxes:', remaining_boxes)
    print('Container amount:', len(containers))
    for i, container in enumerate(containers):
        print(container.representation)


if __name__ == '__main__':
    main()
