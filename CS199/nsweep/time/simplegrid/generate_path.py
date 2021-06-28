import time
import gpxpy

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

def generate_grid_fence(point1, point2, side_length):
    grid_fence = []

    side_interval = side_length * 0.009

    latitude = point1.lat
    longitude = point1.lon

    while latitude > point2.lat:
        row = []

        while longitude < point2.lon:
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
                    if current_fence != i:
                        current_fence = i 
                        path.append(i)
                        break

    return path

if __name__ == "__main__":
    cell_size = 1
    cell_step_interval = 0.09

    runs = 100
    
    # varying traj size
    print('Points,Seconds')
    for i in range(1,11):
        with open(f'../../traj_points/nsweep_{i}000.gpx','r') as gpx_file:
            gps_data = parse_gpx_file(gpx_file)

            point1, point2 = generate_corner_pts(gps_data, cell_size)
            grid_fence = generate_grid_fence(point1, point2, cell_size)

            values = []

            for j in range(1, runs + 1):
                t0 = time.time()
                path = generate_path(gps_data, grid_fence)
                t1 = time.time()
                values.append(t1-t0)

            avg = sum(values) / float(runs)
            print(f'{i}000,{avg:.6f}')

    print()

    # varying first dimension of grid
    print('First Dimension,Seconds')
    with open(f'../../traj_points/nsweep_1000.gpx','r') as gpx_file:
        gps_data = parse_gpx_file(gpx_file)

        pt1, pt2 = generate_corner_pts(gps_data, cell_size)

        values = []

        for i in range(1,11):
            curr_pt1 = Point(pt1.lat + (i - 1) * cell_step_interval, pt1.lon)

            grid = generate_grid_fence(curr_pt1, pt2, cell_size)
            
            for j in range(1, runs + 1):
                t0 = time.time()
                path = generate_path(gps_data, grid)
                t1 = time.time()
                values.append(t1-t0)

            avg = sum(values) / float(runs)
            print(f'{len(grid)},{avg:.6f}')

    print()

    # varying second dimension of grid
    print('Second Dimension,Seconds')
    with open(f'../../traj_points/nsweep_1000.gpx','r') as gpx_file:
        gps_data = parse_gpx_file(gpx_file)

        pt1, pt2 = generate_corner_pts(gps_data, cell_size)

        values = []

        for i in range(1,11):
            curr_pt1 = Point(pt1.lat, pt1.lon - (i - 1) * cell_step_interval)

            grid = generate_grid_fence(curr_pt1, pt2, cell_size)
            
            for j in range(1, runs + 1):
                t0 = time.time()
                path = generate_path(gps_data, grid)
                t1 = time.time()
                values.append(t1-t0)

            avg = sum(values) / float(runs)
            print(f'{len(grid[0])},{avg:.6f}')
