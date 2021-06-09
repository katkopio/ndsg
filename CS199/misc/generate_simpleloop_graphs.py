import pdb
from api import parse_gpx_file, generate_corner_pts, generate_path, route_check
from grid_creation import create_simple_gridmap

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
                errors += check_neighbors(detour, missed_route, grid_cells)
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
    return i, r, detour, missed_route

def check_neighbors(detour, missed_route, grid_cells):
    match = False
    err = 0

    width = len(grid_cells[0])
    length = len(grid_cells) * len(grid_cells[0])

    for d in detour:
        for r in missed_route:
            if d in adjacent_cells(r, width, length):
                match = True 
                break
            else:
                match = False 
        if match == False:
            err = 1
            break 
    return err

def adjacent_cells(d, w, l):
    # Top Left
    if d == 0:
        return [d+1, d+w, d+w+1]
    # Top Right
    elif d == w-1:
        return [d-1, d+w-1, d+w]
    # Bottom Left
    elif d == l-w:
        return [d-w, d-w+1, d+1]
    # Bottom Right
    elif d == l-1:
        return [d-w-1, d-w, d-1]
    # North
    elif d < w:
        return [d-1, d+1, d+w-1, d+w, d+w+1]
    # South
    elif (d < l) and (d >= l-w):
        return [d-w-1, d-w, d-w+1, d-1, d+1]
    # West
    elif d % w == 0:
        return [d-w, d-w+1, d+1, d+w, d+w+1]
    # East
    elif d % w == w - 1:
        return [d-w-1, d-w, d-1, d+w-1, d+w]
    # Middle
    else:
        return [d-w-1, d-w, d-w+1, d-1, d+1, d+w-1, d+w, d+w+1]

def find_current_index(cell, route_list):
    # Find what index in the route_list the trajectory cell exists in
    for i in range(len(route_list)):
        if route_list[i] == cell:
            return i
    return -1

def generate_coords(gps_traj, gps_route, cell_sizes, correct_num_loops):
    loops = []
    loops_tol = []
    ymin = 0
    ymax = 0

    for cell_size in cell_sizes:
        grid_cells = create_simple_gridmap(gps_traj, cell_size)
        vehicle_path = generate_path(gps_traj, grid_cells)
        route_path = generate_path(gps_route, grid_cells)
        loops_y = route_check(route_path, vehicle_path) - correct_num_loops
        loops_tol_y = loop_counting(route_path, vehicle_path, grid_cells)-correct_num_loops
        loops.append((cell_size, loops_y))
        loops_tol.append((cell_size, loops_tol_y))
        ymin = min(ymin, loops_y, loops_tol_y)
        ymax = max(ymax, loops_y, loops_tol_y)

    ytick = [i for i in range(ymin, ymax+1)]

    return loops, loops_tol, ymin, ytick

def generate_latex(title, cell_sizes, xmin, xmax, xlabel, ymin, ytick, ysize, loops, loops_tol): 
    print("\\begin{tikzpicture}")
    print("\\begin{axis}[")
    print(f"ybar=-{ysize}cm,")        
    print(f"bar width={ysize}cm,")
    print("axis lines*=middle,")
    print("ylabel={Deviation from True Loop Count},")
    print("width=\\textwidth * 0.5,")
    print("x tick label style={rotate=45,anchor=east},")
    print("xticklabel style={font=\small},")
    print("legend cell align=left,")
    print("legend style={at={(0.5,-0.15)}, anchor=north,legend columns=-1},")
    print(f"title={title},")
    print(f"xlabel={xlabel},")
    x_axes = "" 
    for x in cell_sizes:
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
    print(f"\\addplot[fill=clr1,draw=clr1_outline, bar shift=-{float(ysize)/2}cm]")
    loop_coords = ""
    for c in loops:
        loop_coords += str(c) + " "
    print("coordinates {",loop_coords[:-1],"};")
    print(f"\\addplot[fill=clr2, draw=clr2_outline, bar shift={float(ysize)/2}cm]")
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
    ysize = 0.15
    correct_num_loops = 2
    cell_sizes = [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1]
    # cell_sizes = [1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,]
    title = "Simple Loop Counting with and without Tolerance"
    xlabel = "Cell Sizes"

    with open(f'../DS/{filename}.gpx', 'r') as gpx_file_location:
        gps_traj = parse_gpx_file(gpx_file_location)
    with open(f'../DS/{gpx_route}.gpx', 'r') as gpx_file:
        gps_route = parse_gpx_file(gpx_file)

    loops, loops_tol, ymin, ytick = generate_coords(gps_traj, gps_route, cell_sizes, correct_num_loops)
    xmin = min(cell_sizes) - 0.05
    xmax = max(cell_sizes) + 0.05

    generate_latex(title, cell_sizes, xmin, xmax, xlabel, ymin, ytick, ysize, loops, loops_tol)