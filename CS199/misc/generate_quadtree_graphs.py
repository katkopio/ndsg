import gpxpy, pdb
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
            if grid_cells[d] in grid_cells[r].siblings:
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

def generate_data(gps_traj, gps_route):
    

    print(depths)
    print(loops)
    print(loops_tol)

def generate_coords(gps_traj, gps_route, depths, correct_num_loops):
    loops = []
    loops_tol = []
    ymin = 0
    ymax = 0

    for num in depths:
        k = ("depth", num)
        tree, grid_cells = create_quadtree_gridmap(gps_traj, k)
        vehicle_path = generate_path(gps_traj, grid_cells)
        route_path = generate_path(gps_route, grid_cells)
        loops_y = route_check(route_path, vehicle_path) - correct_num_loops
        loops_tol_y = loop_counting(route_path, vehicle_path, grid_cells)-correct_num_loops
        loops.append((num, loops_y))
        loops_tol.append((num, loops_tol_y))
        ymin = min(ymin, loops_y, loops_tol_y)
        ymax = max(ymax, loops_y, loops_tol_y)

    ytick = [i for i in range(ymin, ymax+1)]

    return loops, loops_tol, ymin, ytick

def generate_latex(title, depths, xmin, xmax, xlabel, ymin, ytick, ysize, loops, loops_tol): 
    print("\\begin{tikzpicture}")
    print("\\begin{axis}[")
    print(f"ybar=-{ysize}cm,")        
    print(f"bar width={ysize}cm,")
    print("axis lines*=middle,")
    print("ylabel={Number of Loops},")
    print("width=\\textwidth * 0.5,")
    print("legend cell align=left,")
    print("legend style={at={(0.5,-0.15)}, anchor=north,legend columns=-1},")
    print(f"title={title},")
    print(f"xlabel={xlabel},")
    x_axes = "" 
    for x in depths:
        x_axes += str(x) + ","
    print("xtick={",x_axes[:-1],"},",sep='')
    print("symbolic x coords={",str(xmin),",",x_axes[:-1],",",str(xmax),"},",sep='')
    y_axes = ""
    for y in ytick:
        y_axes += str(y) + ","
    print("ytick={",y_axes[:-1],"},",sep='')
    print(f"xmin={xmin},")
    print(f"xmax={xmax},")
    print(f"ymin={ymin}]")
    print(f"\\addplot[fill=clr1,draw=none, bar shift=-{float(ysize)/2}cm]")
    loop_coords = ""
    for c in loops:
        loop_coords += str(c) + " "
    print("coordinates {",loop_coords[:-1],"};")
    print(f"\\addplot[fill=clr2, draw=none, bar shift={float(ysize)/2}cm]")
    loop_coords_tol = ""
    for c in loops_tol:
        loop_coords_tol += str(c) + " "
    print("coordinates {",loop_coords_tol[:-1],"};")
    print("\\legend{No Tolerance, With Tolerance}")
    print("\\end{axis}")
    print("\\end{tikzpicture}")

if __name__ =='__main__':
    filename = "ds1"
    gpx_route = "ds1_route"
    ysize = 0.2
    correct_num_loops = 2
    depths = [1,2,3,4,5,6,7]
    title = "Some Title"
    xlabel = "Some Label"

    with open(f'../DS/{filename}.gpx', 'r') as gpx_file_location:
        gps_traj = parse_gpx_file(gpx_file_location)
    with open(f'../DS/{gpx_route}.gpx', 'r') as gpx_file:
        gps_route = parse_gpx_file(gpx_file)

    loops, loops_tol, ymin, ytick = generate_coords(gps_traj, gps_route, depths, correct_num_loops)
    xmin = min(depths) - 1
    xmax = max(depths) + 1

    generate_latex(title, depths, xmin, xmax, xlabel, ymin, ytick, ysize, loops, loops_tol)
