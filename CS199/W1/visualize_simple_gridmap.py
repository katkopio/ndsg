"""
Visualize simple grid map and also determine dimensions of simple grid map
"""
import pdb

import gpxpy
import sys
from api import parse_gpx_file, generate_corner_pts, generate_grid_fence
from shapely.geometry import Point, Polygon

def calculate_dimensions_gridmap(gpx_track, cell_size):
    point1, point2 = generate_corner_pts(gpx_track)

    side_interval = cell_size * 0.009

    latitude = point1[0]
    longitude = point1[1]

    height = 0
    width = 0

    while latitude > point2[0]:
        while longitude < point2[1]:
            longitude += side_interval
            width +=1

        longitude = point1[1]
        latitude -= side_interval
        height += 1
    return width/float(height), float(height)

def visualize_simple_gridmap(filename, side_length):
    with open(f'DS/{filename}.gpx', 'r') as gpx_file:
        gpx_track = parse_gpx_file(gpx_file)
    point1, point2 = generate_corner_pts(gpx_track)
    
    gpx = gpxpy.gpx.GPX()

    side_interval = side_length * 0.009

    latitude = point1[0]
    longitude = point1[1]

    while latitude > point2[0] - side_interval:
        while longitude < point2[1] + side_interval:
            wp = gpxpy.gpx.GPXWaypoint()
            wp.latitude = latitude
            wp.longitude = longitude
            gpx.waypoints.append(wp)
            longitude += side_interval
        longitude = point1[1]
        latitude -= side_interval
    
    with open(f'DS/{filename}.gpx', 'r') as gpx_file:
        gpx_vehicle = gpxpy.parse(gpx_file)

        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)

        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        segment = gpx_vehicle.tracks[0].segments[0]
        for point in segment.points:
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(point.latitude, point.longitude, time=point.time))

    grid_size = str(side_length) + 'km'
    file_name = f'simplegrids/{filename}_{grid_size}.gpx'

    with open(file_name, 'w') as f:
        f.write(gpx.to_xml())

if __name__ == "__main__":
    # Get Input
    cell = sys.argv[1]
    cell_size = float(cell)
    filename = "ds1"

    with open(f'DS/{filename}.gpx', 'r') as gpx_file:
        gpx_track = parse_gpx_file(gpx_file)

    # Functions
    w, h = calculate_dimensions_gridmap(gpx_track, cell_size)
    visualize_simple_gridmap(filename, cell_size)

    print(f"Dimensions for {filename} with cell size of {cell_size}km: {w}w x {h}h")
