import os
import matplotlib.pyplot as plt
import numpy as np
import shapefile


def parse_and_plot_coastline():

    ROOT_DIR = os.path.dirname(__file__)

    shp_file = os.path.join(ROOT_DIR,
                            'us_medium_shoreline.shp')

    test = shapefile.Reader(shp_file)
    all_y = []
    all_x = []
    for shape in test.shapeRecords():
        xy = [i for i in shape.shape.points[:]]
        coast_x, coast_y = zip(*[(j[0], j[1]) for j in xy])
        all_x += list(coast_x)
        all_y += list(coast_y)
        plt.plot(coast_x, coast_y, 'k')

    np.savetxt(os.path.join(ROOT_DIR,
                            'coastline.txt'),
               np.transpose(np.array(np.array([all_x, all_y]))))