import os


def read_input(file_name):
    data_dict = dict()
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            for line in file:
                data = line.replace('\n', '').split(' ')
                data_dict[data[0]] = int(data[1])
    return data_dict
