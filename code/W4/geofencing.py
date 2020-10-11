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

def geofencing(gps_data, min_limit, max_time, point1, point2):
    fence = Polygon([point1, point2, (point1[0], point2[1]), (point2[0], point1[1])])
    index_start = -1
    results = []

    for i in range(len(gps_data)):
        pt = Point(gps_data[i].get('latitude'), gps_data[i].get('longitude'))

        if fence.intersects(pt):
            # print(gps_data[i].get('time').strftime('%X'))
            if index_start == -1:
                index_start = i
        else:
            if index_start != -1:
                timer_start = gps_data[index_start].get('time').timestamp()
                timer_end = gps_data[i-1].get('time').timestamp()
                fence_time = timer_end - timer_start

                if fence_time < min_limit:
                    results.append({
                        'violation': 'below limit',
                        'time': fence_time,
                        'start': gps_data[index_start].get('time').strftime('%X'),
                        'end': gps_data[i-1].get('time').strftime('%X')
                    })
                elif fence_time > max_time:
                    results.append({
                        'violation': 'above limit',
                        'time': fence_time,
                        'start': gps_data[index_start].get('time').strftime('%X'),
                        'end': gps_data[i-1].get('time').strftime('%X')
                    })
                else:
                    results.append({
                        'violation': 'within limit',
                        'time': fence_time,
                        'start': gps_data[index_start].get('time').strftime('%X'),
                        'end': gps_data[i-1].get('time').strftime('%X')
                    })
                
                index_start = -1

    return results

def main(min_time, max_time):
    gpx_file_location = open('../Datasets/ds1_out.gpx', 'r')
    # gpx_file_location = open('../Datasets/20200924.gpx', 'r')
    
    # For Dataset 1
    point1 = (14.654681, 121.058387)
    point2 = (14.654956, 121.058661)

    gps_data = parse_gpx_file(gpx_file_location)
    results = geofencing(gps_data, min_time, max_time, point1, point2)

    for result in results:
        print(result.get('violation'))
        print(result.get('time'))
        print(result.get('start'))
        print(result.get('end'))
        print()

if __name__ == "__main__":
    main(float(sys.argv[1]), float(sys.argv[2]))