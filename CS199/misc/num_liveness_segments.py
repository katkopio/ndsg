from api import check_liveness, parse_gpx_file
from math import ceil 

def num_segments(gps_data, time_limit):
    segments = check_liveness(gps_data, time_limit)
    violations = segments.get("segments")
    lst = []
    for v in violations:
        lst.append([v.get("liveness"), v.get("time1").strftime("%a, %d %b %Y"), v.get("time1").strftime("%H:%M:%S GMT"), v.get("time2").strftime("%a, %d %b %Y"), v.get("time2").strftime("%H:%M:%S GMT")])

    return len(lst)

if __name__ == '__main__':
    dates = ["0420", "0421", "0422", "0424", "0425", "0426"]
    filenames = [f"DS7-1-{dates[0]}", f"DS7-2-{dates[1]}", f"DS7-3-{dates[2]}", f"DS7-4-{dates[3]}", f"DS7-5-{dates[4]}", f"DS7-6-{dates[5]}", "ds1"]
    avg = [20, 16, 19, 19, 15, 18, 2]
    avg_std = [54, 29, 39, 49, 28, 45, 2]
    
    for i in range(len(filenames)):
        with open(f'../DS/{filenames[i]}.gpx', 'r') as gpx_file_location:
            gps_data = parse_gpx_file(gpx_file_location)

        num_20 = num_segments(gps_data, 20)

        time_limit = avg[i] if i != 6 else 2
        num_avg = num_segments(gps_data, time_limit)

        time_limit = avg_std[i] if i != 6 else 2
        num_avg_sd = num_segments(gps_data, time_limit)

        print(num_20, num_avg, num_avg_sd)