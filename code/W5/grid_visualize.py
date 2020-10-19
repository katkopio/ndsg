import gpxpy
import sys

def main(segments):
    top_left_lat = 14.65498
    top_left_long = 121.05837

    bottom_right_lat = 14.64259
    bottom_right_long = 121.07483

    gpx = gpxpy.gpx.GPX()

    diff_lat = top_left_lat - bottom_right_lat
    diff_long = bottom_right_long - top_left_long

    interval_lat = diff_lat / segments
    interval_long = diff_long / segments

    latitude = top_left_lat
    longitude = top_left_long
    for x in range(segments + 1):
        for y in range(segments + 1):
            wp = gpxpy.gpx.GPXWaypoint()
            wp.latitude = latitude
            wp.longitude = longitude
            gpx.waypoints.append(wp)

            longitude += interval_long

        longitude = top_left_long
        latitude -= interval_lat

    with open('ds1_grid.gpx', 'w') as f:
        f.write(gpx.to_xml())

if __name__ == '__main__':
    main(int(sys.argv[1]))