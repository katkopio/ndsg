"""
For some reason, filtering for unique_points for the test GPX file leads to a varying number of points
"""

import gpxpy, pdb

def parse_gpx_file(gpx_file_location):
    """
    Parses GPX file to output array of objects
    """
    points = []
    gpx = gpxpy.parse(gpx_file_location)
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
    unique_points = list({point['time']:point for point in points}.values())
    print(f"ORIG POINTS: {len(points)}")
    print(f"FILTERED POINTS: {len(unique_points)}")

with open('../../DS/test.gpx', 'r') as gpx_file_location:
    gps_data = parse_gpx_file(gpx_file_location)