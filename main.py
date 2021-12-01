from optimize_finding import Container, process


def main():
    input_boxes = {
        'HU': 2,
        'U': 3,
        'MU': 0
    }
    box_types = {
        'HU': [76, 112, 109],
        'U': [76, 112, 73],
        'MU': [76, 112, 54],
        '2HUL': [110, 180, 109],
        '2UL': [110, 180, 73],
        'WUL01': [1515, 2220, 85],
        'WUL03': [1515, 2220, 73]
    }
    Container.stackable_types = {
        'Stack_HU': [['HU'], ['HU']],
        'Stack_U': [['U'], ['U'], ['U']],
        'Stack_MU': [['MU'], ['MU'], ['MU'], ['MU']],
        'Stack_2HUL': [['2HUL'], ['2HUL']],
        'Stack_2UL': [['2UL'], ['2UL'], ['2UL']],
        'Stack_WUL03': [['WUL03'], ['WUL03'], ['WUL03']],
        'Mix_1': [['M'], ['M'], ['HU']],
        'Mix_5': [['HU', 'HU', 'HU'], ['2HUL']],
        'Mix_6': [['U', 'U', 'U'], ['U', 'U', 'U'], ['2UL']],
        'Mix_7': [['WUL01'], ['WUL03'], ['WUL03']],
        'Mix_8': [['MU', 'MU', 'MU'], ['MU', 'MU', 'MU'], ['2HUL']]
    }
    process(input_boxes)


if __name__ == '__main__':
    main()
