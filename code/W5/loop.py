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

def generate_grid_pts(point1, point2, cells):
    grid = []

    interval_lat = (point1[0] - point2[0]) / cells
    interval_long = (point2[1] - point1[1]) / cells

    latitude = point1[0]
    longitude = point1[1]
    for y in range(cells + 1):
        row = []
        for x in range(cells + 1):
            row.append((latitude, longitude))
            longitude += interval_long
        longitude = point1[1]
        latitude -= interval_lat

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

def path(gpx_track, grid_fence):
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
    
def main():
    with open('../Datasets/ds1_out.gpx', 'r') as gpx_file:
        gpx_track = parse_gpx_file(gpx_file)

    point1 = (14.65498, 121.05837) # top left pt
    point2 = (14.64259, 121.07483) # bottom right pt
    cells = 10
    set_route = [46, 36, 26, 25, 24, 14, 13, 12, 2, 1, 0, 10, 20, 30, 40, 50, 60, 61, 62, 52, 53, 54, 55, 65, 66, 56, 46]

    grid_pts = generate_grid_pts(point1, point2, cells)
    grid_fence = generate_grid_fence(grid_pts)
    vehicle_route = path(gpx_track, grid_fence)
    loops = route_check(set_route, vehicle_route)

    print(vehicle_route)
    print(loops)

if __name__ == "__main__":
    main()