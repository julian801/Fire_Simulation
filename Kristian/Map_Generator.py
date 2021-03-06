
# Code review: Kristian 2018/12/02

# KR: short description of the module could go here

import os
import geopy
from geopy.distance import VincentyDistance
import pandas as pd
import folium
import json
import folium.plugins
import math
import numpy as np
import random
from Forest_Fire import ForestFire

# KR: import section: looks good
#     style recommendation: lower_case.py module names

def UserGPS():
    # KR: most Python programmers expect lower_case() function names
    #     recommendation: run pylint over it.
    latitude = input('Enter the latitude: ')
    longitude = input('Enter the longitude: ')
    return (float(latitude), float(longitude))
    # KR: function nice & clear


def GetMap(latitude=40.77041, longitude=-111.89246):
    Map = folium.Map(location=[latitude, longitude], tiles='OpenStreetMap',
                     zoom_start=10)
    return Map
    # KR: don't know whether a separate function is necessary here


def getParams():
    length = input('Enter the length of the evacuation area (in KM): ')
    width = input('Enter the width of the evacuation area (in KM): ')
    return (float(length), float(width))


def getNM():
    n = int(input('Enter (an odd) number of subdivision for longitude'))
    m = int(input('Enter (an odd) number of subdivision for latitude'))
    # Make n and m odd
    # KR: super useful comment!
    #     recommendation: make it a docstring (2 lines higher, triple quoted)
    if int(n) % 2 == 0:
        n = int(n) + 1
    if int(m) % 2 == 0:
        m = int(m) + 1
    return (n, m)


def Delta_C(latitude, longitude, d, b):
    # given: lat1, lon1, b = bearing in degrees, d = distance in kilometers
    origin = geopy.Point(latitude, longitude)
    destination = VincentyDistance(kilometers=d).destination(origin, b)
    lat2, lon2 = destination.latitude, destination.longitude
    d_lat = lat2 - latitude
    d_lon = lon2 - longitude
    return(d_lat, d_lon)


def Make_Cords(latitude, longitude, n, m):
    # Make the coordinates
    cords = []
    (length, width) = getParams()
    (dx_lat, dx_lon) = Delta_C(latitude, longitude, length / (n + 2), 0)
    (dy_lat, dy_lon) = Delta_C(latitude, longitude, width / (m + 2), 90)
    for i in range(-int((n + 1) / 2),  int(1 + ((1 + n) / 2))):
        for j in range(-int((m + 1) / 2),  int(1 + ((1 + m) / 2))):
            cords.append((latitude + i * dx_lat + j * dy_lat,
                          longitude + i * dx_lon + j * dy_lon))
    return cords
    # KR: good, would benefit from short description


def Make_Squares(cords, m):
    # Make the squares
    squares = []
    for i in range(0, len(cords) - m - 3):
        if (i + 1) % (m + 2) == 0:
            continue
        s = [
            [cords[i][1], cords[i][0]],
            [cords[i + 1][1], cords[i + 1][0]],
            [cords[i + m + 3][1], cords[i + m + 3][0]],
            [cords[i + m + 2][1], cords[i + m + 2][0]],
            [cords[i][1], cords[i][0]]
        ]
        squares.append(s)
    return squares


def Make_GeoJason(squares):
    # KR: spelling: GeoJSON
    mm = {
        "type": "FeatureCollection",
        "features": []
    }
    for i in range(0, len(squares)):
        sq = {
            "type": "Feature",
            "id": str(i),
            "properties": {'name': str(i)},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    squares[i]
                ]
            }
        }
        mm['features'].append(sq)
    return mm


def Square_Burn(matrix, m, n):
    data = []
    for i_m in range(0, m + 1):
        for j_n in range(0, n + 1):
            data.append(burn_ratio(matrix_to_square(matrix, i_m, j_n)))
    return data


def matrix_to_square(matrix, i_m, j_n):
    m_slice = matrix[i_m * 10:(i_m + 1) * 10, j_n * 10:(j_n + 1) * 10]
    return m_slice


def burn_ratio(matrix):
    total = matrix.shape[0] * matrix.shape[1]
    count = matrix.sum()
    return count / total


def show_map():
    # KR: could be useful to have some parameters in this function
    #     so that you can play around with your model more easily
    from Forest_Fire import ForestFire
    # KR: import is not necessary here, you have it above

    (latitude, longitude) = UserGPS()
    (n, m) = getNM()
    cords = Make_Cords(latitude, longitude, n, m)
    squares = Make_Squares(cords, m)
    mm = Make_GeoJason(squares)
    s = json.dumps(mm)
    f = open("area.geojson", "w+")
    f.write(s)
    f.close()
    """
    KR: suggestion: use a ContextManager, remove f.close()
    with open(...) as f:
        f.write(s)
    """
    # use forest fire
    fire = ForestFire((n + 1) * 10, (m + 1) * 10, 0.5)
    fire.run_model()
    data = Square_Burn(fire.MatrixHistory[0], m, n)
    makename = [str(d) for d in range(0, len(squares))]
    df = pd.DataFrame({'value': data, 'name': makename})

    Map = GetMap(latitude, longitude)
    Map.choropleth(
        geo_data='area.geojson',
        name='chloropleth',
        data=df,
        columns=['name', 'value'],
        threshold_scale=[0, .2, .4, .6, .8, 1],
        key_on='properties.name',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Forest Fire'
    )
    folium.LayerControl().add_to(Map)
    return Map

"""
KR: 
Your code looks very well structured. I did not find *any* redundancies or
bigger unnecessary code fragments. This is rare given your experience.
It makes an impression that you really thought through how you want to write
the program.

I think you could show this on your portfolio almost without modification. 
My main recommendations are:

1. write docstrings in the bigger/less obvious functions
2. run pylint over it
3. think whether you want to offer some other way of entering input data than input()
4. clean up the git repository:
   - remove __pycache__, .DS_Store, .ipynb_checkpoints, old_files
   - add a README
   - add a License
   - add a description
-------

I like how the notebook(s) got really short. To make your portfolio a little richer you could
- run a few more simulations with different conditions (and generate more plots)
- put map tiles in your map
- write some text around it to display it online (can be done later)
- ask me for more feedback
"""
