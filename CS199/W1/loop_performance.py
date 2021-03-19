"""
Compares time taken to calculate number of loops in simple grid map and quadtrees

Note: this includes time to generate grid map of trajectory and route
"""
import sys
import time
from api import parse_gpx_file, generate_corner_pts, generate_grid_fence, generate_path, route_check, Point
from grid_creation import create_simple_gridmap, create_quadtree_gridmap

def simple_looping(gps_data_vehicle, gps_data_route, grid_fence):
    vehicle_path = generate_path(gps_data_vehicle, grid_fence)
    route_path = generate_path(gps_data_route, grid_fence)
    loops = route_check(route_path, vehicle_path)
    return loops

def quadtree_looping(gps_data_vehicle, gps_data_route, grid_cells):
    vehicle_path = generate_path(gps_data_vehicle, grid_cells)
    route_path = generate_path(gps_data_route, grid_cells)
    loops = route_check(route_path, vehicle_path)
    return loops

if __name__ == "__main__":
    gpx_track = "ds1"
    gpx_route = "ds1_route"
    with open(f'DS/{gpx_track}.gpx', 'r') as gpx_file:
        gps_data_vehicle = parse_gpx_file(gpx_file)

    with open(f'DS/{gpx_route}.gpx', 'r') as gpx_file:
        gps_data_route = parse_gpx_file(gpx_file)

    """SIMPLE GRID"""
    # # Create Grid Map
    # cell_size = 0.1
    # grid_cells = create_simple_gridmap(gps_data_vehicle, cell_size)

    # # Count Loops
    # t0 = time.time()
    # loops = simple_looping(gps_data_vehicle, gps_data_route, grid_cells)
    # t1 = time.time()
    # total = t1-t0
    # print(f"[{gpx_track}] {cell_size}km Simple Grid: {loops} loops, {total}")

    """QUADTREE GRID"""
    # Create Quadtree

    # k = ("points", 200)
    k = ("depth", 3)
    tree, grid_cells = create_quadtree_gridmap(gps_data_vehicle, k)

    # Count Loops
    t0 = time.time()

    loops = quadtree_looping(gps_data_vehicle, gps_data_route, grid_cells)
    
    t1 = time.time()
    total = t1-t0
    print(f"[{gpx_track}] Quadtree by max {k[0]} of {k[1]}: {loops} loops, {total}")
