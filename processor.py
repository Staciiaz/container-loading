from stacking import Stacking
from container import Container, ContainerSection
import math


class Processor:
    def __init__(self):
        self.__stacking = dict()
        self.__sections = list()
        self.__containers = list()
        self.__remaining_boxes = dict()

    @property
    def remaining_boxes(self):
        return dict(self.__remaining_boxes)

    def update(self, boxes):
        self.__remaining_boxes.update(boxes)

    def clear(self):
        self.__stacking.clear()
        self.__sections.clear()
        self.__containers.clear()
        self.__remaining_boxes.clear()

    def remove_boxes(self, box_type, amount):
        self.__remaining_boxes[box_type] -= amount
        if self.__remaining_boxes[box_type] <= 0:
            self.__remaining_boxes.pop(box_type)
        return box_type in self.__remaining_boxes

    def calculate_stacking(self):
        for stacking in Stacking.get_all():
            if min([0 if x not in self.__remaining_boxes else self.__remaining_boxes[x] for x in stacking.boxes]) > 0:
                stacking_amount = min([self.__remaining_boxes[x] // stacking.boxes[x] for x in stacking.boxes])
                if stacking_amount > 0:
                    self.__stacking[stacking.type_id] = stacking_amount
                    [self.remove_boxes(x, stacking_amount * stacking.boxes[x]) for x in stacking.boxes]
        return self.__stacking

    def __calculate_section(self):
        section_volume = 237  # Container volume = [ 237 * 1200 * 240 ]
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
        return self.__sections

    def calculate_container(self, include_bad_section=False):
        self.__calculate_section()
        container_volume = 1200  # Container volume = [ 237 * 1200 * 240 ]
        sections = sorted([x for x in self.__sections if x.available_volume_ratio < 0.5], reverse=True)
        if include_bad_section:
            bad_sections = sorted([x for x in self.__sections if x.available_volume_ratio >= 0.5], reverse=True)
            sections.extend(bad_sections)
        for section in sections:
            valid_containers = [x for x in self.__containers if x.available_volume >= section.length]
            best_fit_containers = min(valid_containers, key=lambda x: x.available_volume, default=None)
            if best_fit_containers:
                best_fit_containers.append(section)
            else:
                container = Container(container_volume)
                container.append(section)
                self.__containers.append(container)
            self.__sections.remove(section)
        return self.__containers
