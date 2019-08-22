from PIL import Image
from PIL.ExifTags import TAGS
import os
#import pandas as pd

def get_loc_cord(imgFileName):
    try:
        exifData = {}
        with Image.open(imgFileName) as imgFile:
            info = imgFile._getexif()
            if info:
                for item in info.items():
                    tag = item[0]
                    value = item[1]
                    decoded = TAGS.get(tag, tag)
                    exifData[decoded] = value
                    if 'GPSInfo' in exifData:
                        exifGPS = exifData['GPSInfo']
                        N1 = exifGPS[2][0][0]
                        N2 = exifGPS[2][1][0]
                        N3 = exifGPS[2][2][0] / exifGPS[2][2][1]
                        N = N1 + (N2 + N3/60)/60
                        E1 = exifGPS[4][0][0]
                        E2 = exifGPS[4][1][0]
                        E3 = exifGPS[4][2][0] / exifGPS[4][2][1]
                        E = E1 + (E2 + E3/60)/60
                        gps = str(E)+','+str(N)
                        return gps
                else:
                    print(imgFileName + ' NO exif GPS MetaData')
                    pass
    except:
        print(imgFileName + ' NO exif GPS MetaData')
        pass

photo_location = dict()

listfile=os.listdir(r'D:\workspace\birthday project\resource\photos')
for f in listfile:
    if f[-4:] == '.jpg':
        d = f[4:-4]
        nice_date = '%s-%s-%s %s:%s' %(d[0:4], d[4:6], d[6:8], d[9:11], d[11:13])
        if nice_date not in photo_location:
            gps = get_loc_cord(r'D:\workspace\birthday project\resource\photos\%s'%f)
            if gps:
                photo_location[nice_date] = gps

#print(photo_location)

file = open(r'D:\workspace\birthday project\resource\date_pos.txt')
for lines in file.readlines():
    l = lines.split()
    key = '%s %s' %(l[0],l[1]) 
    if key not in photo_location:
        photo_location[key] = l[2]
        #print(key, photo_location[key])


for date in photo_location.keys():
    print('    {name: \'%s\', value: %f},' %(date,int(date[0:4])-2014+float(int(date[5:7])/12)))

for date in photo_location:
    print('    \'%s\':[%s],' %(date, photo_location[date]))

