from optimize_finding import Container, process
from copy import deepcopy


class StackableType:
    __box_types = {}
    __stackable_types = {}

    @staticmethod
    def register_box_type(type_id, properties):
        StackableType.__box_types[type_id] = properties

    @staticmethod
    def register_stackable_type(type_id, patterns):
        StackableType.__stackable_types[type_id] = patterns

    @staticmethod
    def get_box_type(type_id):
        return StackableType.__box_types.get(type_id, None)

    @staticmethod
    def get_stackable_type(type_id):
        if type_id in StackableType.__stackable_types:
            stackable_type = deepcopy(StackableType.__stackable_types.get(type_id))
            for i in range(len(stackable_type)):
                if StackableType.get_stackable_type(stackable_type[i]):
                    stackable_type[i] = StackableType.get_stackable_type(stackable_type[i])
            return stackable_type
        return None


def main():
    input_data = {
        'Box_Type_A': 4,
        'Box_Type_B': 2
    }
    Container.stackable_types = [
        [['Box_Type_A', 'Box_Type_A'], ['Box_Type_B']]
    ]
    process(input_data)
    # StackableType.register_box_type('Box_Type_A', None)
    # StackableType.register_box_type('Box_Type_B', None)
    # StackableType.register_stackable_type('HU', ['Box_Type_A', 'Box_Type_A'])
    # StackableType.register_stackable_type('U', ['Box_Type_B'])
    # StackableType.register_stackable_type('Type_A', ['HU', 'U'])
    # print(StackableType.get_stackable_type('Type_A'))


if __name__ == '__main__':
    main()
