import pandas as pd
import pickle
import os
from read_data_files import read_test_data
from read_data_files import get_time
import numpy as np
from matplotlib import pyplot as plt

ROOT_DIR = os.path.dirname(__file__)


def test_them(model_lon, model_lat):
    test_dir = os.path.join(ROOT_DIR,
                            'data',
                            'Test')

    # make directory for storing the plots
    plot_dir = os.path.join(ROOT_DIR, 'TestPredictions')
    if not os.path.isdir(plot_dir):
        os.mkdir(plot_dir)

    df_test_data = read_test_data(test_dir)

    target_lat = 'Lat_i+1'
    target_lon = 'Long_i+1'

    df_all_predictions = pd.DataFrame()
    for hurricane_name, row in df_test_data.iterrows():
        lat = []
        lon = []
        last_prediction_lon = row['Long'][0][0]
        last_prediction_lat = row['Lat'][0][0]
        prediction_lon = row['Long'][0][1]
        prediction_lat = row['Lat'][0][1]
        for index in np.arange(len(row['Time'][0]) - 2):
            tod0, doy0 = get_time(row['Time'][0][index])
            tod1, doy1 = get_time(row['Time'][0][index + 1])
            tod2, doy2 = get_time(row['Time'][0][index + 2])

            df_test_row = pd.DataFrame({'Name': hurricane_name,
                                        'Day_i-1': doy0,
                                        'Day_i': doy1,
                                        'Day_i+1': doy2,
                                        'Time_i-1': tod0,
                                        'Time_i': tod1,
                                        'Time_i+1': tod2,
                                        'Lat_i-1': last_prediction_lat,
                                        'Lat_i': prediction_lat,
                                        'Long_i-1': last_prediction_lon,
                                        'Long_i': prediction_lon,
                                        'Hemisphere': row['Hemisphere'],
                                        'Ocean': row['Ocean']},
                                       index=[hurricane_name])

            columns = df_test_row.columns.tolist()
            columns = [c for c in columns if c not in [target_lat, target_lon, 'Name']]
            last_prediction_lon = prediction_lon
            last_prediction_lat = prediction_lat
            prediction_lon = model_lon.predict(df_test_row[columns])
            prediction_lat = model_lat.predict(df_test_row[columns])

            lat.extend(prediction_lat)
            lon.extend(prediction_lon)

        df_prediction = pd.DataFrame({'Name': hurricane_name,
                                      'Time': [row['Time']],
                                      'Lat': [lat],
                                      'Long': [lon],
                                      'Hemisphere': row['Hemisphere'],
                                      'Ocean': row['Ocean']},
                                     dtype=object)
        plt.figure()
        plt.scatter(df_prediction['Lat'].values[0], df_prediction['Long'].values[0], label='Prediction')
        plt.scatter(row['Lat'], row['Long'], label='Real')
        plt.title(df_prediction['Name'][0])
        plt.legend()

        df_all_predictions.append(df_prediction)

        fig_name = os.path.join(plot_dir,
                                '{}.png'.format(df_prediction['Name'][0]))
        plt.savefig(fig_name)
        plt.close()


if __name__ == "__main__":
    model_name = '2000_2014_Linear_train_2_predict_3rd'

    model_lon_file_name = os.path.join(ROOT_DIR,
                                       '{}_lon.sav'.format(model_name))
    model_long = pickle.load(open(model_lon_file_name, 'rb'))

    model_lat_file_name = os.path.join(ROOT_DIR,
                                       '{}_lat.sav'.format(model_name))
    model_lati = pickle.load(open(model_lat_file_name, 'rb'))

    test_them(model_long, model_lati)
