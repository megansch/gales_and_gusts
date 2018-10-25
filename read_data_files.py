import numpy as np
import os
import pandas as pd
from datetime import datetime

dict_na_values = {'Wind(WMO': -1,
                  'Pressure(WMO)': -1}


def get_time(time_str):
    dt_object = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    day_of_year = (dt_object - datetime(dt_object.year, 1, 1)).days
    time_of_day = dt_object.hour

    return time_of_day, day_of_year


def format_train_df(hurricane_name, size, latitude, longitude, wind,
                    pressure, time_string, ocean, hemisphere):
    df_all_data = pd.DataFrame()
    for index in np.arange(size - 2):

        if (latitude.size < (index + 1) or longitude.size < (index + 1) or
                wind.size < (index + 1) or pressure.size < (index + 1)):
            print('oops')
        if (np.isnan(latitude[index]) or np.isnan(latitude[index + 1]) or
                np.isnan(longitude[index]) or np.isnan(longitude[index + 1]) or
                np.isnan(wind[index]) or np.isnan(wind[index + 1]) or
                np.isnan(pressure[index]) or np.isnan(pressure[index + 1])):
            continue
        tod0, doy0 = get_time(time_string[index])
        tod1, doy1 = get_time(time_string[index + 1])
        tod2, doy2 = get_time(time_string[index + 2])

        df_data = pd.DataFrame.from_records([{'Name': hurricane_name,
                                              'Day_i-1': doy0,
                                              'Time_i-1': tod0,
                                              'Day_i': doy1,
                                              'Time_i': tod1,
                                              'Day_i+1': doy2,
                                              'Time_i+1': tod2,
                                              'Lat_i-1': latitude[index],
                                              'Lat_i': latitude[index + 1],
                                              'Lat_i+1': latitude[index + 2],
                                              'Long_i-1': longitude[index],
                                              'Long_i': longitude[index + 1],
                                              'Long_i+1': longitude[index + 2],
                                              'Hemisphere': hemisphere,
                                              'Ocean': ocean}],
                                            index='Name')
        df_all_data = df_all_data.append(df_data)

    return df_all_data


def read_data(data_dir, all):
    train_data_files = os.listdir(os.path.join(data_dir))

    df_all_data = pd.DataFrame()
    number_read = 0
    for file in train_data_files:
        print('{} files left to train.'.format((len(train_data_files) - number_read)))
        number_read += 1
        if number_read > 10 and not all:
            break

        df_read = pd.read_csv(os.path.join(data_dir,
                                           file),
                              sep=',',
                              skiprows=[0, 2],
                              na_values=dict_na_values)
        basin = df_read['Basin'][0].strip()
        if basin[0] == 'N':
            hemisphere = 1
        elif basin[0] == 'S':
            hemisphere = -1
        elif basin[0] == 'W' or basin[0] == 'E':
            hemisphere = 0
        else:
            hemisphere = 0

        if basin[1] == 'A':
            ocean = 1
        elif basin[1] == 'P':
            ocean = 2
        elif basin[1] == 'I':
            ocean = 3
        else:
            ocean = 0

        df_returned = format_train_df(df_read['Name'][0],
                                           df_read.index.size,
                                           df_read['Latitude'],
                                           df_read['Longitude'],
                                           df_read['Wind(WMO)'],
                                           df_read['Pres(WMO)'],
                                           df_read['ISO_time'],
                                           ocean,
                                           hemisphere)
        df_all_data = df_all_data.append(df_returned)

    return df_all_data


def read_test_data(data_dir):
    test_data_files = os.listdir(os.path.join(data_dir))

    df_all_data = pd.DataFrame()
    for file in test_data_files:
        df_read = pd.read_csv(os.path.join(data_dir,
                                           file),
                              sep=',',
                              skiprows=[0, 2],
                              na_values=dict_na_values)
        basin = df_read['Basin'][0].strip()
        if basin[0] == 'N':
            hemisphere = 1
        elif basin[0] == 'S':
            hemisphere = -1
        elif basin[0] == 'W' or basin[0] == 'E':
            hemisphere = 0
        else:
            hemisphere = 0

        if basin[1] == 'A':
            ocean = 1
        elif basin[1] == 'P':
            ocean = 2
        elif basin[1] == 'I':
            ocean = 3
        else:
            ocean = 0
        hurricane_name = df_read['Name'][0]
        time_string = df_read['ISO_time']
        latitude = df_read['Latitude']
        longitude = df_read['Longitude']

        df_data = pd.DataFrame.from_records([{'Name': hurricane_name,
                                              'Time': [time_string],
                                              'Lat': [latitude],
                                              'Long': [longitude],
                                              'Hemisphere': hemisphere,
                                              'Ocean': ocean}],
                                            index='Name')
        df_all_data = df_all_data.append(df_data)

    return df_all_data
