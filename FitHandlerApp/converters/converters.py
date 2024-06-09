import csv
import fitparse
import pandas as pd
import os

all_headers = {
    "time_and_data": ["timestamp", "start_time", "total_elapsed_time", "total_timer_time"],
    "navigation": ["position_lat", "position_long", "gps_accuracy"],
    "distance_and_speed": ["distance", "enhanced_speed", "speed", "enhanced_avg_speed", "avg_speed",
                           "enhanced_max_speed", "max_speed", "total_distance", 'vertical_speed'],
    "gear": ["rear_gear_num", "rear_gear", "front_gear_num", "front_gear"],  # TODO
    "temperature": ["temperature", "avg_temperature", "max_temperature"],
    "cadence": ["cadence", "avg_cadence", "max_cadence"],
    "fitness_metrics": ["heart_rate", "calories", "min_heart_rate", "avg_heart_rate", "max_heart_rate",
                        "time_in_hr_zone",
                        "total_calories"],
    "height_and_slope": ["enhanced_altitude", "altitude", "grade", "enhanced_min_altitude", "min_altitude", "avg_grade",
                         "enhanced_avg_altitude", "avg_altitude", "enhanced_max_altitude", "max_altitude",
                         "max_neg_grade",
                         "max_pos_grade", "ascent", "descent", "total_ascent", "total_descent"],
    "tec_data": ["event", "event_type", "timer_trigger", "battery_soc", "data", 'vertical_speed'],

    "record_headers": ['timestamp', 'position_lat', 'position_long', 'gps_accuracy', 'distance', 'enhanced_speed',
                       'speed', 'enhanced_altitude', 'altitude', 'grade', 'battery_soc', 'ascent', 'descent',
                       'temperature',
                       'heart_rate', 'vertical_speed', 'calories', 'cadence']}

lap_headers = ['start_time', 'total_elapsed_time', 'total_timer_time', 'total_distance',
               'total_moving_time', 'total_calories', 'enhanced_avg_speed', 'avg_speed', 'enhanced_max_speed',
               'max_speed', 'total_ascent', 'total_descent', 'enhanced_avg_altitude', 'avg_altitude',
               'enhanced_max_altitude', 'max_altitude', 'avg_grade', 'max_pos_grade', 'max_neg_grade',
               'max_cadence', 'avg_cadence'
                              'enhanced_min_altitude', 'min_altitude', 'event', 'event_type', 'avg_heart_rate',
               'max_heart_rate',
               'lap_trigger', 'sport', 'sub_sport', 'avg_temperature', 'max_temperature', 'min_heart_rate',
               'unknown_124', 'time_in_hr_zone']

event_headers = ['timer_trigger', 'rear_gear_num', 'rear_gear', 'front_gear_num',
                 'front_gear', 'gear_change_data']


def convert_to_csv(file_path: str, file_name: str, headers_list: list):
    fit_data = fitparse.FitFile(file_path, data_processor=fitparse.StandardUnitsDataProcessor())
    data_for_record = []
    headers = []
    [headers.extend(all_headers.get(header)) for header in headers_list]
    string_counter = 0
    for record_data in fit_data.get_messages(['record', 'lap', 'event']):

        line_for_record = {}

        if record_data.name == 'record':
            string_counter += 1
            for key in record_data.get_values().keys():
                if key in headers:
                    line_for_record.update({key: record_data.get_values().get(key)})

        elif record_data.name == 'lap':
            for key in record_data.get_values().keys():
                if key in headers:
                    data_for_record[string_counter-1].update({key: record_data.get_values().get(key)})

        elif record_data.name == 'event':
            for key in record_data.get_values().keys():
                if key in headers:
                    if string_counter == 0:
                        continue
                    else:
                        data_for_record[string_counter-1].update({key: record_data.get_values().get(key)})
        if data_for_record != {}:
            data_for_record.append(line_for_record)

    with open(f'media/converted_files/{file_name[:-4]}.csv', 'w', newline='') as f:
        fieldnames = headers
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for line in data_for_record:
            timestamp = ''
            line_ = {}
            if timestamp == line_.get('timestamp'):
                continue
            timestamp = line_.get('timestamp')
            for key, value in line.items():
                line_.update({key: str(value).replace('None', '')})
            if line_ != {}:
                writer.writerow(line_)

    file = f'converted_files/{file_name[:-4]}.csv'
    return file


def convert_to_excel(file_path: str, file_name: str, ex_headers_list: list):
    fitfile = file_path
    fit_data = fitparse.FitFile(fitfile, data_processor=fitparse.StandardUnitsDataProcessor())
    headers = []
    print(ex_headers_list)
    for ex_header in ex_headers_list:

        a = all_headers.get(ex_header)
        headers.extend(a)
    # [headers.extend(all_headers.get(header)) for header in headers_list]
    print(headers)

    data_for_record = {key: [] for key in headers}

    for message in fit_data.get_messages(['lap', 'record', 'event']):
        for key in headers:
            data_for_record.get(key).append(message.get_values().get(key, ''))

    df = pd.DataFrame(data_for_record)
    file = f'converted_files/{file_name[:-4]}.xlsx'
    cwd = os.getcwd().replace(r'FitHandlerApp\converters', '')
    os.path.join(cwd, f'{file}.xlsx')
    df.to_excel(os.path.join(cwd, 'media', f'{file}'), index=False)
    return file



