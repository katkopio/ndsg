import pdb
import sys
import time
from api import parse_gpx_file, generate_corner_pts, generate_path, route_check, Point
from quadtree import convert_points, Node, QTree, recursive_subdivide, contains, find_children
from grid_creation import create_simple_gridmap, create_quadtree_gridmap
from statistics import stdev
from tolerance import loop_counting

def grid_creation_test(gpx_track, n, grid_type, threshold):
    """
    Returns average time taken to generate a grid of {grid_type} over {n} iterations, given {threshold}
    """
    with open(f'../DS/{gpx_track}.gpx', 'r') as gpx_file_location:
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
    Returns average time taken for {grid_type} loop counting over {n} iterations, given {threshold}
    """

    with open(f'../DS/{gpx_track}.gpx', 'r') as gpx_file:
        gps_data_vehicle = parse_gpx_file(gpx_file)

    with open(f'../DS/{gpx_route}.gpx', 'r') as gpx_file:
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
    return avg, standard_dev

def tolerance_test(gpx_track, gpx_route, n, grid_type, threshold):
    """
    Returns average time taken for {grid_type} loop counting with tolerance
     over {n} iterations, given {threshold}
    """

    with open(f'../DS/{gpx_track}.gpx', 'r') as gpx_file:
        gps_data_vehicle = parse_gpx_file(gpx_file)

    with open(f'../DS/{gpx_route}.gpx', 'r') as gpx_file:
        gps_data_route = parse_gpx_file(gpx_file)

    values = []

    if grid_type == "simple":
        grid_cells = create_simple_gridmap(gps_data_vehicle, threshold)
        for i in range(1, n):
            t0 = time.time()
            vehicle_path = generate_path(gps_data_vehicle, grid_cells)
            route_path = generate_path(gps_data_route, grid_cells)
            loops = loop_counting(route_path, vehicle_path, grid_cells)
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
            loops = loop_counting(route_path, vehicle_path, grid_cells)
            t1 = time.time()
            total = t1-t0
            values.append(total)
    
    # print(values)
    avg = sum(values) / float(n)
    standard_dev = stdev(values)  
    return avg, standard_dev

def ds1_simple():
    gpx_track = "ds1"
    gpx_route = "ds1_route"
    n = 100
    grid_type = "simple"
    threshold_list = [0.25, 0.5, 0.75, 1]

    notol = []
    tol = []

    for threshold in threshold_list:
        loop_avg, loop_standard_dev = loop_count_test(gpx_track, gpx_route, n, grid_type, threshold)
        notol.append([threshold, loop_avg, loop_standard_dev])

    for threshold in threshold_list:
        tol_avg, tol_standard_dev = tolerance_test(gpx_track, gpx_route, n, grid_type, threshold)
        tol.append([threshold, tol_avg, tol_standard_dev])
    
    print("Dataset 1 Simple Grids")
    print(notol)
    print(tol)

def ds1_quad():
    gpx_track = "ds1"
    gpx_route = "ds1_route"
    n = 100
    grid_type = "quadtree"
    threshold_list = [1, 3, 5, 7]

    notol = []
    tol = []

    for threshold in threshold_list:
        loop_avg, loop_standard_dev = loop_count_test(gpx_track, gpx_route, n, grid_type, threshold)
        notol.append([threshold, loop_avg, loop_standard_dev])

    for threshold in threshold_list:
        tol_avg, tol_standard_dev = tolerance_test(gpx_track, gpx_route, n, grid_type, threshold)
        tol.append([threshold, tol_avg, tol_standard_dev])
    
    print("Dataset 1 Quadtrees")
    print(notol)
    print(tol)

def ds2_simple():
    gpx_track = "DS7-1-0420"
    gpx_route = "DS7_route"
    n = 100
    grid_type = "simple"
    threshold_list = [1, 4, 7, 10]

    notol = []
    tol = []

    for threshold in threshold_list:
        loop_avg, loop_standard_dev = loop_count_test(gpx_track, gpx_route, n, grid_type, threshold)
        notol.append([threshold, loop_avg, loop_standard_dev])

    for threshold in threshold_list:
        tol_avg, tol_standard_dev = tolerance_test(gpx_track, gpx_route, n, grid_type, threshold)
        tol.append([threshold, tol_avg, tol_standard_dev])
    
    print("Dataset 2 Simple Grids")
    print(notol)
    print(tol)

def ds2_quad():
    gpx_track = "DS7-1-0420"
    gpx_route = "DS7_route"
    n = 100
    grid_type = "quadtree"
    threshold_list = [1, 3, 5, 7]

    notol = []
    tol = []

    for threshold in threshold_list:
        loop_avg, loop_standard_dev = loop_count_test(gpx_track, gpx_route, n, grid_type, threshold)
        notol.append([threshold, loop_avg, loop_standard_dev])

    for threshold in threshold_list:
        tol_avg, tol_standard_dev = tolerance_test(gpx_track, gpx_route, n, grid_type, threshold)
        tol.append([threshold, tol_avg, tol_standard_dev])
    
    print("Dataset 2 Quadtrees")
    print(notol)
    print(tol)

if __name__ == '__main__':
    ds1_simple()
    ds1_quad()
    ds2_simple()
    ds2_quad()