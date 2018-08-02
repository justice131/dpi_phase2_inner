import tools

# formate txt into csv file
# one txt to one csv
def txt_to_csv_121(dir, save_dir):
    files = tools.files_in_directory(dir)
    for file in files:
        list = []
        lines = tools.list_file_reader(file)
        for i in range(2, len(lines)):
            items1 = lines[i].split(" ")
            items2 = []
            for item in items1:
                item = item.replace(" ","")
                if len(item) > 0 :
                    items2.append(item)
            if len(items2) == 8:
                line = ""
                for item in items2:
                    line += item +","
                list.append(line)
        file_name = file[(file.rfind("\\") + 1):file.rfind(".txt")]
        tools.list_file_writer(list, save_dir + "/" + file_name + ".csv")


# formate txt into csv file
# all txts to one csv file
def txt_to_csv_all(dir, save_path):
    files = tools.files_in_directory(dir)
    list = []
    for file in files:
        lines = tools.list_file_reader(file)
        for i in len(2, len(lines)):
            items1 = lines[i].split(" ")
            items2 = []
            for item in items1:
                item = item.replace(" ", "")
                if len(item) > 0:
                    items2.append(item)
            if len(items2) == 8:
                line = ""
                for item in items2:
                    line += item + ","
                list.append(line)
    tools.list_file_writer(list, save_path)


# Main function
if __name__ == '__main__':
    base_dir = "F:\Projects\Cooperation\DPI\Project2\Data\FlowData_Rooban_20180720\Flow_prediction"
    dir = base_dir+ "/" + "Climate_data"
    save_dir = base_dir+ "/" + "Climate_data_csv"
    txt_to_csv_121(dir, save_dir)