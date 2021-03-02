# Trying to make a quadtree from GPS points using our own GPX data
# Adapted from: https://katherinepully.com/quadtree-python/

import sys
import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import gpxpy

def parse_gpx_file(gpx_file_location):
    """
    Parses GPX file and outputs x and y
    """
    points = []
    lat = []
    lon = []
    gpx = gpxpy.parse(gpx_file_location)
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                coordinate = Point(point.longitude, point.latitude)
                points.append(coordinate)
                lon.append(point.longitude)
                lat.append(point.latitude)
    return points, min(lon), min(lat), max(lon)-min(lon), max(lat)-min(lat)

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Node():
    def __init__(self, x0, y0, w, h, points):
        self.x0 = x0
        self.y0 = y0
        self.width = w
        self.height = h
        self.points = points
        self.children = []

    def get_width(self):
        return self.width
    
    def get_height(self):
        return self.height
    
    def get_points(self):
        return self.points

class QTree():
    def __init__(self, k, points, root):
        self.threshold = k
        self.points = points
        self.root = root

    def add_point(self, x, y):
        self.points.append(Point(x, y))
    
    def get_points(self):
        return self.points
    
    def subdivide(self):
        recursive_subdivide(self.root, self.threshold)
    
    def graph(self):
        fig = plt.figure(figsize=(8, 8))
        plt.title(f"By Max Number of Points: {self.threshold}")
        ax = fig.add_subplot(111)
        c = find_children(self.root)
        print(f"Max number of points in node: {self.threshold}")
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
    if len(node.points)<=k:
        return
    w_ = float(node.width/2)
    h_ = float(node.height/2)

    p = contains(node.x0, node.y0, w_, h_, node.points)
    x1 = Node(node.x0, node.y0, w_, h_, p)
    recursive_subdivide(x1, k)

    p = contains(node.x0, node.y0+h_, w_, h_, node.points)
    x2 = Node(node.x0, node.y0+h_, w_, h_, p)
    recursive_subdivide(x2, k)

    p = contains(node.x0+w_, node.y0, w_, h_, node.points)
    x3 = Node(node.x0 + w_, node.y0, w_, h_, p)
    recursive_subdivide(x3, k)

    p = contains(node.x0+w_, node.y0+h_, w_, h_, node.points)
    x4 = Node(node.x0+w_, node.y0+h_, w_, h_, p)
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

if __name__ == '__main__':
    start_time = time.time()

    sys.setrecursionlimit(5000)

    max_num_points = 1
    # gpx_file_location = open('../Datasets/ds1_out.gpx', 'r')
    gpx_file_location = open('../Datasets/20200924.gpx', 'r')

    points, min_lon, min_lat, width, height = parse_gpx_file(gpx_file_location)
    root = Node(min_lon, min_lat, width, height, points)

    tree = QTree(max_num_points, points, root)
    tree.subdivide()
    tree.graph()
