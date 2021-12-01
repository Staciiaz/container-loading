from copy import deepcopy
from time import time


class Box:
    def __init__(self, box_type, empty=True):
        self.type = box_type
        self.empty = empty
        self.previous_box = None

    def __str__(self):
        return self.id

    def __repr__(self):
        return '(type={0}, empty={1})'.format(self.type, self.empty)


class BoxStack:
    def __init__(self):
        self.inside = []
        self.available_box_types = {}
        self.pattern = []

    def __repr__(self):
        return '{0}'.format([['' if y.empty else y.type for y in x] for x in self.inside])

    def set_pattern(self, pattern):
        self.inside.clear()
        self.available_box_types.clear()
        self.pattern = pattern
        for row in pattern:
            data = []
            previous_box = None
            for box_type in row:
                box = Box(box_type)
                box.previous_box = previous_box
                if box_type in self.available_box_types:
                    self.available_box_types[box_type].append(box)
                else:
                    self.available_box_types[box_type] = [box]
                data.append(box)
                previous_box = box
            self.inside.append(data)

    def is_valid_for(self, box_type):
        if box_type in self.available_box_types:
            available_boxes = self.available_box_types[box_type]
            selected_box = available_boxes[0]
            if not selected_box.previous_box or (selected_box.previous_box and not selected_box.previous_box.empty):
                return True
        return False

    def is_full(self):
        return min([min([not y.empty for y in x]) for x in self.inside])

    def add(self, box_type):
        if self.is_valid_for(box_type):
            available_boxes = self.available_box_types[box_type]
            selected_box = available_boxes.pop(0)
            selected_box.empty = False
            if not available_boxes:
                self.available_box_types.pop(box_type)
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

    def __lt__(self, other):
        return self.fitness() < other.fitness()

    def fitness(self):
        return len(self.inside)

    def search_possibilities(self, box_type):
        possibilities = []
        for i in range(len(self.inside)):
            box_stack = self.inside[i]
            if box_stack.is_valid_for(box_type):
                container = Container(inside=deepcopy(self.inside))
                container.inside[i].add(box_type)
                possibilities.append(container)
        for stackable_type in Container.stackable_types:
            if box_type in [x[0] for x in stackable_type]:
                box_stack = BoxStack()
                box_stack.set_pattern(stackable_type)
                box_stack.add(box_type)
                container = Container(inside=deepcopy(self.inside))
                container.inside.append(box_stack)
                possibilities.append(container)
        return possibilities


class Node:
    def __init__(self, boxes: dict, container=Container(), is_root=False, is_leaf=False):
        self.container = container
        self.is_root = is_root
        self.is_leaf = is_leaf
        self.boxes = boxes
        self.children = {box: None for box in boxes}

    def __repr__(self):
        return str(self.container)


def remove_box(boxes, box_type):
    remaining_boxes = dict(boxes)
    remaining_boxes[box_type] -= 1
    if remaining_boxes[box_type] == 0:
        remaining_boxes.pop(box_type)
    return remaining_boxes


def process(boxes):
    print('Input:', boxes)
    queue = [Node(boxes, is_root=True)]
    containers = []
    seen_containers = set()
    start_timestamp = time()
    print('Processing ...')
    while queue:
        current_node = queue.pop(0)
        if current_node.children:
            for box_type in current_node.children:
                current_node.children[box_type] = [Node(remove_box(current_node.boxes, box_type), container=x)
                                                   for x in current_node.container.search_possibilities(box_type)]
                queue.extend(current_node.children[box_type])
        else:
            current_node.is_leaf = True
            if str(current_node.container) not in seen_containers:
                seen_containers.add(str(current_node.container))
                containers.append(current_node.container)
    max_container = min(containers)
    best_containers = [x for x in containers if x.fitness() == max_container.fitness()]
    end_timestamp = time()
    print('Possibilities found:', len(containers))
    print('Best Possibilities:')
    for container in best_containers:
        print(container)
    print('Elapsed Time:', end_timestamp - start_timestamp, 'second(s)')
    return best_containers
