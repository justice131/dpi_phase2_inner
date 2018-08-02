import model_io
import tools
import models
import os

# predict using all existing flow data
def predict_flow_directly(climate_station_ids, flow_station_code,
    water_source_id, climate_data_dir, flow_data_path, my_model_dir, regressor):
    # initiate the climate data
    postfix = water_source_id + "_" + flow_station_code +".csv"
    average_climate_path = my_model_dir + "/average_climate/average_climate_" + postfix
    predicted_flow_path = my_model_dir + "/predicted_results/" + regressor + "_" + postfix

    if os.path.exists(average_climate_path):
        climate_date_map = tools.list_map_reader(average_climate_path, 7, ",")
    else:
        climate_date_map = model_io.average_climate_data(climate_station_ids, climate_data_dir)
        tools.list_map_writer(climate_date_map, average_climate_path, ",")

    # initiate the flow data
    flow_date_map = tools.flow_data_reader(flow_data_path, flow_station_code)
    max_min = tools.get_max_min(flow_date_map.values())
    flow_date_map = tools.normalize_flow_map(flow_date_map, max_min)

    flow_keys = flow_date_map.keys()
    climate_keys = climate_date_map.keys()
    common_keys = []
    climate_only_keys = []

    for date in climate_keys:
        if date in flow_keys:
            common_keys.append(date)
        else:
            climate_only_keys.append(date)

    # initiate the training and test set
    train_x = []
    train_y = []
    for date in common_keys:
        train_x.append(climate_date_map[date])
        train_y.append(flow_date_map[date])
    test_x = []
    for date in climate_only_keys:
        test_x.append(climate_date_map[date])

    # cross_validation performance validation
    RMSE = model_performance_cv(train_x, train_y, max_min, regressor)
    print "water_source_id=" + water_source_id + ", regressor=" + regressor + ", RMSE: " + str(RMSE)

    # train and test
    model = models.regressor(train_x, train_y, regressor)
    predict_y = model.predict(test_x)
    predict_y = tools.renormalize_flow(predict_y, max_min)
    train_y = tools.renormalize_flow(train_y, max_min)
    result = model_io.merge_sort_result(climate_only_keys, predict_y, common_keys, train_y)
    tools.list_file_writer(result, predicted_flow_path)


# predict using existing flow data minus input flows
def predict_flow_minus(climate_station_ids, flow_station_code, water_source_id,
    climate_data_dir, flow_data_path, my_model_dir, minus_flow_station_codes, regressor):
    # initiate the climate data
    postfix = water_source_id + "_" + flow_station_code + ".csv"
    average_climate_path = my_model_dir + "/average_climate/average_climate_" + postfix
    predicted_flow_path = my_model_dir + "/predicted_results/" + regressor + "_" + postfix
    if os.path.exists(average_climate_path):
        climate_date_map = tools.list_map_reader(average_climate_path, 7, ",")
    else:
        climate_date_map = model_io.average_climate_data(climate_station_ids, climate_data_dir)
        tools.list_map_writer(climate_date_map, average_climate_path, ",")

    # initiate the flow data
    ori_flow_date_map = tools.flow_data_reader(flow_data_path, flow_station_code)
    all_predicted_flows = tools.files_in_directory(my_model_dir + "/predicted_results") # get all predicted results
    minus_flow_date_maps = []

    # initiate flow data for the minus flow stations
    for mfsc in minus_flow_station_codes:
        flow_path = False
        for apf in all_predicted_flows:
            if apf.endswith("_"+mfsc+".csv"):
                flow_path = apf
                break
        if flow_path:
            minus_flow_date_map = tools.csv_map_reader(flow_path)
        else:
            print "minus_flow_station_code=" + mfsc + " not found in predited result"
            minus_flow_date_map = tools.flow_data_reader(flow_data_path, mfsc)
        minus_flow_date_maps.append(minus_flow_date_map)

    # original flow minus minus flows
    ori_flow_keys = ori_flow_date_map.keys()
    processed_flow_date_map = {}
    for key in ori_flow_keys:
        flag = True
        for minus_flow_date_map in minus_flow_date_maps:
            if not key in minus_flow_date_map:
                flag = False
        if flag:
            processed_flow_date_map[key] = ori_flow_date_map[key]
            for minus_flow_date_map in minus_flow_date_maps:
                processed_flow_date_map[key] -= minus_flow_date_map[key]
    max_min = tools.get_max_min(processed_flow_date_map.values())
    processed_flow_date_map = tools.normalize_flow_map(processed_flow_date_map, max_min)

    flow_keys = processed_flow_date_map.keys()
    climate_keys = climate_date_map.keys()
    common_keys = []
    climate_only_keys = []

    for date in climate_keys:
        if date in flow_keys:
            common_keys.append(date)
        else:
            climate_only_keys.append(date)

    # initiate the training and test set
    train_x = []
    train_y = []
    for date in common_keys:
        train_x.append(climate_date_map[date])
        train_y.append(processed_flow_date_map[date])
    test_x = []
    for date in climate_only_keys:
        test_x.append(climate_date_map[date])

    # cross_validation performance validation
    RMSE = model_performance_cv(train_x, train_y, max_min, regressor)
    print "water_source_id=" + water_source_id + ", regressor="+ regressor + ", RMSE: " + str(RMSE)

    # train and test
    model = models.regressor(train_x, train_y, regressor)
    predict_y = model.predict(test_x)
    predict_y = tools.renormalize_flow(predict_y, max_min)
    result = model_io.merge_sort_result(climate_only_keys, predict_y, common_keys, train_y)
    tools.list_file_writer(result, predicted_flow_path)


# validate the performance using cross_validations
def model_performance_cv(train_x, train_y, max_min, regressor):
    from sklearn.model_selection import KFold  # import KFold
    import numpy as np
    import math
    sample_len = len(train_y)

    train_x = np.array(train_x)
    train_y = np.array(train_y)

    kf = KFold(n_splits=5)  # Define the split - into 5 folds
    kf.get_n_splits(train_x)  # returns the number of splitting iterations in the cross-validator
    RMSE = 0
    for train_index, test_index in kf.split(train_x):
        x_train, x_test = train_x[train_index], train_x[test_index]
        y_train, y_test = train_y[train_index], train_y[test_index]

        model = models.regressor(x_train, y_train, regressor)
        y_predict = model.predict(x_test)
        y_predict = tools.renormalize_flow(y_predict, max_min)
        y_test = tools.renormalize_flow(y_test, max_min)
        for i in range(0, len(y_predict)):
            RMSE += pow((y_predict[i] - y_test[i]), 2)
    RMSE = math.sqrt((RMSE/sample_len))
    return RMSE


# Main function
if __name__ == '__main__':
    base_dir = "F:/Projects/Cooperation/DPI/Project2/Data/FlowData_Rooban_20180720/Flow_prediction/"
    climate_data_dir = base_dir + "Climate_data_csv"
    flow_data_path = base_dir + "Flow_data/merge_manning_flow_data.csv"
    my_model_dir = base_dir + "my_model"
    # regressors = ["random_forest", "linear", "adaboost", "svr_lin"]
    regressors = ["random_forest"]
    for regressor in regressors:
        # water_source_id = "1"
        # flow_station_code = "208027"
        # climate_station_ids = [42,43,59,60,61,62,77,78,79,80,95,96,97,98,112,113,114,115,116,117,132,133,134,151]
        # predict_flow_directly(climate_station_ids, flow_station_code, water_source_id, climate_data_dir, flow_data_path, my_model_dir, regressor)
        #
        # water_source_id = "2"
        # flow_station_code = "208026"
        # climate_station_ids = [129,130,131,147,148,149,150,165,166,167,168,169,185,186,187,203,204,205,222,223,241]
        # predict_flow_directly(climate_station_ids, flow_station_code, water_source_id, climate_data_dir, flow_data_path, my_model_dir, regressor)
        #
        # water_source_id = "3"
        # flow_station_code = "208011"
        # minus_flow_station_codes = ["208027", "208026"]
        # climate_station_ids = [135,136,152,153,170,171,172,188,189,190,206,207,208,224,225,226,242,243,244,261,262,279,280,298]
        # predict_flow_minus(climate_station_ids, flow_station_code, water_source_id,climate_data_dir, flow_data_path, my_model_dir, minus_flow_station_codes, regressor)
        #
        # water_source_id = "4"
        # flow_station_code = "208005"
        # climate_station_ids = [183,184,200,201,202,220,221,240,259,260,278,296,297,315,333,352,353,370,371,218,219,236,237,238,239,
        #                        254,255,256,257,258,271,272,273,274,275,276,277,291,292,293,294,295,311,312,313,314,332,290,307,308,
        #                        309,310,326,327,328,329,330,331,345,346,347,348,349,350,351,363,364,365,366,367,368,369,383,384,385,386,]
        # predict_flow_directly(climate_station_ids, flow_station_code, water_source_id, climate_data_dir, flow_data_path,
        #                       my_model_dir, regressor)

        # water_source_id = "5"
        # flow_station_code = "208029"
        # climate_station_ids = [137,154,155,156,173,174,191,192,209,210,227,228,245,246,263,264,281,282,299,300]
        # predict_flow_directly(climate_station_ids, flow_station_code, water_source_id, climate_data_dir, flow_data_path, my_model_dir, regressor)

        # water_source_id = "6" # cannot predict, climate data end 20100322, flow data starts 20100904
        # flow_station_code = "208031"
        # climate_station_ids = [140,142,157,158,159,160,175,176,177,178,193,194,195,196,211,212,213,229,230,231,248,249,267,247,265,266,283,284,301,319,320]
        # predict_flow_directly(climate_station_ids, flow_station_code, water_source_id, climate_data_dir, flow_data_path, my_model_dir, regressor)

        # water_source_id = "7"
        # flow_station_code = "208020"
        # climate_station_ids = [197,214,215,232,250,268,269,270,287,304,305,321,322,285,286,302,303]
        # predict_flow_directly(climate_station_ids, flow_station_code, water_source_id, climate_data_dir, flow_data_path, my_model_dir, regressor)
        #
        # water_source_id = "8"
        # flow_station_code = "208003"
        # climate_station_ids = [140,142,157,158,159,160,175,176,177,178,193,194,195,196,211,212,213,229,230,231,248,249,267,247,265,266,
        #                        283,284,301,319,320,270,288,306,323,324,339,340,341,358,359,360,378,337,338,355,356,357,373,197,214,215,
        #                        232,250,268,269,270,287,304,305,321,322,285,286,302,303]
        # predict_flow_directly(climate_station_ids, flow_station_code, water_source_id, climate_data_dir, flow_data_path, my_model_dir, regressor)
        #
        # water_source_id = "10"
        # flow_station_code = "208004"
        # minus_flow_station_codes = ["208011", "208029", "208005", "208003"]
        # climate_station_ids = [372,374,375,376,390,391,392,393,408,409,410,427,428,429,445,446,447,463,464,465,483]
        # predict_flow_minus(climate_station_ids, flow_station_code, water_source_id, climate_data_dir, flow_data_path, my_model_dir, minus_flow_station_codes, regressor)

        # water_source_id = "11" # cannot predict, climate data end 20100322, flow data starts 20100904
        # flow_station_code = "208032"
        # climate_station_ids = [386,387,388,389,404,405,406,407,422,423,424,425,426,440,441,442,443,444,445,458,459,476]
        # predict_flow_directly(climate_station_ids, flow_station_code, water_source_id, climate_data_dir, flow_data_path, my_model_dir, regressor)

        water_source_id = "12" # cannot predict, due to 11
        flow_station_code = "208410"
        minus_flow_station_codes = ["208032", "208004"]
        climate_station_ids = [460,461,462,477,478,479,480,481,482,494,495,496,497,498,499,500,513,514,515,516,517,518,533,534,535,536,550,551,552,553,554,568,569,570,571,587,588]
        predict_flow_minus(climate_station_ids, flow_station_code, water_source_id, climate_data_dir, flow_data_path, my_model_dir, minus_flow_station_codes, regressor)