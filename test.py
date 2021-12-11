from box import Box
from stacking import Stacking
from container import ContainerSection
from processor import Processor
from util import read_input
import socket
import json


def compute(boxes):
    processor = Processor()
    print('Input Boxes:', boxes)
    remaining_boxes, remaining_sections, containers = processor.calculate(boxes, large_container=True)
    print('Remaining boxes:', remaining_boxes)
    print('Remaining sections:', len(remaining_sections))
    print('Container amount:', len(containers))
    for i, container in enumerate(containers):
        print('Container', i, '=>', container.representation)


def test():
    # Box.initialize()
    # Stacking.initialize()
    # input_boxes = read_input('data/input_boxes.txt')
    # compute(input_boxes)
    server = socket.socket()
    server.connect(('127.0.0.1', 8200))
    print('Connected to server')
    boxes = [20, 30, 30, 10, 30, 15, 30, 15]
    server.send(json.dumps(boxes).encode())
    print('Sending boxes to server')
    print('Waiting for server to response')
    byte_length = server.recv(1024)
    response_data = server.recv(int.from_bytes(byte_length, 'big'))
    result = json.loads(response_data.decode())
    print(result)
    server.close()
    print('Disconnected')


if __name__ == '__main__':
    test()
