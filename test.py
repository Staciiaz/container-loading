from box import Box
from stacking import Stacking
from container import Container
from processor import Processor
import socket
import json


def test():
    Box.initialize()
    Stacking.initialize()
    server = socket.socket()
    server.connect(('127.0.0.1', 8200))
    print('Connected to server')
    boxes = [20, 30, 30, 10, 30, 15, 30, 15]
    print('Input Boxes:', boxes)
    server.send(json.dumps(boxes).encode())
    print('Sending boxes to server')
    print('Waiting for server to response')
    byte_length = server.recv(1024)
    response_data = server.recv(int.from_bytes(byte_length, 'big'))
    computed_data = json.loads(response_data.decode())
    containers, remaining_boxes = computed_data['containers'], computed_data['remaining_boxes']
    print('Remaining boxes:', remaining_boxes)
    print('Container amount:', len(containers))
    for i, container_data in enumerate(containers):
        container = Container.from_dict(container_data)
        print('Container', i, '=>', container.representation)
    server.close()
    print('Disconnected')


if __name__ == '__main__':
    test()
