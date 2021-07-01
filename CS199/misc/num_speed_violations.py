from api import speed_violation, parse_gpx_file
import pdb

if __name__ == '__main__':
    dates = ["0420", "0421", "0422", "0424", "0425", "0426"]
    filenames = [f"DS7-1-{dates[0]}", f"DS7-2-{dates[1]}", f"DS7-3-{dates[2]}", f"DS7-4-{dates[3]}", f"DS7-5-{dates[4]}", f"DS7-6-{dates[5]}", "ds1"]

    for i in range(len(filenames)):
        with open(f'../../DS/{filenames[i]}.gpx', 'r') as gpx_file_location:
            gps_data = parse_gpx_file(gpx_file_location)

        s = 60 if i != 6 else 30
        t = 0.5

        e_violations = speed_violation(gps_data, "Explicit", s, t)
        l_violations = speed_violation(gps_data, "Location", s, t)

        print(len(e_violations), len(l_violations))