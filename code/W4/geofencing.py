from shapely.geometry import Point, Polygon
import gpxpy
import sys

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

    return unique_points

def geofencing(gps_data, min_limit, max_time):
    fence = Polygon([(14.6544901, 121.058524), (14.6544901, 121.058420), (14.654872, 121.058420), (14.654872,121.058524)])
    timer_start = -1
    violation = []

    for i in range(len(gps_data)):
        pt = Point(gps_data[i].get('latitude'), gps_data[i].get('longitude'))

        if fence.intersects(pt):
            print(gps_data[i].get('time').strftime('%X'))
            if timer_start == -1:
                timer_start = gps_data[i].get('time').timestamp()
        else:
            if timer_start != -1:
                timer_end = gps_data[i-1].get('time').timestamp()
                fence_time = timer_end - timer_start

                if fence_time < min_limit:
                    violation.append({
                        'violation': 'below limit',
                        'time': fence_time
                    })
                elif fence_time > max_time:
                    violation.append({
                        'violation': 'above limit',
                        'time': fence_time
                    })
                
                timer_start = -1

    return violation

def main(min_time, max_time):
    gpx_file_location = open('../Datasets/ds1_out.gpx', 'r')
    # gpx_file_location = open('../Datasets/20200924.gpx', 'r')

    gps_data = parse_gpx_file(gpx_file_location)
    results = geofencing(gps_data, min_time, max_time)

    # for result in results:
    #     print(result.get('violation'))
    #     print(result.get('time'))

if __name__ == "__main__":
    main(float(sys.argv[1]), float(sys.argv[2]))