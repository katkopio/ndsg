"""
The route downloaded from OSM for EDSA Carousel is formatted differently from ds1 or ds2
So, modified parse_gpx_file to read waypoints in a GPX file

By only considering unique points, the size of the list shrinks
Not sure if there's that many duplicate time stamps
Can check on this next time
"""

import gpxpy.gpx

def parse_gpx_file(gpx_file_location):
    """
    Parses GPX file to output array of objects
    """
    points = []
    gpx = gpxpy.parse(gpx_file_location)

    for waypoint in gpx.waypoints:
        points.append({
            'latitude': waypoint.latitude,
            'longitude': waypoint.longitude,
            'elevation': waypoint.elevation,
            'time': waypoint.time,
        })

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append({
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'elevation': point.elevation,
                    'time': point.time,
                    'speed': point.speed
                })

    return points

if __name__ == '__main__':
    with open('south.gpx', 'r') as gpx_file_location:
        gps_data = parse_gpx_file(gpx_file_location)