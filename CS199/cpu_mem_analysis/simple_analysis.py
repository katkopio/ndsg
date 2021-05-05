""" 
This code generates CPU/Mem Time Series data for simple grids
Code is copy pasted from the API module in order to easily add time stamps
"""
import os, psutil, time, gpxpy
from datetime import datetime
from multiprocessing import Process

""" CODE FROM API """
# THIS IS FOR EASIER TIME STAMPING #

class Point():
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

class Polygon():
    def __init__(self, top_left_pt, bottom_right_pt):
        self.top_left_pt = top_left_pt
        self.bottom_right_pt = bottom_right_pt

    def contains(self, point):
        if self.top_left_pt.lat >= point.lat and self.top_left_pt.lon <= point.lon and self.bottom_right_pt.lat < point.lat and self.bottom_right_pt.lon > point.lon:
            return True
        else:
            return False

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

def generate_grid_fence(point1, point2, side_length):
    grid_fence = []

    side_interval = side_length * 0.009

    latitude = point1.lat
    longitude = point1.lon

    while latitude > point2.lat - side_interval:
        row = []

        while longitude < point2.lon + side_interval:
            top_left_pt = Point(latitude, longitude)
            bottom_right_pt = Point(latitude - side_interval, longitude + side_interval)

            geofence = Polygon(top_left_pt, bottom_right_pt)
            row.append(geofence)

            longitude += side_interval

        longitude = point1.lon
        latitude -= side_interval

        grid_fence.append(row)

    return grid_fence

def generate_path(gps_data, grid_fence):
    path = []
    current_fence = -1

    if isinstance(grid_fence[0], list):
        for point in gps_data:
            pt = Point(point.get('latitude'), point.get('longitude'))
            for i in range(len(grid_fence)):
                for j in range(len(grid_fence[0])):
                    if grid_fence[i][j].contains(pt):
                        # timestamp("in process: loop counting")
                        fence_number = i * len(grid_fence[0]) + j
                        if current_fence != fence_number:
                            current_fence = fence_number
                            path.append(fence_number)
                            break
                else:
                    continue
                break
    else:
        for point in gps_data:
            pt = Point(point.get('latitude'), point.get('longitude'))
            for i in range(len(grid_fence)):
                if grid_fence[i].contains(pt):
                    # timestamp("in process: loop counting")
                    if current_fence != i:
                        current_fence = i 
                        path.append(i)
                        break

    return path

def route_check(set_route, vehicle_route):
    set_route = "".join([str(x) for x in set_route])
    vehicle_route = "".join([str(x) for x in vehicle_route])

    loops = 0
    start = 0 
    while start < len(vehicle_route):
        pos = vehicle_route.find(set_route, start)

        if pos != -1:
            start = pos + 1
            loops += 1
        else:
            break

    return loops

""" END CODE FROM API """

def analyze(pid):
    pr = psutil.Process(pid=pid)
    while psutil.pid_exists(pid):
        print(f"1,{datetime.now()},{pr.cpu_percent()},{pr.cpu_times().user},{pr.cpu_times().system},{pr.memory_info().rss},{pr.memory_info().vms},{pr.memory_info().pfaults},{pr.memory_info().pageins},{pr.memory_percent()}")
        time.sleep(0.1)

def timestamp(comment):
    print(f"0,{datetime.now()},{comment}")

def main():
    # Open Files
    timestamp("opening file")
    filename = "test"
    with open(f'../../DS/{filename}.gpx', 'r') as gpx_file_location:
        gps_data = parse_gpx_file(gpx_file_location)

    gpx_route = "test"
    with open(f'../../DS/{gpx_route}.gpx', 'r') as gpx_file:
        gps_route = parse_gpx_file(gpx_file)

    # Create Simple Grid Map 
    cell_size = 0.1
    timestamp("generating corner points")
    point1, point2 = generate_corner_pts(gps_data)
    timestamp("generating grid fence")
    grid_cells = generate_grid_fence(point1, point2, cell_size)


    # Loop Count
    timestamp("generating path of vehicle")
    vehicle_path = generate_path(gps_data, grid_cells)
    timestamp("generating route")
    route_path = generate_path(gps_route, grid_cells)
    timestamp("about to loop count")
    loops = route_check(route_path, vehicle_path)
    timestamp("done looping")

if __name__ == "__main__":
    print("type,time,cpupercent,cputime_user,cputime_system,rss,vms,pfaults,pageins,mempercent")
    p1 = Process(target=main)
    p1.start()
    p2 = Process(target=analyze, args=(p1.pid,))
    p2.start()

    p1.join()
    p2.join()