""" 
This code generates CPU/Mem Time Series data for quadtrees
Code is copy pasted from API and Quadtree modules in order to easily add time stamps
"""
import sys, time, psutil, gpxpy
import matplotlib.pyplot as plt
import matplotlib.patches as patches

""" CODE FROM API """

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

""" QUADTREE CODE """

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

""" END QUADTREE CODE """

def analyze(pid):
    pr = psutil.Process(pid=pid)
    print("type,time,cpupercent,cputime_user,cputime_system,rss,vms,pfaults,pageins,mempercent")
    while psutil.pid_exists(pid):
        print(f"1,{datetime.now()},{pr.cpu_percent()},{pr.cpu_times().user},{pr.cpu_times().system},{pr.memory_info().rss},{pr.memory_info().vms},{pr.memory_info().pfaults},{pr.memory_info().pageins},{pr.memory_percent()}")
        time.sleep(0.1)

def timestamp(comment):
    print(f"0,{datetime.now()},{comment}")

def main():
    # Open Files
    filename = "ds1"
    with open(f'../../DS/{filename}.gpx', 'r') as gpx_file_location:
        gps_data = parse_gpx_file(gpx_file_location)

    gpx_route = "ds1_route"
    with open(f'../../DS/{gpx_route}.gpx', 'r') as gpx_file:
        gps_route = parse_gpx_file(gpx_file)

    # Create Quadtree
    k = ("points", 200)
    k = ("depth", 5)

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

    # Loop Count
    vehicle_path = generate_path(gps_data, grid_cells)
    route_path = generate_path(gps_route, grid_cells)
    loops = route_check(route_path, vehicle_path)

if __name__ == '__main__':
    main()
    # p1 = Process(target=main)
    # p1.start()
    # p2 = Process(target=analyze, args=(p1.pid,))
    # p2.start()

    # p1.join()
    # p2.join()