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

def loop_counting(route, traj, grid_cells):
    errors = 0
    loops = 0
    r = 0
    i = 0
    while i < len(traj):
        if traj[i] == route[r]:
            r += 1
        else:
            ind = find_current_index(traj[i], route)
            # "Local" Errors
            if ind != -1:
                if ind > r:
                    r = ind + 1
                elif ind < r:
                    if traj[ind] == route[0]:
                        if traj[i - 1] == route[1]:
                            r = ind + 1
                        else: 
                            r = len(route) 
                    else:
                        r = ind + 1
            # "Foreign" Errors
            elif ind == -1:
                i, r, detour, missed_route = detour_info(i, r, route, traj)
                errors += check_neighbors(detour, missed_route, grid_cells)
        if r == len(route):
            r = r % len(route)
            if errors == 0:
                loops += 1
            else:
                errors = 0
        i += 1
    return loops

def detour_info(i, r, route, traj):
    detour = []
    missed_route = []
    sub_traj = traj[i:]
    _i = i
    
    # Find Detour List
    for j in range(len(sub_traj)):
        if find_current_index(sub_traj[j], route) == -1:
            detour.append(sub_traj[j])
            i += 1
        else:
            break

    # Find Missing Route
    if _i == 0:
        if find_current_index(traj[i], route) == 0:
            missed_route = [route[0]]
        else:
            end_index = find_current_index(traj[i], route) + 1
            missed_route = route[0:end_index]
        r = find_current_index(traj[i], route) + 1
    elif _i != 0:
        start_index = find_current_index(traj[_i-1], route)
        if i == len(traj):
            missed_route = route[start_index:len(route)]
            r = len(route) # arbitrary, traj has already ended
        else:
            end_index = find_current_index(traj[i], route) + 1
            if end_index < start_index:
                missed_route = route[start_index:len(route)]
                missed_route.append(end_index)
            else:
                missed_route = route[start_index:end_index]
            r = find_current_index(traj[i], route) + 1
    return i, r, detour, missed_route

def check_neighbors(detour, missed_route, grid_cells):
    match = False
    err = 0

    width = len(grid_cells[0])
    length = len(grid_cells) * len(grid_cells[0])

    for d in detour:
        for r in missed_route:
            if d in adjacent_cells(r, width, length):
                match = True 
                break
            else:
                match = False 
        if match == False:
            err = 1
            break 
    return err

def adjacent_cells(d, w, l):
    # Top Left
    if d == 0:
        return [d+1, d+w, d+w+1]
    # Top Right
    elif d == w-1:
        return [d-1, d+w-1, d+w]
    # Bottom Left
    elif d == l-w:
        return [d-w, d-w+1, d+1]
    # Bottom Right
    elif d == l-1:
        return [d-w-1, d-w, d-1]
    # North
    elif d < w:
        return [d-1, d+1, d+w-1, d+w, d+w+1]
    # South
    elif (d < l) and (d >= l-w):
        return [d-w-1, d-w, d-w+1, d-1, d+1]
    # West
    elif d % w == 0:
        return [d-w, d-w+1, d+1, d+w, d+w+1]
    # East
    elif d % w == w - 1:
        return [d-w-1, d-w, d-1, d+w-1, d+w]
    # Middle
    else:
        return [d-w-1, d-w, d-w+1, d-1, d+1, d+w-1, d+w, d+w+1]

def find_current_index(cell, route_list):
    # Find what index in the route_list the trajectory cell exists in
    for i in range(len(route_list)):
        if route_list[i] == cell:
            return i
    return -1

if __name__ == "__main__":
    cell_size = 1

    runs = 100

    with open('../../traj_points/DS7_route.gpx','r') as gpx_file:
        route_gps = parse_gpx_file(gpx_file)

        print('Points,Seconds')
        for i in range(1,11):
            with open(f'../../traj_points/nsweep_{i}000.gpx','r') as gpx_file:
                vehicle_gps = parse_gpx_file(gpx_file)

                point1, point2 = generate_corner_pts(vehicle_gps, cell_size)
                grid = generate_grid_fence(point1, point2, cell_size)
                vehicle_path = generate_path(vehicle_gps, grid)
                route_path = generate_path(route_gps, grid)

                values = []

                for j in range(1, runs + 1):
                    t0 = time.time()
                    loops = loop_counting(route_path, vehicle_path, grid)
                    t1 = time.time()
                    values.append(t1-t0)

                avg = sum(values) / float(runs)
                print(f'{i}000,{avg:.6f}')
