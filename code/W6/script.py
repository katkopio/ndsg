"""
What we wanna do is...
- Generate files to analyze with time_freq
- Shove it in grid_size.py and output the results
- Generate the grids with grid_visualize.py
- Graph the results 
"""

from time_freq import time_freq
from grid_visualize import visualize
from grid_size import parse_gpx_file, generate_grid_pts, generate_grid_fence, generate_path, generate_route, route_check
import datetime

def generate_time_files(time_interval):
    # Generate GPX Time Files (ds1_time_<interval>s.gpx) using time_freq
    for t in time_interval:
        time_freq(t)

def generate_grids(time_interval, distance_interval):
    # Given GPX Time Files, generate different grid sizes per time interval
    for t in time_interval:
        for d in distance_interval:
            file_name = f"ds1_time_{t}s.gpx"
            visualize(file_name, d)

def analyze_gpx(time_interval, distance_interval):
    for t in time_interval:
        for d in distance_interval:
            file_name = f"ds1_time_{t}s.gpx"
            side_length = d

            with open('ds1_times/' + file_name, 'r') as gpx_file:
                gpx_track = parse_gpx_file(gpx_file)

            point1 = (14.65498, 121.05837) # top left pt
            point2 = (14.64259, 121.07483) # bottom right pt

            grid_pts = generate_grid_pts(point1, point2, side_length)
            grid_fence = generate_grid_fence(grid_pts)

            start = datetime.datetime.now().timestamp()
            vehicle_route = generate_path(gpx_track, grid_fence)
            set_route = generate_route(vehicle_route)
            loops = route_check(set_route, vehicle_route)
            end = datetime.datetime.now().timestamp()

            time = "{:7.6f}".format(end - start)
            if loops == 2:
                accuracy = True
            else:
                accuracy = False
            
            print(f"{t}s {d}km,{t},{d},{loops},{time},{accuracy}")

if __name__ == '__main__':
    time_interval = [i for i in range(10, 130, 10)]
    distance_interval = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    # generate_time_files(time_interval)
    # generate_grids(time_interval, distance_interval)

    print("desc,data_freq,grid_distance,num_loops,time,accuracy")
    analyze_gpx(time_interval, distance_interval)

# run with python3 script.py > out.txt
# else, will print in terminal
