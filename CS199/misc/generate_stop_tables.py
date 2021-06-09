from api import parse_gpx_file, parse_gpx_waypoints,stop_violation, Point
import pdb

def generate_violations(gps_data, stops, min_time, max_time):
    violations = []
    for i in range(len(stops)):
        if i % 2 == 0:
            point1 = Point(stops[i]['latitude'], stops[i]['longitude'])
            point2 = Point(stops[i+1]['latitude'], stops[i+1]['longitude'])
            violations += stop_violation(gps_data, min_time, max_time, point1, point2)
        else:
            continue
    return violations

def generate_latex(violations, caption, label):
    lst = []
    for v in violations:
        lst.append([v.get("violation"), v.get("duration"), v.get("time1").strftime("%a, %d %b %Y"), v.get("time1").strftime("%H:%M:%S GMT"), v.get("time2").strftime("%a, %d %b %Y"), v.get("time2").strftime("%H:%M:%S GMT")])

    print("\\begin{table}[ht]")
    print("\\centering")
    print("\\caption{",caption,"}",sep='')
    print("\\begin{tabular}{|c|c|c|c|}")
    print("\\hline")
    print("\\textbf{Type} & \\textbf{Duration} & \\textbf{Start} & \\textbf{End} \\\\ \hline")
    for i in lst:
        print(f"{i[0]} & {i[1]} & {i[2]} & {i[4]} \\\\")
        print(f"& & {i[3]} & {i[5]} \\\\ \hline")
    print("\\end{tabular}")
    print("\\label{Tab:",label,"}",sep='')
    print("\\end{table}")
    print()

if __name__ == '__main__':
    # filename = "ds1"
    # stop_file = "ds1_stops"
    # min_time = 3
    # max_time = 20
    # caption = "Some Caption"
    # label = "somelabel"

    # with open(f'../DS/{filename}.gpx', 'r') as gpx_file_location:
    #     gps_data = parse_gpx_file(gpx_file_location)
    # with open(f'../DS/{stop_file}.gpx', 'r') as gpx_file:
    #     stops = parse_gpx_waypoints(gpx_file)

    # violations = generate_violations(gps_data, stops, min_time, max_time)
    # generate_latex(violations, caption, label)


    dates = ["0420", "0421", "0422", "0424", "0425", "0426"]
    filenames = [f"DS7-1-{dates[0]}", f"DS7-2-{dates[1]}", f"DS7-3-{dates[2]}", f"DS7-4-{dates[3]}", f"DS7-5-{dates[4]}", f"DS7-6-{dates[5]}", "ds1"]

    for i in range(len(filenames)):
        with open(f'../DS/{filenames[i]}.gpx', 'r') as gpx_file_location:
            gps_data = parse_gpx_file(gpx_file_location)

        stop_file = "DS7_stops" if i != 6 else "ds1_stops"
        with open(f'../DS/{stop_file}.gpx', 'r') as gpx_file:
            stops = parse_gpx_waypoints(gpx_file)

        min_time = 3
        max_time = 120 if i != 6 else 20
        caption =  f"DS 2 {dates[i]} - Stop Violations" if i != 6 else "DS 1 Stop Violations"
        label = f"{dates[i]}stopviolation" if i != 6 else "ds1stopviolation"

        violations = generate_violations(gps_data, stops, min_time, max_time)
        generate_latex(violations, caption, label)