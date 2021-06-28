import time
import gpxpy

class Point():
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

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

def convert_points(gps_data):
    """
    Converts gps_data into Point objects
    """
    points = []
    for point in gps_data:
        coordinate = Point(point.get("latitude"), point.get("longitude"))
        points.append(coordinate)
    return points

if __name__ == "__main__":
    runs = 100

    print('Points,Seconds')
    for i in range(1,11):
        with open(f'../../traj_points/nsweep_{i}000.gpx','r') as gpx_file:
            gps_data = parse_gpx_file(gpx_file)

            values = []

            for j in range(1, runs + 1):
                t0 = time.time()
                points = convert_points(gps_data)
                t1 = time.time()
                values.append(t1-t0)

            avg = sum(values) / float(runs)
            print(f'{i}000,{avg:.6f}')