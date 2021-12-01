from copy import deepcopy
from time import time


class Box:
    def __init__(self, box_id, box_type):
        self.id = box_id
        self.type = box_type
        self.previous_box = None

    def __str__(self):
        return self.id

    def __repr__(self):
        return '(id={0}, type={1})'.format(self.id, self.type)


class BoxStack:
    def __init__(self):
        self.inside = []
        self.available_box_types = {}
        self.pattern = []

    def __repr__(self):
        return '{0}'.format([[y.id for y in x] for x in self.inside])

    def set_pattern(self, pattern):
        self.inside.clear()
        self.available_box_types.clear()
        self.pattern = pattern
        for row in pattern:
            data = []
            previous_box = None
            for box_type in row:
                box = Box(None, box_type)
                box.previous_box = previous_box
                if box_type in self.available_box_types:
                    self.available_box_types[box_type].append(box)
                else:
                    self.available_box_types[box_type] = [box]
                data.append(box)
                previous_box = box
            self.inside.append(data)

    def is_valid_for(self, box):
        if box.type in self.available_box_types:
            available_boxes = self.available_box_types[box.type]
            selected_box = available_boxes[0]
            if not selected_box.previous_box or (selected_box.previous_box and selected_box.previous_box.id):
                return True
        return False

    def add(self, box):
        if self.is_valid_for(box):
            available_boxes = self.available_box_types[box.type]
            selected_box = available_boxes.pop(0)
            selected_box.id = box.id
            if not available_boxes:
                self.available_box_types.pop(box.type)
            return True
        return False


class Container:
    stackable_types = None

    def __init__(self, inside=None):
        if not inside:
            inside = []
        self.inside = inside

    def __str__(self):
        return str(self.inside)

    def search_possibilities(self, box):
        possibilities = []
        for i in range(len(self.inside)):
            box_stack = self.inside[i]
            if box_stack.is_valid_for(box):
                container = Container(inside=deepcopy(self.inside))
                container.inside[i].add(box)
                possibilities.append(container)
        for stackable_type in Container.stackable_types:
            if box.type in [x[0] for x in stackable_type]:
                box_stack = BoxStack()
                box_stack.set_pattern(stackable_type)
                box_stack.add(box)
                container = Container(inside=deepcopy(self.inside))
                container.inside.append(box_stack)
                possibilities.append(container)
        return possibilities


class Node:
    def __init__(self, boxes, container=Container(), is_root=False, is_leaf=False):
        self.container = container
        self.is_root = is_root
        self.is_leaf = is_leaf
        self.children = {box: None for box in boxes}

    def __repr__(self):
        return str(self.container)


def fitness(container):
    return len(container.inside)


def convert_to_boxes(input_data):
    boxes = []
    for box_type in input_data:
        amount = input_data[box_type]
        for index in range(amount):
            boxes.append(Box('{0} [{1}]'.format(box_type, index), box_type))
    return boxes


def process(data):
    boxes = convert_to_boxes(data)
    print('Input:', boxes)
    queue = [Node(boxes, is_root=True)]
    containers = []
    seen_containers = set()
    start_timestamp = time()
    print('Processing ...')
    while queue:
        current_node = queue.pop(0)
        if current_node.children:
            for box in current_node.children:
                remaining_boxes = list(current_node.children)
                remaining_boxes.remove(box)
                current_node.children[box] = [Node(remaining_boxes, container=x)
                                              for x in current_node.container.search_possibilities(box)]
                queue.extend(current_node.children[box])
        else:
            current_node.is_leaf = True
            if str(current_node.container) not in seen_containers:
                seen_containers.add(str(current_node.container))
                containers.append(current_node.container)
    max_container = min(containers, key=fitness)
    max_fitness_value = fitness(max_container)
    best_containers = [x for x in containers if fitness(x) == max_fitness_value]
    end_timestamp = time()
    print('Possibilities found:', len(containers))
    print('Best Possibilities:')
    for container in best_containers:
        print(container)
    print('Elapsed Time:', end_timestamp - start_timestamp, 'second(s)')
