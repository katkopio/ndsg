import time
import random

def route_check(set_route, vehicle_route):
    set_route = "".join([str(x) for x in set_route])
    vehicle_route = "".join([str(x) for x in vehicle_route])

    loops = 0
    start = 0 
    while start < len(vehicle_route):
        pos = vehicle_route.find(set_route, start)

        if pos != -1:
            start = pos + 1
            loops += 1
        else:
            break

    return loops

if __name__ == "__main__":
    list_length = 1000

    runs = 100

    print('Points,Seconds')
    for i in range(1,11):
        route = random.sample(range(0, list_length + 1), list_length) * i
        traj = route

        values = []

        for j in range(1, runs + 1):
            t0 = time.time()
            loops = route_check(route, traj)
            t1 = time.time()
            values.append(t1-t0)

        avg = sum(values) / float(runs)
        print(f'{i}0000,{avg:.6f}')