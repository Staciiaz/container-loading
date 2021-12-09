from stacking import Stacking
from container import Container, ContainerSection
import math


class Processor:
    def __init__(self):
        self.__boxes = dict()
        self.__stacking = dict()
        self.__sections = list()
        self.__containers = list()

    @property
    def remaining_boxes(self):
        return dict(self.__boxes)

    @property
    def remaining_sections(self):
        return list(self.__sections)

    def update(self, boxes):
        self.__boxes.update(boxes)

    def clear(self):
        self.__boxes.clear()
        self.__stacking.clear()
        self.__sections.clear()
        self.__containers.clear()

    def remove_boxes(self, box_type, amount):
        self.__boxes[box_type] -= amount
        if self.__boxes[box_type] <= 0:
            self.__boxes.pop(box_type)
        return box_type in self.__boxes

    def calculate_stacking(self):
        for stacking in Stacking.get_all():
            if min([0 if x not in self.__boxes else self.__boxes[x] for x in stacking.boxes]) > 0:
                stacking_amount = min([self.__boxes[x] // stacking.boxes[x] for x in stacking.boxes])
                if stacking_amount > 0:
                    self.__stacking[stacking.type_id] = stacking_amount
                    [self.remove_boxes(x, stacking_amount * stacking.boxes[x]) for x in stacking.boxes]
        return self.__stacking

    def __calculate_section(self):
        section_volume = 237
        for stacking_type, stacking_amount in sorted(self.__stacking.items(), key=lambda x: Stacking.get(x[0]).volume_2d, reverse=True):
            stacking = Stacking.get(stacking_type)
            for _ in range(stacking_amount):
                valid_sections = [x for x in self.__sections if x.is_valid_for(stacking)]
                best_fit_sections = min(valid_sections, key=lambda x: x.available_volume, default=None)
                if best_fit_sections:
                    best_fit_sections.append(stacking)
                else:
                    section = ContainerSection(section_volume)
                    section.append(stacking)
                    self.__sections.append(section)
        self.__stacking.clear()
        return self.__sections

    def calculate_container(self, include_bad_section=False):
        self.__calculate_section()
        # Large container volume = [ 237 * 1200 * 240 ]
        # Small container volume = [ 237 * 590 * 224 ]
        container_volume = 1200
        height_limit = 240
        sections = sorted([x for x in self.__sections if x.used_volume_ratio >= 0.9], reverse=True)
        if include_bad_section:
            bad_sections = sorted([x for x in self.__sections if x.used_volume_ratio < 0.9], reverse=True)
            sections.extend(bad_sections)
        for section in sections:
            if section.height <= height_limit:
                valid_containers = [x for x in self.__containers if x.is_valid_for(section)]
                best_fit_containers = min(valid_containers, key=lambda x: x.available_volume, default=None)
                if best_fit_containers:
                    best_fit_containers.append(section)
                else:
                    container = Container(container_volume, height_limit)
                    container.append(section)
                    self.__containers.append(container)
                self.__sections.remove(section)
        return self.__containers
