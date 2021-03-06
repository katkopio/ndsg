# Trying to make a quadtree from GPS points using our own GPX data
# Adapted from: https://katherinepully.com/quadtree-python/

import sys
import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import gpxpy
import pdb

def parse_gpx_file(gpx_file_location):
    """
    Parses GPX file and outputs x and y
    """
    points = []
    gpx_data_route = []
    lat = []
    lon = []
    gpx = gpxpy.parse(gpx_file_location)
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                gpx_data_route.append({
                    'latitude': point.latitude,
                    'longitude': point.longitude,
                    'elevation': point.elevation,
                    'time': point.time,
                    'speed': point.speed
                })
                coordinate = Point(point.longitude, point.latitude)
                points.append(coordinate)
                lon.append(point.longitude)
                lat.append(point.latitude)

    unique_points = list({point['time']:point for point in gpx_data_route}.values())

    return unique_points, points, min(lon), min(lat), max(lon)-min(lon), max(lat)-min(lat)

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Node():
    def __init__(self, x0, y0, w, h, points, depth):
        self.x0 = x0
        self.y0 = y0
        self.width = w
        self.height = h
        self.points = points
        self.children = []
        self.depth = depth

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    
    def get_points(self):
        return self.points

    def contains(self, point):
        if point.x >= self.x0 and point.x <= (self.x0 + self.width) and point.y >= self.y0 and point.y <= (self.y0 + self.height):
            return True
        else:
            return False

class QTree():
    def __init__(self, k, points, root):
        self.threshold = k
        self.points = points
        self.root = root

    def add_point(self, x, y):
        self.points.append(Point(x, y))
    
    def get_points(self):
        return self.points

    def get_cells(self):
        return find_children(self.root)

    def subdivide(self):
        recursive_subdivide(self.root, self.threshold)
    
    def graph(self):
        fig = plt.figure(figsize=(8, 8))
        plt.title(f"By max depth: {self.threshold}")
        ax = fig.add_subplot(111)
        c = find_children(self.root)
        print(f"Max depth: {self.threshold}")
        print(f"Number of nodes: {len(c)}")
        areas = set()
        for el in c:
            areas.add(el.width*el.height)
        print(f"Minimum segment area: {min(areas)} units")
        for n in c:
            ax.add_patch(patches.Rectangle((n.x0, n.y0), n.width, n.height, fill=False))
        x = [point.x for point in self.points]
        y = [point.y for point in self.points]
        plt.plot(x, y, 'ro')
        print(f"Time Elapsed: {time.time()-start_time}")
        plt.show()
        return

def recursive_subdivide(node, k):
    if len(node.points) <= 1 or node.depth >= k:
        return
    w_ = float(node.width/2)
    h_ = float(node.height/2)

    # increase depth of node here
    p = contains(node.x0, node.y0, w_, h_, node.points)
    x1 = Node(node.x0, node.y0, w_, h_, p, node.depth+1)
    recursive_subdivide(x1, k)

    p = contains(node.x0, node.y0+h_, w_, h_, node.points)
    x2 = Node(node.x0, node.y0+h_, w_, h_, p, node.depth+1)
    recursive_subdivide(x2, k)

    p = contains(node.x0+w_, node.y0, w_, h_, node.points)
    x3 = Node(node.x0 + w_, node.y0, w_, h_, p, node.depth+1)
    recursive_subdivide(x3, k)

    p = contains(node.x0+w_, node.y0+h_, w_, h_, node.points)
    x4 = Node(node.x0+w_, node.y0+h_, w_, h_, p, node.depth+1)
    recursive_subdivide(x4, k)

    node.children = [x1, x2, x3, x4]

def contains(x, y, w, h, points):
   pts = []
   for point in points:
       if point.x >= x and point.x <= x+w and point.y>=y and point.y<=y+h:
           pts.append(point)
   return pts

def find_children(node):
   if not node.children:
       return [node]
   else:
       children = []
       for child in node.children:
           children += (find_children(child))
   return children

def generate_path(gps_data, grid_fence):
    path = []
    current_fence = -1

    for point in gps_data:
        pt = Point(point.get('longitude'), point.get('latitude'))
        for i in range(len(grid_fence)):
            if grid_fence[i].contains(pt):
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

if __name__ == '__main__':
    # Testing Run Time
    start_time = time.time()

    # Set Recursion Limit
    sys.setrecursionlimit(5000)

    # Input
    max_depth = 3
    gpx_file_location = open('../Datasets/ds1_out.gpx', 'r')
    gpx_route = open('../Datasets/Routes/ds1_route.gpx', 'r')
    gpx_route = open('../Datasets/Routes/ds1_route_alt.gpx', 'r')
    # gpx_file_location = open('../Datasets/20200924.gpx', 'r')

    # Parse GPX Files
    gps_data_vehicle, points, min_lon, min_lat, width, height = parse_gpx_file(gpx_file_location)
    gps_data_route = parse_gpx_file(gpx_route)[:-5][0]

    # Set root node, create tree, subdivide
    root = Node(min_lon, min_lat, width+0.001, height+0.001, points, 0)
    tree = QTree(max_depth, points, root)
    tree.subdivide()

    # Loop Counting
    grid_cells = tree.get_cells()
    vehicle_path = generate_path(gps_data_vehicle, grid_cells)
    route_path = generate_path(gps_data_route, grid_cells)
    loops = route_check(route_path, vehicle_path)
    print(f"Number of Loops: {loops}")
    # print(f"Vehicle Path: {vehicle_path}")
    # print(f"Route Path: {route_path}")
    tree.graph()