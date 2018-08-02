import os
import csv


# Read lines as a list from the specified file
def list_file_reader(file_path):
    file = open(file_path, 'r')
    list = []
    line = file.readline()
    while line:
        list.append(line.strip('\r\n'))
        line = file.readline()
    file.close()
    return list


# Save simple list into file
def list_file_writer(list,save_path):
    create_parent_dir_not_exist(save_path)
    file = open(save_path, 'w+')
    for item in list:
        file.write(str(item)+"\n")
    file.close()


# Save map to file, the value of the map is a list
def list_map_writer(map, save_path, separator):
    create_parent_dir_not_exist(save_path)
    file = open(save_path, 'w+')
    keys = map.keys()
    for key in keys:
        line = key + ","
        items = map[key]
        for item in items:
            line += str(item) + separator
        file.write(line[0:len(line)-1] + "\n")
    file.close()


# Map reader
def list_map_reader(file_path, col_num, separator):
    map = {}
    file = open(file_path, 'r')
    line = file.readline()
    while line:
        line = line.strip('\r\n')
        items = line.split(separator)
        if len(items) == col_num:
            list = []
            for i in range(1, len(items)):
                list.append(items[i])
            map[items[0]] = list
        else:
            print "format not valid: " + line
        line = file.readline()
    file.close()
    return map


# Map reader
def list_map_reader(file_path, col_num, separator):
    map = {}
    file = open(file_path, 'r')
    line = file.readline()
    while line:
        line = line.strip('\r\n')
        items = line.split(separator)
        if len(items) == col_num:
            list = []
            for i in range(1, len(items)):
                list.append(items[i])
            map[items[0]] = list
        else:
            print "format not valid: " + line
        line = file.readline()
    file.close()
    return map


# map reader from csv file
def csv_map_reader(file_path):
    map = {}
    csvFile = open(file_path, "r")
    reader = csv.reader(csvFile)
    for cells in reader:
        if len(cells) == 2:
            map[cells[0]] = float(cells[1])
    csvFile.close()
    return map


# Read climate data from the csv file
def climate_data_reader(file_path):
    date_map = {}
    csvFile = open(file_path, "r")
    reader = csv.reader(csvFile)
    for cells in reader:
        if len(cells) == 9:
            # if cells[0] in date_map:
            #     print cells[0] + " repeated"
            items = []
            for i in range(2, 8):
                items.append(float(cells[i]))
            date_map[cells[0]] = items
    csvFile.close()
    return date_map


# Read flow data from the csv file
def flow_data_reader(file_path, station_code):
    flow_date_map = {}
    csvFile = open(file_path, "r")
    reader = csv.reader(csvFile)
    for cells in reader:
        if len(cells) == 3 and cells[0] == station_code:
            flow_date_map[cells[1]] = float(cells[2])
    csvFile.close()
    return flow_date_map


# normalize the flow map data
def normalize_flow_map(flow_date_map, max_min):
    keys = flow_date_map.keys()
    for key in keys:
        flow_date_map[key] = (flow_date_map[key]- max_min[1])/ max_min[2]
    return flow_date_map


# renormalize the flow data
def renormalize_flow(predict_value, max_min):
    ren_predict_value = []
    for value in predict_value:
        ren_predict_value.append(max_min[2]*value +max_min[1])
    return ren_predict_value


# get max, min and max-min
def get_max_min(list):
    max_min = [0, 0, 0]
    for item in list:
        if max_min[0] < item:
            max_min[0] = item
        if max_min[1] > item:
            max_min[1] = item
    max_min[2] = max_min[0] - max_min[1]
    return max_min


    # Get files in the specified directory
def files_in_directory(dir):
    import os
    file_names = []
    walk = os.walk(dir)
    for path, dir_list, file_list in walk:
        for file_name in file_list:
            file_names.append(os.path.join(path, file_name))
    return file_names


# Create file if not exist
def create_parent_dir_not_exist(file_path):
    parent_dir = os.path.dirname(file_path)
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)