import time
import gpxpy

class Point():
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

class Polygon():
    def __init__(self, top_left_pt, bottom_right_pt):
        self.top_left_pt = top_left_pt
        self.bottom_right_pt = bottom_right_pt

def generate_grid_fence(point1, point2, side_length):
    grid_fence = []

    side_interval = side_length * 0.009

    latitude = point1.lat
    longitude = point1.lon

    while latitude > point2.lat:
        row = []

        while longitude < point2.lon:
            top_left_pt = Point(latitude, longitude)
            bottom_right_pt = Point(latitude - side_interval, longitude + side_interval)

            geofence = Polygon(top_left_pt, bottom_right_pt)
            row.append(geofence)

            longitude += side_interval

        longitude = point1.lon
        latitude -= side_interval

        grid_fence.append(row)

    return grid_fence

if __name__ == "__main__":
    pt1 = Point(0.09,0)
    pt2 = Point(0, 0.09)

    cell_size = 1
    grid_step_interval = 10 * 0.009 # 0.009 converts km into lat/lon degrees
    cell_step_interval = 0.1

    runs = 100

    # varying lat difference
    print('Height,Seconds')
    for i in range(1,11):
        curr_pt1 = Point(pt1.lat + (i-1) * (grid_step_interval), 0)

        values = []

        for j in range(1, runs + 1):
            t0 = time.time()
            grid = generate_grid_fence(curr_pt1, pt2, cell_size)
            t1 = time.time()
            values.append(t1-t0)

        avg = sum(values) / float(runs)
        print(f'{i}0,{avg:.6f}')

    print()

    #varying lon difference
    print('Width,Seconds')
    for i in range(1,11):
        curr_pt2 = Point(0, pt2.lon + (i-1) * (grid_step_interval))

        values = []

        for j in range(1, runs + 1):
            t0 = time.time()
            grid = generate_grid_fence(pt1, curr_pt2, cell_size)
            t1 = time.time()
            values.append(t1-t0)

        avg = sum(values) / float(runs)
        print(f'{i}0,{avg:.6f}')

    print()

    #varying cell size
    print('Cell Size,Seconds')
    for i in range(1,11):
        curr_cell_size = cell_size - (i-1) * (cell_step_interval)

        values = []

        for j in range(1, runs + 1):
            t0 = time.time()
            grid = generate_grid_fence(pt1, pt2, curr_cell_size)
            t1 = time.time()
            values.append(t1-t0)

        avg = sum(values) / float(runs)
        print(f'{(cell_size - (i-1) * (cell_step_interval)):.1f},{avg:.6f}')
