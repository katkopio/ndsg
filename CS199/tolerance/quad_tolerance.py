import gpxpy, pdb
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from api import Point, parse_gpx_file, generate_corner_pts, generate_path, route_check
from quadtree import convert_points, Node, QTree, recursive_subdivide, contains, find_children
from grid_creation import create_quadtree_gridmap

def generate_quad_path(gps_data, grid_fence):
    # Same as generate_path but instead returns list of objects, instead of list of indices
    path = []
    current_fence = -1

    for point in gps_data:
        pt = Point(point.get('latitude'), point.get('longitude'))
        for i in range(len(grid_fence)):
            if grid_fence[i].contains(pt):
                if current_fence != i:
                    current_fence = i 
                    path.append(grid_fence[i])
                    break
    return path

def substring(substring, word):
    # Counts number of occurences of substring in string, alternate to route_check()
    # Input:  substring("katrinakatkatrkatkat", "kat")
    # Output: 5
    count = 0
    for i in range(len(word)):
        if word[i:i+len(substring)] == substring:
            count = count + 1
    return count

def list_slice(word, substring):
    # Splits the word into separate words based on first character of substring
    # Input:  list_slice("katrinakatkatrkatkat", "kat")
    # Output: ["katrina", "kat", "katr", "kat", "kat"]
    index = [i for i in range(len(word)) if word[i] == substring[0]]
    index.append(len(word))
    words = [word[index[i]:index[i+1]] for i in range(len(index)-1)]
    return words

def loop_counting(route, traj, grid_cells):
    errors = 0
    loops = 0
    r = 0
    i = 0
    while i < len(traj):
        if traj[i] == route[r]:
            r += 1
        else:
            ind = find_current_index(traj[i], route)
            # "Local" Errors
            if ind != -1:
                if ind > r:
                    r = ind + 1
                elif ind < r:
                    if traj[ind] == route[0]:
                        if traj[i - 1] == route[1]:
                            r = ind + 1
                        else: 
                            r = len(route) 
                    else:
                        r = ind + 1
            # "Foreign" Errors
            elif ind == -1:
                i, r, detour, missed_route = detour_info(i, r, route, traj)
                errors += check_siblings(detour, missed_route, grid_cells)
        if r == len(route):
            r = r % len(route)
            if errors == 0:
                loops += 1
            else:
                errors = 0
        i += 1
    return loops

def detour_info(i, r, route, traj):
    detour = []
    missed_route = []
    sub_traj = traj[i:]
    _i = i
    
    # Find Detour List
    for j in range(len(sub_traj)):
        if find_current_index(sub_traj[j], route) == -1:
            detour.append(sub_traj[j])
            i += 1
        else:
            break

    # Find Missing Route
    if _i == 0:
        if find_current_index(traj[i], route) == 0:
            missed_route = [route[0]]
        else:
            end_index = find_current_index(traj[i], route) + 1
            missed_route = route[0:end_index]
        r = find_current_index(traj[i], route) + 1
    elif _i != 0:
        start_index = find_current_index(traj[_i-1], route)
        if i == len(traj):
            missed_route = route[start_index:len(route)]
            r = len(route) # arbitrary, traj has already ended
        else:
            end_index = find_current_index(traj[i], route) + 1
            if end_index < start_index:
                missed_route = route[start_index:len(route)]
                missed_route.append(end_index)
            else:
                missed_route = route[start_index:end_index]
            r = find_current_index(traj[i], route) + 1
    # print(i, r, detour, missed_route)
    return i, r, detour, missed_route

def check_siblings(detour, missed_route, grid_cells):
    # A detour cell must be a sibling of at least one missed_route cell
    err = 0
    for d in detour:
        for r in missed_route:
            if grid_cells[d] not in grid_cells[r].siblings:
                err = 1
                break
    return err

def find_current_index(cell, route_list):
    # Find what index in the route_list the trajectory cell exists in
    for i in range(len(route_list)):
        if route_list[i] == cell:
            return i
    return -1

def generate_data(gps_traj, gps_route):
    loops = []
    loops_tol = []
    depths = [1,2,3,4,5,6,7]
    
    for num in depths:
        # Create Quadtree
        k = ("depth", num)
        tree, grid_cells = create_quadtree_gridmap(gps_traj, k)
        vehicle_path = generate_path(gps_traj, grid_cells)
        route_path = generate_path(gps_route, grid_cells)
        loops.append(route_check(route_path, vehicle_path))
        loops_tol.append(loop_counting(route_path, vehicle_path, grid_cells))

    print(depths)
    print(loops)
    print(loops_tol)

def quad_test():
    filename = "ds1"
    with open(f'../DS/{filename}.gpx', 'r') as gpx_file_location:
        gps_traj = parse_gpx_file(gpx_file_location)

    gpx_route = "ds1_route"
    with open(f'../DS/{gpx_route}.gpx', 'r') as gpx_file:
        gps_route = parse_gpx_file(gpx_file)

    loops = []
    loops_tol = []
    depths = [1,2,3,4,5,6,7]
    
    for num in depths:
        # Create Quadtree
        k = ("depth", num)
        tree, grid_cells = create_quadtree_gridmap(gps_traj, k)
        vehicle_path = generate_path(gps_traj, grid_cells)
        route_path = generate_path(gps_route, grid_cells)
        loops.append(route_check(route_path, vehicle_path))
        loops_tol.append(loop_counting(route_path, vehicle_path, grid_cells))

    if loops == [3, 2, 2, 1, 1, 1, 1] and loops_tol == [3, 3, 2, 2, 3, 1, 1]: 
        print("Test Passed")
    else:
        print(loops)
        print(loops_tol)
        print("Test Failed")

def main(gps_traj, gps_route):
    # Create Quadtree
    k = ("depth", 7)
    tree, grid_cells = create_quadtree_gridmap(gps_traj, k)

    # Generate List of Cell Numbers
    vehicle_path = generate_path(gps_traj, grid_cells)
    route_path = generate_path(gps_route, grid_cells)

    print(vehicle_path)
    print(route_path)
    print(f"OLD: {route_check(route_path, vehicle_path)}")
    print(f"LOOPS: {loop_counting(route_path, vehicle_path, grid_cells)}")

if __name__ =='__main__':
    # Open Files
    filename = "DS7-3-0422"
    with open(f'../DS/{filename}.gpx', 'r') as gpx_file_location:
        gps_traj = parse_gpx_file(gpx_file_location)

    gpx_route = "DS7_route"
    with open(f'../DS/{gpx_route}.gpx', 'r') as gpx_file:
        gps_route = parse_gpx_file(gpx_file)

    generate_data(gps_traj, gps_route)
    # main(gps_traj, gps_route)