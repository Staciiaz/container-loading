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
    def available_volume(self):
        return self.volume - self.used_volume

    @property
    def available_volume_ratio(self):
        return self.available_volume / self.volume

    def is_valid_for(self, stacking):
        return self.available_volume >= stacking.width and (not self.length or self.length == stacking.length)

    def append(self, stacking):
        if self.is_valid_for(stacking):
            self.stacking_list.append(stacking)
            self.used_volume += stacking.width
            if not self.length:
                self.length = stacking.length


class Container:
    def __init__(self, volume, height_limit):
        self.volume = volume
        self.height_limit = height_limit
        self.sections = []
        self.used_volume = 0

    def __str__(self):
        container_representation = str()
        container_representation += 'Used Volume: {0} / {1} ({2:.4f}%)\n'.format(self.used_volume, self.volume, self.used_volume_ratio * 100)
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

    def is_valid_for(self, section):
        return self.available_volume >= section.length and self.height_limit >= section.height

    def append(self, section):
        if section.length < self.available_volume:
            self.sections.append(section)
            self.used_volume += section.length
