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

def generate_corner_pts(gps_data, buffer=0.1):
    greatest_lat = gps_data[0].get('latitude')
    least_lat = gps_data[0].get('latitude')
    greatest_long = gps_data[0].get('longitude')
    least_long = gps_data[0].get('longitude')

    for point in gps_data:
        point_lat = point.get('latitude')
        point_long = point.get('longitude')

        if point_lat > greatest_lat:
            greatest_lat = point_lat 
        elif point_lat < least_lat:
            least_lat = point_lat
        
        if point_long > greatest_long:
            greatest_long = point_long
        elif point_long < least_long:
            least_long = point_long

    # 1km * buffer, buffer by default is 0.1 (100m), buffer is set to cell_size
    greatest_lat += 0.009 * buffer
    least_long -= 0.009 * buffer
    least_lat -= 0.009 * buffer
    greatest_long += 0.009 * buffer

    return Point(greatest_lat, least_long), Point(least_lat, greatest_long)

if __name__ == "__main__":
    runs = 100

    print('Points,Seconds')
    for i in range(1, 11):
        with open(f'../../traj_points/nsweep_{i}000.gpx','r') as gpx_file:
            gps_data = parse_gpx_file(gpx_file)

            values = []

            for j in range(1, runs + 1):
                t0 = time.time()
                pts = generate_corner_pts(gps_data)
                t1 = time.time()
                values.append(t1-t0)

            avg = sum(values) / float(runs)
            print(f'{i}000,{avg:.6f}')