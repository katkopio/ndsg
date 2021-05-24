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
    match = False
    err = 0

    for d in detour:
        for r in missed_route:
            if grid_cells[r] in grid_cells[d].siblings:
                match = True 
                break
            else:
                match = False 
        if match == False:
            err = 1
            break 
    return err

def find_current_index(cell, route_list):
    # Find what index in the route_list the trajectory cell exists in
    for i in range(len(route_list)):
        if route_list[i] == cell:
            return i
    return -1

if __name__ =='__main__':
    # Open Files
    filename = "ds1"
    with open(f'../DS/{filename}.gpx', 'r') as gpx_file_location:
        gps_traj = parse_gpx_file(gpx_file_location)

    gpx_route = "ds1_route"
    with open(f'../DS/{gpx_route}.gpx', 'r') as gpx_file:
        gps_route = parse_gpx_file(gpx_file)

    # Create Quadtree
    k = ("depth", 7)
    tree, grid_cells = create_quadtree_gridmap(gps_traj, k)

    # Generate List of Cell Numbers
    vehicle_path = generate_path(gps_traj, grid_cells)
    route_path = generate_path(gps_route, grid_cells)

    print(f"LOOPS: {loop_counting(route_path, vehicle_path, grid_cells)}")