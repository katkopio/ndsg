import pdb
import sys
import time
from api import parse_gpx_file, generate_corner_pts, generate_path, route_check, Point
from quadtree import convert_points, Node, QTree, recursive_subdivide, contains, find_children
from grid_creation import create_simple_gridmap, create_quadtree_gridmap
from statistics import stdev

def grid_creation_test(gpx_track, n, grid_type, threshold):
    """
    Returns average time taken to generate a grid of {grid_type} over {n} iterations, given {threshold}
    """
    with open(f'DS/{gpx_track}.gpx', 'r') as gpx_file_location:
        gps_data = parse_gpx_file(gpx_file_location)

    values = []

    if grid_type == "simple":
        for i in range(1, n):
            t0 = time.time()
            gridcells = create_simple_gridmap(gps_data, threshold)
            t1 = time.time()
            total = t1-t0
            values.append(total)

    elif grid_type == "quadtree":
        # k = ("points", threshold)
        k = ("depth", threshold)
        for i in range(1, n):
            t0 = time.time()
            tree = create_quadtree_gridmap(gps_data, k)
            t1 = time.time()
            total = t1-t0
            values.append(total)

    # print(values)
    avg = sum(values) / float(n)
    standard_dev = stdev(values)  
    return avg, standard_dev

def loop_count_test(gpx_track, gpx_route, n, grid_type, threshold):
    """
    Returns average time and number of loops taken for {grid_type} over {n} iterations, given {threshold}
    """

    with open(f'DS/{gpx_track}.gpx', 'r') as gpx_file:
        gps_data_vehicle = parse_gpx_file(gpx_file)

    with open(f'DS/{gpx_route}.gpx', 'r') as gpx_file:
        gps_data_route = parse_gpx_file(gpx_file)

    values = []

    if grid_type == "simple":
        grid_cells = create_simple_gridmap(gps_data_vehicle, threshold)
        for i in range(1, n):
            t0 = time.time()
            vehicle_path = generate_path(gps_data_vehicle, grid_cells)
            route_path = generate_path(gps_data_route, grid_cells)
            loops = route_check(route_path, vehicle_path)
            t1 = time.time()
            total = t1-t0
            values.append(total)

    elif grid_type == "quadtree":
        # k = ("points", threshold)
        k = ("depth", threshold)
        tree, grid_cells = create_quadtree_gridmap(gps_data_vehicle, k)
        for i in range(1, n):
            t0 = time.time()
            vehicle_path = generate_path(gps_data_vehicle, grid_cells)
            route_path = generate_path(gps_data_route, grid_cells)
            loops = route_check(route_path, vehicle_path)
            t1 = time.time()
            total = t1-t0
            values.append(total)
    
    # print(values)
    avg = sum(values) / float(n)
    standard_dev = stdev(values)  
    return avg, standard_dev, loops

if __name__ == '__main__':
    grid_type = sys.argv[1]

    gpx_track = "ds1"
    gpx_route = "ds1_route"
    n = 100

    if grid_type == "simple":
        threshold_list = [0.05, 0.06, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]
    elif grid_type == "quadtree":
        threshold_list = [2, 3, 4, 5, 6, 7]

    print(f"GRID TYPE: {grid_type}")
    print("Threshold, Grid_Avg, Grid_Stdev, Loop_Avg, Loop_Stdev, NumLoops")
    for threshold in threshold_list:
        grid_avg, grid_standard_dev = grid_creation_test(gpx_track, n, grid_type, threshold)
        loop_avg, loop_standard_dev, loops = loop_count_test(gpx_track, gpx_route, n, grid_type, threshold)
        print(f"{threshold} \t {grid_avg} \t {grid_standard_dev} \t {loop_avg} \t {loop_standard_dev} \t {loops}")