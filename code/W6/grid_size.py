from shapely.geometry import Point, Polygon
import datetime
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

def generate_grid_pts(point1, point2, side_length):
    grid = []

    side_interval = side_length * 0.009

    latitude = point1[0]
    longitude = point1[1]

    while latitude > point2[0] - side_interval:
        row = []
        while longitude < point2[1] + side_interval:
            row.append((latitude, longitude))
            longitude += side_interval
        longitude = point1[1]
        latitude -= side_interval

        grid.append(row)

    return grid

def generate_grid_fence(grid_pts):
    grid_fence = []

    for y in range(len(grid_pts)-1):
        for x in range(len(grid_pts)-1):
            top_left_pt = grid_pts[y][x]
            top_right_pt = grid_pts[y][x+1]
            bottom_left_pt = grid_pts[y+1][x]
            bottom_right_pt = grid_pts[y+1][x+1]

            geofence = Polygon([top_left_pt, top_right_pt, bottom_right_pt, bottom_left_pt])
            grid_fence.append(geofence)
    
    return grid_fence

def generate_path(gpx_track, grid_fence):
    path = []
    current_fence = -1

    for point in gpx_track:
        pt = Point(point.get('latitude'), point.get('longitude'))
        for i in range(len(grid_fence)):
            if grid_fence[i].intersects(pt):
                if current_fence != i:
                    current_fence = i 
                    path.append(i)
                    break

    return path

def generate_route(vehicle_route):
    route = [vehicle_route[0]]

    for i in range(1,len(vehicle_route)):
        route.append(vehicle_route[i])
        if vehicle_route[i] == route[0]:
            break
    
    return route

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

def main(file, side_length):
    with open('ds1_times/' + file, 'r') as gpx_file:
        gpx_track = parse_gpx_file(gpx_file)

    point1 = (14.65498, 121.05837) # top left pt
    point2 = (14.64259, 121.07483) # bottom right pt

    grid_pts = generate_grid_pts(point1, point2, side_length)
    grid_fence = generate_grid_fence(grid_pts)

    start = datetime.datetime.now().timestamp()
    vehicle_route = generate_path(gpx_track, grid_fence)
    set_route = generate_route(vehicle_route)
    loops = route_check(set_route, vehicle_route)
    end = datetime.datetime.now().timestamp()

    print(vehicle_route)
    print(set_route)
    print(loops)
    print('{:7.6f}'.format(end - start))

if __name__ == '__main__':
    main(sys.argv[1], float(sys.argv[2]))

# to run use 'python grid_size.py <ds1_time file> <grid cell size in km>'