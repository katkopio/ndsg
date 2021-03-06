import pdb
from api import parse_gpx_file, generate_corner_pts, generate_path, route_check
from tolerance import loop_counting, detour_info, check_neighbors, adjacent_cells, find_current_index
from grid_creation import create_simple_gridmap

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

def generate_latex(title, cell_sizes, xmin, xmax, ymin, ytick, ysize, loops, loops_tol, caption, label): 
    print("\\begin{figure}[ht]")
    print("\\begin{center}")
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
    print("xlabel={Cell Sizes},")
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
    print(f"\\addplot[fill=clr1, draw=clr1_outline, postaction={{pattern=north east lines}}, bar shift=-{float(ysize)/2}cm]")
    loop_coords = ""
    for c in loops:
        loop_coords += str(c) + " "
    print("coordinates {",loop_coords[:-1],"};")
    print(f"\\addplot[fill=clr2, draw=clr2_outline, postaction={{pattern=horizontal lines}}, bar shift={float(ysize)/2}cm]")
    loop_coords_tol = ""
    for c in loops_tol:
        loop_coords_tol += str(c) + " "
    print("coordinates {",loop_coords_tol[:-1],"};")
    print("\\legend{No Tolerance, With Tolerance}")
    print("\\end{axis}")
    print("\\end{tikzpicture}")
    print("\caption{",caption,"}",sep='')
    print("\label{",label,"}",sep='')
    print("\end{center}")
    print("\end{figure}")
    print()

if __name__ =='__main__':
    dates = ["0420", "0421", "0422", "0424", "0425", "0426"]
    filenames = [f"DS7-1-{dates[0]}", f"DS7-2-{dates[1]}", f"DS7-3-{dates[2]}", f"DS7-4-{dates[3]}", f"DS7-5-{dates[4]}", f"DS7-6-{dates[5]}", "ds1"]
    ysize = 0.15
    loop_count = [3,5,5,3,5,2,2]

    for i in range(len(filenames)):
        gpx_route = "DS7_route" if i != 6 else "ds1_route"

        with open(f'../DS/{filenames[i]}.gpx', 'r') as gpx_file_location:
            gps_traj = parse_gpx_file(gpx_file_location)
        with open(f'../DS/{gpx_route}.gpx', 'r') as gpx_file:
            gps_route = parse_gpx_file(gpx_file)

        cell_sizes = [1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10] if i != 6 else [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1]

        correct_num_loops = loop_count[i]
        title =  f"{dates[i]} Simple Loop Counting with and without Tolerance" if i != 6 else "DS 1 Simple Loop Counting with and without Tolerance"
    
        loops, loops_tol, ymin, ytick = generate_coords(gps_traj, gps_route, cell_sizes, correct_num_loops)
        xmin = min(cell_sizes) - 0.05
        xmax = max(cell_sizes) + 0.05

        caption =  f"DS 2 {dates[i]} (Simple Grid) - Deviation from True Loop Count" if i != 6 else "DS 1 (Simple Grid) - Deviation from True Loop Count"
        label = f"{dates[i]}simpledeviation" if i != 6 else "ds1simpledeviation"

        generate_latex(title, cell_sizes, xmin, xmax, ymin, ytick, ysize, loops, loops_tol, caption, label)