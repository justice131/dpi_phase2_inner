import tools

# average the climate data in a specified area(water source)
def average_climate_data(climate_station_ids, climate_data_dir):
    map_container = []
    unique_date_list = set()
    for gsi in climate_station_ids:
        climate_data_path = climate_data_dir + "/" + str(gsi) + ".csv"
        date_map = tools.climate_data_reader(climate_data_path)
        map_container.append(date_map)
        date_list = date_map.keys()
        for date in date_list:
            unique_date_list.add(date)

    average_date_map = {}
    for date in unique_date_list:
        averages = [0, 0, 0, 0, 0, 0]
        valid_num = 0
        for date_map in map_container:
            if date_map.__contains__(date):
                items = date_map[date]
                valid_num += 1
                for i in range(0, 6):
                    averages[i] += items[i]
        for i in range(0, 6):
            averages[i] = averages[i]/valid_num
        average_date_map[date] = averages
    return average_date_map


# merge and sort the prediction result
def merge_sort_result(test_date, predict_y, train_date, train_y):
    train_date.extend(test_date)
    train_y.extend(predict_y)
    result_len = len(train_y)
    # for i in range(0, result_len-1):
    #     for j in range(0, result_len-1-i):
    #         if train_x[j] > train_x[j+1] :
    #             temp1 = train_x[j]
    #             train_x[j] = train_x[j+1]
    #             train_x[j + 1] = temp1
    #
    #             temp2 = train_y[j]
    #             train_y[j] = train_y[j + 1]
    #             train_y[j + 1] = temp2
    result_list = []
    for i in range(0, result_len):
        result_list.append(str(train_date[i]) + "," +str(train_y[i]))
    return result_list

