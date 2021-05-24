"""
Compares (1) time it takes to create a grid and (2) number of cells created
in simple grid map vs Quadtrees
"""
import pdb
import sys
import time
from api import parse_gpx_file, generate_corner_pts, generate_grid_fence_2D
from quadtree import convert_points, Node, QTree, recursive_subdivide, contains, find_children

def create_simple_gridmap(gpx_track, cell_size):
    # Build Simple
    point1, point2 = generate_corner_pts(gpx_track, cell_size)
    return generate_grid_fence_2D(point1, point2, cell_size)

def create_quadtree_gridmap(gps_data, k):
    points = convert_points(gps_data)
    pt1, pt2 = generate_corner_pts(gps_data)
    min_lat = pt2.lat
    min_lon = pt1.lon
    height = pt1.lat - pt2.lat
    width = pt2.lon - pt1.lon

    # Build Quadtree
    root = Node(min_lon, min_lat, width, height, 0, points)
    tree = QTree(k, points, root)
    tree.subdivide()
    grid_cells = tree.get_cells()
    return tree, grid_cells

if __name__ == "__main__":
    filename = "ds1"
    with open(f'DS/{filename}.gpx', 'r') as gpx_file_location:
        gps_data = parse_gpx_file(gpx_file_location)
    cell_size = 0.1
    # k = ("points", 200)
    k = ("depth", 5)

    """SIMPLE GRID"""
    t0 = time.time()    
    gridcells = create_simple_gridmap(gps_data, cell_size)
    t1 = time.time()
    total = t1-t0

    print(f"[{filename}] Simple Grid for {cell_size}km: {total}")

    """QUADTREE"""
    t0 = time.time()
    tree = create_quadtree_gridmap(gps_data, k)
    # tree[0].graph()
    t1 = time.time()
    total = t1-t0

    print(f"[{filename}] Quadtree by max {k[0]} of {k[1]}: {total}")
