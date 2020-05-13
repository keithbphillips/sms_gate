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

    def normalize_coords(latitude,longitude):
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
                    coord = re.search('^\[0\]\s(\w+|\w+-\d+)\>\S+:(@\d+\S|!|=|\/)(\d+\.\d+\D)\D(\d+\.\d+\D).*', line)
                    if coord:
                        call_id = coord.group(1)
                        zulu = coord.group(2)
                        latitude = coord.group(3)
                        longitude = coord.group(4)
                        try:
                            call_coords = normalize_coords(latitude, longitude)
                            map_coords[call_id] = call_coords
                            z = re.search('\D(\d\d\d\d\d\d)\D', zulu)
                            if z:
                                if int(z.group(1)) < int(dt.utcnow().strftime("%H%m")) - timedelta(hours=1):
                                    os.remove(root + '/' + filename)    
                        except:
                            pass
                    else:
                        os.remove(root + '/' + filename)    

    for entry in map_coords:
        add_marker(entry, map_coords[entry])

    folium_map.save('/home/pi/smsmessages/sms_gate/app/templates/map.html')
    return
