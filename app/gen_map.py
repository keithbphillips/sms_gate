import folium
from folium.features import DivIcon
import re
from re import search 
from datetime import datetime as dt
from datetime import timedelta
import codecs
import os
from os import walk

map_coords = {}

mypath = '/home/pi/smsmessages/out'
mycall = 'KI7ADJ-1'
mycoords = [45.816040, -122.999950]

def gen_map():
    files = []
    for (dirpath, dirnames, filenames) in walk(mypath):
        files.extend(filenames)
        break

    folium_map = folium.Map(location=mycoords,
                        zoom_start=8,
                        tiles="Stamen Terrain")

    def normalize_coords(lat_deg,lat_min,lat_sec,lat_dir,long_deg,long_min,long_sec,long_dir):
        if lat_dir == "S":
            lat_deg = lat_deg - lat_deg * 2
        latitude = float(lat_deg + (lat_min/60) + (lat_sec/3600)) 

        if long_dir == "W":
            long_deg = long_deg - long_deg * 2
        longitude = float(long_deg + (long_min/60) + (long_sec/3600)) 

        fixed_coords = [round(latitude, 4), round(longitude, 4)]
        print(fixed_coords)
        return fixed_coords
        
    def add_marker(call_id, coord_num):
        tooltip = call_id
        #marker = folium.Marker(location=coord_num, tooltip=tooltip).add_to(folium_map)
        marker = folium.map.Marker(
        coord_num,
        icon=DivIcon(
            icon_size=(100,36),
            icon_anchor=(0,0),
            html='<div style="font-size: 12pt; color: blue;">'+ tooltip + '</div>',
            )
        ).add_to(folium_map)

    add_marker(mycall, mycoords)

    for file in files:
       for root, dirs, files in os.walk("/home/pi/smsmessages/out"):
            for filename in files:
                with codecs.open(root + '/' + filename, 'r', encoding='utf-8', errors='ignore') as line:
                    line = line.readline()
                    msg_date = dt.strptime(filename, '%Y%m%d-%H%M%S-%f')
                    coord = re.search('^\[0\]\s(\w+|\w+-\d+)\>\S+:(@\d+\S|!|=|\/)(\d\d)(\d\d)\.(\d+)(\D)\D(\d\d\d)(\d\d)\.(\d+)(\D).*', line)
                    if coord:
                        call_id = coord.group(1)
                        zulu = coord.group(2)
                        lat_deg = coord.group(3)
                        lat_min = coord.group(4)
                        lat_sec = coord.group(5)
                        lat_dir = coord.group(6)
                        long_deg = coord.group(7)
                        long_min = coord.group(8)
                        long_sec = coord.group(9)
                        long_dir = coord.group(10)
                        try:
                            call_coords = normalize_coords(int(lat_deg), int(lat_min), int(lat_sec), lat_dir, int(long_deg), int(long_min), int(long_sec), long_dir)
                            map_coords[call_id] = call_coords
                            z = re.search('\D(\d\d\d\d\d\d)\D', zulu)
                            if z:
                               if int(z.group(1)) < int((dt.utcnow()- timedelta(hours=1)).strftime("%H%m%s")):
                                   os.remove(root + '/' + filename)    
                        except:
                            pass
                    else:
                        os.remove(root + '/' + filename)    

    for entry in map_coords:
        print(entry, map_coords[entry])
        add_marker(entry, map_coords[entry])

    folium_map.save('/home/pi/smsmessages/sms_gate/app/templates/map.html')
    return
=======
files = []
for (dirpath, dirnames, filenames) in walk(mypath):
    files.extend(filenames)
    break

folium_map = folium.Map(location=mycoords,
                    zoom_start=8,
                    tiles="Stamen Terrain")

def normalize_coords(coords):
    latitude, longitude = coords.split("/")
    if search("S", latitude):
        latitude = latitude.replace("S","")
        latitude = float(latitude)
        latitude = latitude - latitude * 2
    else:
        latitude = latitude.replace("N","")
        latitude = float(latitude)

    if search("W", longitude):
        longitude = longitude.replace("W","")
        longitude = float(longitude)
        longitude = longitude - longitude * 2
        
    else:
        longitude = longitude.replace("E","")
        longitude = float(longitude)


    fixed_coords = [round(latitude / 100, 4), round(longitude /100, 4)]
    return fixed_coords
    
def add_marker(call_id, coord_num):
    tooltip = call_id
    marker = folium.Marker(location=coord_num, tooltip=tooltip).add_to(folium_map)

add_marker(mycall, mycoords)

for file in files:
   for root, dirs, files in os.walk("/home/pi/smsmessages/out"):
        for filename in files:
            with codecs.open(root + '/' + filename, 'r', encoding='utf-8', errors='ignore') as line:
                line = line.readline()
                msg_date = dt.strptime(filename, '%Y%m%d-%H%M%S-%f')
                coord = re.search('\[0\]\s(\S+)>.*@\d+\w(\d*.\d+\w\/\d+.\d+\w).*', line)
                if coord:
                    call_id = coord.group(1)
                    log_coord = (coord.group(2))
                    try:
                        call_coords = normalize_coords(log_coord)
                        map_coords[call_id] = call_coords
                    except:
                        pass
for entry in map_coords:
    print(entry, map_coords[entry]) 
    add_marker(entry, map_coords[entry])

folium_map.save('/home/pi/smsmessages/sms_gate/app/templates/map.html')
