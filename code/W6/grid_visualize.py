import gpxpy
import sys

def main(file, side_length):
    point1 = (14.65498, 121.05837) # top left pt
    point2 = (14.64259, 121.07483) # bottom right pt

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
    
    with open('ds1_times/' + file, 'r') as gpx_file:
        gpx_vehicle = gpxpy.parse(gpx_file)

        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)

        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        segment = gpx_vehicle.tracks[0].segments[0]
        for point in segment.points:
            gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(point.latitude, point.longitude, time=point.time))

    if file != 'base.gpx':
        time_freq = file.split('_')[2].split('.')[0]
    else:
        time_freq = 'base'
    grid_size = str(side_length) + 'km_'
    file_name = 'ds1_grids/ds1_grid_' + grid_size + time_freq + '.gpx'

    with open(file_name, 'w') as f:
        f.write(gpx.to_xml())

if __name__ == '__main__':
    main(sys.argv[1], float(sys.argv[2]))

# to run use 'python grid_visualize.py <ds1_time file> <grid cell size in km>'