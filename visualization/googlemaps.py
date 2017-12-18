# googleMaps.py
# Use this to play with Google Maps Static Maps API
# by James Fulford
# Began: 6/7/2016
# Stopped Developing: 6/8/2016
# Jing: http://screencast.com/t/z2gEdPXUyjsK

import webbrowser
import math


def googleMaps(center, markers):
    """
    Provided a tuple with latitude, longitude of the center of the map
    and a list of tuples specifying latitude, longitude, then color(optional)
    opens a google map static image of dimensions 500x500.

    Tested.
    """
    url = 'http://maps.googleapis.com/maps/api/' + \
          'staticmap?size=500x500&sensor=false'
    url = url + 'center=%f,%f' % (center[0], center[1])
    if len(markers) == 1:
        if len(markers[0]) == 2:
            url = url + '&markers=%f,%f' % (markers[0][0], markers[0][1])
        elif len(markers[0]) == 3:
            url = url + '&markers=color:%s|%f,%f' % \
                (markers[0][2], markers[0][0], markers[0][1])
    else:
        for marker in markers:
            if len(marker) == 2:
                url = url + '&markers=%f,%f' % (marker[0], marker[1])
            elif len(marker) == 3:
                url = url + '&markers=color:%s|%f,%f' % \
                    (marker[2], marker[0], marker[1])
    webbrowser.open(url)


def tupleAppend(tuple1, appendage):
    result = list(tuple1)
    result.append(appendage)
    return tuple(result)


def surroundTarget(target_coordinates, radius_kilometers, numberSurroundPins):
    """
    Accurate only for small radius. Acts weird near poles Radius in miles.
    Note: Google has 400 error if numberSurroundPins is greater than 47.
    """
    if numberSurroundPins <= 47:
        angleDifferential = 360 / numberSurroundPins
        listOfPins = []
        for i in range(0, numberSurroundPins):
            coordinates = coordinatesTravel(target_coordinates,
                                            angleDifferential * i,
                                            radius_kilometers)
            listOfPins.append(tupleAppend(coordinates, 'blue'))
        googleMaps(target_coordinates, listOfPins)
    else:
        print("Requested too many pins - displaying 47.")
        surroundTarget(target_coordinates, radius_kilometers, 47)


def coordinatesTravel(start_coordinates, heading_degrees, distance_kilometers):
    radius = 6378.14  # radius of earth in kilometers

    latitude = math.pi * start_coordinates[0] / 180
    longitude = math.pi * start_coordinates[1] / 180
    bearing_radians = math.pi * heading_degrees / 180

    part = math.sin(latitude) * \
        math.cos(distance_kilometers / radius)
    next_part = part + math.cos(latitude) * \
        math.sin(distance_kilometers / radius) * math.cos(bearing_radians)
    new_lat = math.asin(next_part)

    first_parameter = math.sin(bearing_radians) * \
        math.sin(distance_kilometers / radius) * \
        math.cos(latitude)
    second_parameter = math.cos(distance_kilometers / radius) - \
        math.sin(latitude) * math.sin(new_lat)
    new_long = longitude + math.atan2(first_parameter, second_parameter)

    return (new_lat * 180 / math.pi, new_long * 180 / math.pi)
