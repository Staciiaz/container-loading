class Container:
    def __init__(self, volume):
        self.volume = volume
        self.stacking_list = []
        self.used_volume = 0

    def __str__(self):
        return '[{0}]'.format(' '.join(self.stacking_list))

    @property
    def available_volume(self):
        return self.volume - self.used_volume

    def use(self, stacking):
        if stacking.volume_2d < self.available_volume:
            self.stacking_list.append(stacking.type_id)
            self.used_volume += stacking.volume_2d
