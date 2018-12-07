'''A program to show the potential burn of a forest fire on a Folium
map using the Forest_Fire package/model'''
import json
import pandas as pd
import geopy
from geopy.distance import VincentyDistance
import folium.plugins
import folium

def user_gps():
    '''Gather user data for later functions'''
    latitude = input('Enter the latitude: ')
    longitude = input('Enter the longitude: ')
    return (float(latitude), float(longitude))

def get_map(latitude=40.77041, longitude=-111.89246):
    '''Displays map with default cords of SLC Utah USA'''
    show_map = folium.Map(location=[latitude, longitude], tiles='OpenStreetMap', zoom_start=11)
    return show_map

def get_length():
    '''Gathers info for later functions'''
    length = input('Enter the length of the evacuation area (in KM): ')
    return float(length)

def sub_divisions():
    '''Get user input and makes m odd'''
    num_squares = int(input('Enter (an odd) number of subdivision for latitude'))
    if int(num_squares) % 2 == 0:
        num_squares = int(num_squares) + 1
    return num_squares

def delta_c(latitude, longitude, distance, bearing):
    '''given: lat1, lon1, bearing = bearing in degrees, distance = distance in kilometers.
    The program outputs the change in coordinates by moving a distance and bearing'''
    origin = geopy.Point(latitude, longitude)
    destination = VincentyDistance(kilometers=distance).destination(origin, bearing)
    lat2, lon2 = destination.latitude, destination.longitude
    d_lat = lat2 - latitude
    d_lon = lon2 - longitude
    return(d_lat, d_lon)

def make_cords(latitude, longitude, num_squares, length):
    ''' Makes the coordinates for the grid based on the inputs'''
    cords = []
    (dx_lat, dx_lon) = delta_c(latitude, longitude, length / (num_squares + 2), 0)
    (dy_lat, dy_lon) = delta_c(latitude, longitude, length / (num_squares + 2), 90)
    for i in range(-int((num_squares + 1) / 2), int(1 + ((1 + num_squares) / 2))):
        for j in range(-int((num_squares + 1) / 2), int(1 + ((1 + num_squares) / 2))):
            cords.append((latitude + i * dx_lat + j * dy_lat,
                          longitude + i * dx_lon + j * dy_lon))
    return cords

def make_squares(cords, num_squares):
    '''This function makes the polygon/square data to be inputted into the
    geojasonfile to display on the folium map'''
    squares = []
    for i in range(0, len(cords) - num_squares - 3):
        if (i + 1) % (num_squares + 2) == 0:
            continue
        draw_square = [
            [cords[i][1], cords[i][0]],
            [cords[i + 1][1], cords[i + 1][0]],
            [cords[i + num_squares + 3][1], cords[i + num_squares + 3][0]],
            [cords[i + num_squares + 2][1], cords[i + num_squares + 2][0]],
            [cords[i][1], cords[i][0]]
        ]
        squares.append(draw_square)
    return squares

def geojson(squares):
    '''This is the formatting of the geojson file. After this function the
    dictionary json_string must be converted to a file'''
    json_string = {
        "type": "FeatureCollection",
        "features": []
    }
    for i in range(0, len(squares)):
        square = {
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
        json_string['features'].append(square)
    return json_string

def square_burn(matrix, num_squares):
    '''Determines how much of the area/square is burned based on the input matrix'''
    data = []
    for i in range(0, num_squares + 1):
        for j in range(0, num_squares + 1):
            data.append(burn_ratio(matrix_to_square(matrix, i, j)))
    return data

def matrix_to_square(matrix, i, j):
    '''Slices the matrix so that is corresponds to a square of the geojson file'''
    m_slice = matrix[i * 10:(i + 1) * 10, j * 10:(j + 1) * 10]
    return m_slice

def burn_ratio(matrix):
    '''Calculates the amount burned for the matrix'''
    total = matrix.shape[0] * matrix.shape[1]
    count = matrix.sum()
    return count / total

def json_file(num_squares, length, latitude, longitude):
    '''Writes a json file for the map'''
    cords = make_cords(latitude, longitude, num_squares, length)
    squares = make_squares(cords, num_squares)
    json_string = geojson(squares)
    write_string = json.dumps(json_string)
    file = open("area.geojson", "w+")
    file.write(write_string)
    file.close()

def display_map(matrix, num_squares, latitude, longitude):
    ''' This function colors the map given the inputs, and colors it according
    to the proportion of the model burned.'''
    data = square_burn(matrix, num_squares) #Color the map
    make_name = [str(d) for d in range(0, (num_squares+1)**2)]
    color_data = pd.DataFrame({'value': data, 'name': make_name})
    show_map = get_map(latitude, longitude)
    show_map.choropleth(
        geo_data='area.geojson',
        name='chloropleth',
        data=color_data,
        columns=['name', 'value'],
        threshold_scale=[0, .2, .4, .6, .8, 1],
        key_on='properties.name',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Forest Fire'
    )
    folium.LayerControl().add_to(show_map)
    return show_map
