from box import Box
from stacking import Stacking
from container import ContainerSection
from processor import Processor
import socket
import json


def compute(box_array):
    boxes = dict(zip(Box.get_types(), box_array))
    processor = Processor()
    remaining_boxes, containers = processor.calculate(boxes, large_container=True)
    return {
        'containers': [x.to_dict() for x in containers],
        'remaining_boxes': remaining_boxes
    }


def main():
    Box.initialize()
    Stacking.initialize()
    port = 8200
    server = socket.socket()
    print('Socket created')
    server.bind(('', port))
    print('Socket bind to port {}'.format(port))
    server.listen(5)
    print('Socket is listening')
    while True:
        client, address = server.accept()
        print(f'Got connection from {address}')
        print('Waiting for client to send data')
        receive_data = client.recv(1024)
        boxes = json.loads(receive_data.decode())
        print('Computing data ...')
        computed_data = compute(boxes)
        with open('logs/latest.json', 'w') as file:
            file.write(json.dumps(computed_data, indent=2))
        json_encode_data = json.dumps(computed_data)
        client.send(len(json_encode_data).to_bytes(4, 'big'))
        client.send(json_encode_data.encode())
        print('Sending computed data to client')


if __name__ == '__main__':
    main()
