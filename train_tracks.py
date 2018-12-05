import os
import argparse
import pandas as pd
from read_coastline import parse_and_plot_coastline
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
import pickle
from read_data_files import read_data
from test_tracks import test_them


def train_tracks(train_dir, all):

    model_name = '2000_2014_Linear_train_2_predict_3rd'

    df_train_data = read_data(train_dir, all)
    
    kmeans_model = KMeans(n_clusters=5, random_state=1)
    good_columns = df_train_data._get_numeric_data()
    kmeans_model.fit(good_columns)
    labels = kmeans_model.labels_
    
    pca_2 = PCA(2)
    plot_columns = pca_2.fit_transform(good_columns)

    target_lat = 'Lat_i+1'
    target_lon = 'Long_i+1'
    corrs_lat = df_train_data.corr()[target_lat]
    corrs_lon = df_train_data.corr()[target_lon]

    columns = df_train_data.columns.tolist()
    columns = [c for c in columns if c not in [target_lat, target_lon]]

    model_lat = LinearRegression()
    model_lat.fit(df_train_data[columns], df_train_data[target_lat])

    model_lon = LinearRegression()
    model_lon.fit(df_train_data[columns], df_train_data[target_lon])

    model_lon_file_name = os.path.join(ROOT_DIR,
                                   '{}_lon.sav'.format(model_name))
    model_lat_file_name = os.path.join(ROOT_DIR,
                                   '{}_lat.sav'.format(model_name))
    pickle.dump(model_lon, open(model_lon_file_name, 'wb'))
    pickle.dump(model_lat, open(model_lat_file_name, 'wb'))

    test_them(model_lon, model_lat)



