from box import Box
from stacking import Stacking
from container import Container
from processor import Processor
import socket
import json


def print_response(response_data):
    # computed_data = json.loads(response_data)
    # containers, remaining_boxes = computed_data['containers'], computed_data['remaining_boxes']
    # print('Remaining boxes:', remaining_boxes)
    # print('Container amount:', len(containers))
    # for i, container_data in enumerate(containers):
    #     container = Container.from_dict(container_data)
    #     print('Container', i, '=>', container.representation)
    print(response_data)


def test():
    Box.initialize()
    Stacking.initialize()
    server = socket.socket()
    server.connect(('127.0.0.1', 8200))
    print('Connected to server')
    # boxes = [20, 30, 30, 10, 30, 15, 30, 15]
    boxes = [200, 300, 300, 300, 300, 300, 20, 30]
    print('Input Boxes:', boxes)
    server.send(json.dumps(boxes).encode())
    print('Sending boxes to server')
    print('Waiting for server to response')
    byte_length = server.recv(1024)
    response = server.recv(int.from_bytes(byte_length, 'big'))
    decoded_string = response.decode()
    print_response(decoded_string)
    with open('logs/test.json', 'w') as file:
        json_object = json.loads(decoded_string)
        file.write(json.dumps(json_object, indent=2))
    server.close()
    print('Disconnected')


if __name__ == '__main__':
    test()
