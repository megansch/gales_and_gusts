import os
from ftplib import FTP

ROOT_DIR = os.path.dirname(__file__)

train_dir = os.path.join(ROOT_DIR,
                         'data',
                         'Train')

ftp = FTP('eclipse.ncdc.noaa.gov')
ftp.login()
ftp.cwd('pub/ibtracs/v03r09/wmo/csv/storm/')

files = ftp.nlst()

for file in files:
    year = int(file[6:10])
    if year == 2016 or year < 2000:
        continue
    destination = os.path.join(train_dir,
                               file)
    lf = open(destination, "wb")
    ftp.retrbinary("RETR " + file, lf.write, 8*1024)
    lf.close()
    print('file')

print('Here')