""" 
Make a quadtree given GPS points
- User can choose the splitting threshold (by depth, or by maximum number of nodes)
- User can count number of loops taken
Reference: https://katherinepully.com/quadtree-python/
"""
import pdb
import sys
import time
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from api import parse_gpx_file, generate_corner_pts, Point

def convert_points(gps_data):
    """
    Converts gps_data into Point objects
    """
    points = []
    for point in gps_data:
        coordinate = Point(point.get("latitude"), point.get("longitude"))
        points.append(coordinate)
    return points

class Node():
    def __init__(self, x, y, w, h, d, points):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.depth = d
        self.points = points
        self.siblings = []
        self.children = []

    def num_points(self):
        return len(self.points)
    
    def get_depth(self):
        return self.depth

    def contains(self, point):
        if point.lon >= self.x and point.lon <= (self.x + self.width) and point.lat >= self.y and point.lat <= (self.y + self.height):
            return True
        else:
            return False

class QTree():
    def __init__(self, k, points, root):
        self.threshold = k
        self.points = points
        self.root = root

    def get_cells(self):
        return find_children(self.root)

    def subdivide(self):
        recursive_subdivide(self.root, self.threshold)
    
    def graph(self):
        fig = plt.figure(figsize=(8, 8))
        plt.title(f"By max {self.threshold[0]}: {self.threshold[1]}")
        ax = fig.add_subplot(111)
        c = find_children(self.root)
        print(f"Number of cells: {len(c)}")
        areas = set()
        for el in c:
            areas.add(el.width*el.height)
        print(f"Minimum segment area: {min(areas)} units")
        for n in c:
            ax.add_patch(patches.Rectangle((n.x, n.y), n.width, n.height, fill=False))
        x = [point.lon for point in self.points]
        y = [point.lat for point in self.points]
        plt.plot(x, y, marker=".", markersize=1)
        # plt.savefig(f'Quadtree/{self.threshold[0]} {self.threshold[1]}.png', transparent = True, dpi = 300, bbox_inches='tight')
        plt.show()
        return

def recursive_subdivide(node, k):
    if(k[0] == "depth"):
        if node.get_depth() >= k[1] or node.num_points() <= 1:
            return
    elif(k[0] == "points"):
        if node.num_points() <= k[1]:
            return

    w_ = float(node.width/2)
    h_ = float(node.height/2)

    p = contains(node.x, node.y, w_, h_, node.points)
    x1 = Node(node.x, node.y, w_, h_, node.depth+1, p)
    recursive_subdivide(x1, k)

    p = contains(node.x, node.y+h_, w_, h_, node.points)
    x2 = Node(node.x, node.y+h_, w_, h_, node.depth+1, p)
    recursive_subdivide(x2, k)

    p = contains(node.x+w_, node.y, w_, h_, node.points)
    x3 = Node(node.x + w_, node.y, w_, h_, node.depth+1, p)
    recursive_subdivide(x3, k)

    p = contains(node.x+w_, node.y+h_, w_, h_, node.points)
    x4 = Node(node.x+w_, node.y+h_, w_, h_, node.depth+1, p)
    recursive_subdivide(x4, k)

    x1.siblings = [x2, x3, x4]
    x2.siblings = [x1, x3, x4]
    x3.siblings = [x1, x2, x4]
    x4.siblings = [x1, x2, x3]

    node.children = [x1, x2, x3, x4]

def contains(x, y, w, h, points):
   pts = []
   for point in points:
       if point.lon >= x and point.lon <= x+w and point.lat>=y and point.lat<=y+h:
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
    t0 = time.time()

    k = ("depth", 5)
    # k = ("points", 150)
    gpx_file_location = open(f'DS/ds2.gpx', 'r')
    gps_data = parse_gpx_file(gpx_file_location)

    points = convert_points(gps_data)
    pt1, pt2 = generate_corner_pts(gps_data)
    min_lat = pt2.lat
    min_lon = pt1.lon
    height = pt1.lat - pt2.lat
    width = pt2.lon - pt1.lon
    root = Node(min_lon, min_lat, width, height, 0, points)
    tree = QTree(k, points, root)
    tree.subdivide()
    grid_cells = tree.get_cells()
    tree.graph()

    # Timer
    t1 = time.time()
    total = t1-t0
    print(f"Quadtree by max {k[0]} of {k[1]}: {total}")