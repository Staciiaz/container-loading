class ContainerSection:
    def __init__(self, volume):
        self.volume = volume
        self.stacking_list = []
        self.used_volume = 0
        self.length = None

    def __str__(self):
        stacking_list = [x.type_id for x in self.stacking_list]
        return '[{0}]'.format(' '.join(stacking_list))

    def __repr__(self):
        stacking_list = [x.type_id for x in self.stacking_list]
        return '(used_volume={0}, length={1}, stacking_list=[{2}])'.format(self.used_volume, self.length, ' '.join(stacking_list))

    def __lt__(self, other):
        if len(self.stacking_list) != len(other.stacking_list):
            return len(self.stacking_list) > len(other.stacking_list)
        elif self.length != other.length:
            return self.length < other.length
        else:
            return False

    @property
    def height(self):
        return max([x.height for x in self.stacking_list])

    @property
    def used_volume_ratio(self):
        return self.used_volume / self.volume

    @property
    def available_volume(self):
        return self.volume - self.used_volume

    @property
    def available_volume_ratio(self):
        return self.available_volume / self.volume

    @property
    def used_boxes(self):
        used_boxes = dict()
        for stacking in self.stacking_list:
            for box_type, box_amount in stacking.boxes.items():
                if box_type not in used_boxes:
                    used_boxes[box_type] = 0
                used_boxes[box_type] += box_amount
        return used_boxes

    def is_valid_for(self, stacking):
        return self.available_volume >= stacking.width and (not self.length or self.length == stacking.length)

    def append(self, stacking):
        if self.is_valid_for(stacking):
            self.stacking_list.append(stacking)
            self.used_volume += stacking.width
            if not self.length:
                self.length = stacking.length


class Container:
    width = 237

    def __init__(self, volume, height_limit):
        self.volume = volume
        self.height_limit = height_limit
        self.sections = []
        self.used_volume = 0

    def __str__(self):
        return '{}'.format(self.sections)

    def __repr__(self):
        return '(used_volume={}, sections={})'.format(self.used_volume, self.sections)

    @property
    def volume_2d(self):
        return self.volume * Container.width

    @property
    def representation(self):
        container_representation = str()
        container_representation += 'Used volume: {:.2f}%, Box used: {}\n'.format(self.used_volume_2d_ratio * 100, self.used_boxes)
        for section in self.sections:
            container_representation += '{}\n'.format(str(section))
        return container_representation

    @property
    def used_volume_ratio(self):
        return self.used_volume / self.volume

    @property
    def available_volume(self):
        return self.volume - self.used_volume

    @property
    def available_volume_ratio(self):
        return self.available_volume / self.volume

    @property
    def used_volume_2d(self):
        return self.used_volume * Container.width - sum([x.available_volume * x.length for x in self.sections])

    @property
    def used_volume_2d_ratio(self):
        return self.used_volume_2d / self.volume_2d

    @property
    def used_boxes(self):
        used_boxes = dict()
        for section in self.sections:
            for box_type, box_amount in section.used_boxes.items():
                if box_type not in used_boxes:
                    used_boxes[box_type] = 0
                used_boxes[box_type] += box_amount
        return used_boxes

    def is_valid_for(self, section):
        return self.available_volume >= section.length and self.height_limit >= section.height

    def append(self, section):
        if section.length < self.available_volume:
            self.sections.append(section)
            self.used_volume += section.length
